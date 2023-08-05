import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from configparser import ConfigParser
from fnmatch import fnmatch
from glob import iglob
from hashlib import sha256
from json import JSONDecodeError, dumps as json_dumps
from sys import version_info, version
from textwrap import dedent
from argparse import ArgumentParser
from io import StringIO
from subprocess import check_output, CalledProcessError
from time import time

from pypandoc import get_pandoc_path, convert_file, convert_text
from yaml import safe_load
from panflute import load as pf_load, dump as pf_dump
from deepmerge import always_merger

logging.basicConfig(format="%(asctime)s-%(levelname)s: %(message)s")
logger = logging.getLogger("pandoc-compose")
logger.setLevel(logging.ERROR)

KNOWN_TARGET_FORMATS = {
    "commonmark": ".md",
    "context": ".tex",
    "docbook": ".xml",
    "docbook4": ".xml",
    "docbook5": ".xml",
    "docx": ".docx",
    "epub": ".epub",
    "epub2": ".epub",
    "epub3": ".epub",
    "fb2": ".xml",
    "gfm": ".md",
    "html": ".html",
    "html4": ".html",
    "html5": ".html",
    "icml": ".icml",
    "ipynb": ".py",
    "jats": ".xml",
    "jira": ".txt",
    "json": ".json",
    "latex": ".tex",
    "markdown": ".md",
    "markdown_github": ".md",
    "markdown_mmd": ".md",
    "markdown_phpextra": ".md",
    "markdown_strict": ".md",
    "mediawiki": ".txt",
    "muse": ".muse",
    "native": ".hs",
    "odt": ".odt",
    "opendocument": ".odf",
    "opml": ".opml",
    "plain": ".txt",
    "pdf": ".pdf",
    "pptx": ".pptx",
    "revealjs": ".html",
    "rst": ".rst",
    "rtf": ".rtf",
    "s5": ".html",
    "slideous": ".html",
    "slidy": ".html",
    "texinfo": ".texinfo",
    "textile": ".txt",
    "xwiki": ".txt",
    "zimwiki": ".txt",
}


class PandocComposeGenericError(Exception):
    def __init__(self, message):
        super().__init__()
        self.message = message


class PandocConfigNotFoundError(PandocComposeGenericError):
    def __init__(self, config_file_path):
        msg = dedent(
            """
            ERROR: {0} does not exist. 
            Please use `dest` argument to point to, or exectute this command in 
            a directory containing a {1} file.
        """
        ).format(config_file_path, PandocConfig.PANDOC_COMPOSE_FILE)
        super().__init__(msg)


class PandocConfig:
    PANDOC_COMPOSE_FILE = "pandoc-compose.yml"
    POSSIBLE_OVERRIDES_IN_MD = ["pandoc_options"]

    def __init__(self, config_file_path, original_config):
        self.config_file_path = config_file_path
        self.files = []
        self.pandoc = {}
        self.pandoc_options = []
        self.__original_config = original_config

        self.__process_config()

    def merge(self, config_override):
        new_config = always_merger.merge(self.__original_config.copy(), config_override)
        return PandocConfig(self.config_file_path, new_config)

    def __process_config(self):
        self.__process_files_section()
        self.pandoc = self.__original_config.get("pandoc", {})
        self.pandoc_options = self.__original_config.get("pandoc_options", {})
        pass

    def __process_files_section(self):
        files = self.__original_config.get("files", None)
        if files is not None:
            try:
                self.files = list(filter(self.__filter_and_warning, files))
            except TypeError:
                logger.warning(
                    "`files` section of %s is malformed; %s",
                    self.config_file_path,
                    'Falling back to default "**/*.md": "pdf"',
                )
                self.files = [{"**/*.md": "pdf"}]
        else:
            self.files = [{"**/*.md": "pdf"}]

    def __str__(self):
        return json_dumps(
            self.__original_config, indent=4, sort_keys=True, ensure_ascii=False
        )

    @staticmethod
    def get_config_file_path(dest):
        return os.path.join(dest, PandocConfig.PANDOC_COMPOSE_FILE)

    @staticmethod
    def __filter_and_warning(item):
        _, output_format = list(item.items())[0] if (len(item)) > 0 else ""
        if KNOWN_TARGET_FORMATS.get(output_format, None) is None:
            logger.warning(
                "{0} is not a currently supported format".format(output_format)
            )
            return False
        return True


class PandocComposeConfig:
    PANDOC_COMPOSE_HASH_FILE_NAME = ".pandoc-compose-hash"
    HASH_DEFAULT_SECTION = "DEFAULT"

    def __init__(self, cli_args, *args):
        self.destination = os.path.join(cli_args.dest, "")
        self.pandoc_config = None
        self.timeout = 0
        self.force = False
        self.hash_file_path = None
        self.hash_config = {}
        self.pandoc_config_file_hash = None

        config_file_path = PandocConfig.get_config_file_path(self.destination)
        if not os.path.exists(config_file_path):
            raise PandocConfigNotFoundError(config_file_path)

        original_config = self.__read_config(config_file_path)
        pandoc_compose_config = original_config.pop("pandoc_compose_options", {})
        self.pandoc_config = PandocConfig(config_file_path, original_config)

        self.__init_pandoc_compose_config(pandoc_compose_config, cli_args)

        if len(list(args)) > 0:
            self.pandoc_config = pandoc_config.merge({"pandoc_options": remaining})

        self.__init_hash_config()

    def __init_hash_config(self):
        self.pandoc_config_file_hash = self.get_file_hash(
            self.pandoc_config.config_file_path
        )

        self.hash_file_path = os.path.join(
            self.destination, self.PANDOC_COMPOSE_HASH_FILE_NAME
        )

        if os.path.exists(self.hash_file_path):
            cp = ConfigParser()
            # https://stackoverflow.com/questions/19359556/configparser-reads-capital-keys-and-make-them-lower-case
            cp.optionxform = str
            cp.read(self.hash_file_path)
            try:
                self.hash_config = dict(cp[self.HASH_DEFAULT_SECTION])
            except KeyError:
                self.hash_config = {}

    def __init_pandoc_compose_config(self, pandoc_compose_original_config, cli_args):
        level = logging.getLevelName(
            {1: "WARNING", 2: "INFO", 3: "DEBUG"}.get(cli_args.verbose)
        )
        if isinstance(level, int):
            logger.setLevel(level)
        else:
            verbose = pandoc_compose_original_config.get("verbose")
            level = logging.getLevelName(verbose)
            if isinstance(level, int):
                logger.setLevel(level)

        timeout = (
            cli_args.timeout
            if cli_args.timeout is not None
            else pandoc_compose_original_config.get("timeout", "10m")
        )
        self.timeout = self.__compute_timeout(timeout)

        self.force = cli_args.force or pandoc_compose_original_config.get(
            "force", False
        )

    @staticmethod
    def get_file_hash(fname):
        def file_as_blockiter(blocksize=65536):
            with open(fname, "rb") as f:
                block = f.read(blocksize)
                while len(block) > 0:
                    yield block
                    block = f.read(blocksize)

        file_hash = sha256()

        for chunk in file_as_blockiter():
            file_hash.update(chunk)

        return file_hash.hexdigest()

    @staticmethod
    def __compute_timeout(timeout):
        try:
            if timeout.endswith("h"):
                return int(timeout[:-1]) * 60 * 60
            elif timeout.endswith("m"):
                return int(timeout[:-1]) * 60
            elif timeout.endswith("s"):
                return int(timeout[:-1])
            else:
                return int(timeout)
        except ValueError:
            raise PandocComposeGenericError("--timeout option is not correct")

    @staticmethod
    def __read_config(config_file_path):
        with open(config_file_path, mode="r") as f:
            _config = safe_load(f)
            return _config if isinstance(_config, dict) else {}


class ConvertFileCallback:
    def __init__(self, file_path, target_format, pandoc_compose_config):
        self.file_path = file_path
        self.target_format = target_format
        self.pandoc_compose_config = pandoc_compose_config
        self.pandoc_config = pandoc_compose_config.pandoc_config

    def __call__(self, *args, **kwargs):
        try:
            logger.info("Starting processing %s", self.file_path)
            if logger.isEnabledFor(logging.DEBUG):
                self.__convert_file_timed()
            else:
                self.__convert_file()
            logger.info("Finished processing %s", self.file_path)
        except RuntimeError as e:
            rest = (
                ""
                if logger.isEnabledFor(logging.WARNING)
                else "\n    | (Try to increase the verbosity to see error message)"
            )
            logger.error("Pandoc failed to convert %s%s", self.file_path, rest)
            logger.warning("Error was:\n    | %s", e)

    def __convert_file(self):
        ast = self.__get_pandoc_ast()
        ast_meta = ast.get_metadata(builtin=True).copy()

        individual_overrides = ast_meta.get("pandoc_compose", None)
        new_config = {}
        if isinstance(individual_overrides, dict):
            for key in PandocConfig.POSSIBLE_OVERRIDES_IN_MD:
                if key == "pandoc_options":
                    # Pandoc's `smart` markdown extension replaces double dashes to half-em-dashes which breaks cli opts
                    new_config[key] = [
                        x.replace("–", "--").replace("—", "---")
                        for x in individual_overrides.get(key)
                    ]
                else:
                    new_config[key] = individual_overrides.get(key)
            ast_meta.pop("pandoc_compose")

        new_config["pandoc"] = ast_meta

        self.pandoc_config = self.pandoc_config.merge(new_config)

        if logger.isEnabledFor(logging.DEBUG):
            json_str = str(self.pandoc_config).replace("\n", "\n    | ")
            logger.debug(
                "pandoc-compose configuration for %s:\n    | %s",
                self.file_path,
                json_str,
            )

        ast.metadata = self.pandoc_config.pandoc

        extension = KNOWN_TARGET_FORMATS.get(
            self.target_format, KNOWN_TARGET_FORMATS.get(self.target_format, ".txt")
        )
        new_name = os.path.splitext(self.file_path)[0] + extension
        extra_args = self.pandoc_config.pandoc_options

        if self.target_format == "latex":
            # Produce standalone fully compilable LaTeX
            extra_args.append("--standalone")

        with StringIO() as pandoc_ast_json:
            pf_dump(ast, pandoc_ast_json)
            convert_text(
                pandoc_ast_json.getvalue(),
                self.target_format,
                extra_args=extra_args,
                format="json",
                outputfile=new_name,
            )

    def __convert_file_timed(self):
        start_time = time()
        self.__convert_file()
        end_time = time()
        sec_elapsed = end_time - start_time

        h = int(sec_elapsed / (60 * 60))
        m = int((sec_elapsed % (60 * 60)) / 60)
        s = sec_elapsed % 60.0

        h_str = "" if h == 0 else "{}h".format(h)
        m_str = "" if m == 0 else "{:>02}m".format(m)
        s_str = "" if s == 0 else "{:>05.2f}s".format(s)

        end_msg = "".join([h_str, m_str, s_str])

        logger.debug("Processing %s took %s to execute", self.file_path, end_msg)

    def __get_pandoc_ast(self):
        """Convert a file to a pandoc AST

        This is usefull to apply transformations to files before converting them.
        In particular, metadata transformations can be applied.

        See `Pandoc filters <https://pandoc.org/filters.html>`_

        :param file: Path to file
        :type: str
        :return: Pandoc AST in the form of a parsed JSON
        :type: panflute.Doc
        """
        json_str = (
            convert_file(self.file_path, "json")
            if os.path.exists(self.file_path)
            else "{}"
        )
        try:
            return pf_load(StringIO(json_str))
        except JSONDecodeError:
            return pf_load(StringIO("{}"))


def __convert_files(pandoc_compose_config):
    callbacks = []
    file_paths = []
    found_files = iglob(
        os.path.join(pandoc_compose_config.destination, "**"), recursive=True
    )

    has_pandoc_compose_config_changed = __has_pandoc_compose_config_changed(
        pandoc_compose_config
    )

    for file_path in found_files:
        target_format = __find_target_format(file_path, pandoc_compose_config)
        if target_format is not None:
            file_paths.append(file_path)

            shoud_convert = __shoud_convert_file(file_path, pandoc_compose_config)
            if has_pandoc_compose_config_changed or shoud_convert:
                callbacks.append(
                    ConvertFileCallback(file_path, target_format, pandoc_compose_config)
                )
            elif not has_pandoc_compose_config_changed:
                logger.info(
                    "%s hasen't changed since last exectution; it won't be processed",
                    file_path,
                )

    if pandoc_compose_config.force:
        logger.info(
            "pandoc-compose is executing in force mode; all files will be processed"
        )
    elif len(callbacks) > 0 and has_pandoc_compose_config_changed:
        logger.info(
            "%s has changed since last process; all files will be processed",
            PandocConfig.PANDOC_COMPOSE_FILE,
        )
    elif len(file_paths) == 0:
        logger.info("No file to process found")

    with ThreadPoolExecutor(max_workers=16) as executor:
        for cb in callbacks:
            executor.submit(cb)

    # Update all SHA256 of the files
    hash_config = {
        PandocConfig.PANDOC_COMPOSE_FILE: PandocComposeConfig.get_file_hash(
            pandoc_compose_config.pandoc_config.config_file_path
        )
    }

    for file_path in file_paths:
        relative_file_path = file_path.replace(pandoc_compose_config.destination, "")
        hash_config[relative_file_path] = PandocComposeConfig.get_file_hash(file_path)

    with open(pandoc_compose_config.hash_file_path, "w") as pcf:
        cp = ConfigParser()
        # https://stackoverflow.com/questions/19359556/configparser-reads-capital-keys-and-make-them-lower-case
        cp.optionxform = str
        cp[PandocComposeConfig.HASH_DEFAULT_SECTION] = hash_config
        cp.write(pcf)
        logger.debug(
            "New file hash written in %s", pandoc_compose_config.hash_file_path
        )

    logger.info("Finished")


def __find_target_format(file_path, pandoc_compose_config):
    if not os.path.isfile(file_path):
        return None

    for item in pandoc_compose_config.pandoc_config.files:
        k, v = list(item.items())[0]
        if fnmatch(file_path, os.path.join(pandoc_compose_config.destination, k)):
            return v
    else:
        return None


def __has_pandoc_compose_config_changed(pandoc_compose_config):
    pandoc_config_computed_file_hash = pandoc_compose_config.hash_config.get(
        PandocConfig.PANDOC_COMPOSE_FILE
    )
    return (
        pandoc_config_computed_file_hash
        != pandoc_compose_config.pandoc_config_file_hash
    )


def __shoud_convert_file(file_path, pandoc_compose_config):
    if pandoc_compose_config.force:
        return True

    # File won't be converted if both it and pandoc-compose configuration haven't been modified
    # We determine that a file was nt modified by comparing it's computed SHA256 hash and
    # the one that was stored in .pandoc-compose-hash
    file_relative_path = file_path.replace(pandoc_compose_config.destination, "")
    file_hash = PandocComposeConfig.get_file_hash(file_path)

    pandoc_config_computed_file_hash = pandoc_compose_config.hash_config.get(
        file_relative_path, None
    )
    return file_hash != pandoc_config_computed_file_hash


def __check_install():
    # Check Python version
    if version_info < (3, 5):
        logger.fatal(
            "This scripts only support Python>=3.5, current version is %s", version
        )
        exit(1)

    # Checks pandoc install
    try:
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        get_pandoc_path()
    except OSError:  # TODO: handle download pandoc switch
        logger.error(
            dedent(
                """No pandoc was found: either install pandoc and add it to your PATH variable.
                See http://johnmacfarlane.net/pandoc/installing.html for installation options"""
            )
        )
        exit(1)
    finally:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

def main():
    __check_install()

    description = dedent(
        """
        Process every markdown file in a directory and convert it into PDF

        `pandoc-compose` is a wrapper around pandoc for batch processing multiple Markdown documents 
        in a directory while mutualising documents metadata in a single `{0}` file.

        Any Pandoc metadata variable (see https://pandoc.org/MANUAL.html#metadata-variables) can be set in 
        `{0}`. Every metadata variable will be incuded in every Markdown file during conversion 
        unless it is overriden in the file itself.
    """
    ).format(PandocConfig.PANDOC_COMPOSE_FILE)

    parser = ArgumentParser(description=description)

    parser.add_argument(
        "dest",
        metavar="dest",
        type=str,
        nargs="?",
        default=os.getcwd(),
        help="Destination (defaults to current directory)",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="count",
        help="Verbose mode (use -vv and -vvv to increase)",
    )

    parser.add_argument(
        "--timeout",
        "-t",
        action="store",
        help=dedent(
            """
            Sets a timeout for each file processing. 
            If a file cannot be converted after the timeout is elapsed, the convertion is aborted.
            This parameters takes a interger value in seconds by default. 'h', 'm' and 's' suffix also work.
            Examples: -t 10s, -t 1000
        """
        ),
    )

    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Forces the conversion of every file whether they've changed or not",
    )

    try:
        reminder = sys.argv.index("--")
        start = reminder + 1
        remaining = sys.argv[start:]
        sys.argv = sys.argv[:reminder]
        cli_args = parser.parse_args()
    except ValueError:
        cli_args = parser.parse_args()
        remaining = []

    try:
        __convert_files(PandocComposeConfig(cli_args, *remaining))
    except PandocComposeGenericError as pce:
        logger.error(pce.message)
        parser.print_help(sys.stderr)


if __name__ == "__main__":
    main()
