import os
from json import dumps as json_dumps

from deepmerge import always_merger

from pandoc_compose.utils import logger, KNOWN_TARGET_FORMATS, KNOWN_SOURCE_FORMATS


class PandocConfig:
    PANDOC_COMPOSE_FILE = "pandoc-compose.yml"
    POSSIBLE_OVERRIDES_IN_MD = ["pandoc_options"]

    def __init__(self, config_file_path, original_config, merging=False):
        self.config_file_path = config_file_path
        self.__original_config = original_config.copy()
        # When merging two config, we expect files have already been processed
        # so files section in original config should be correct
        if not merging:
            self.__process_files_section()

    @property
    def files(self):
        return self.__original_config.get("files")

    @files.setter
    def files(self, value):
        self.__original_config["files"] = value

    @property
    def pandoc(self):
        return self.__original_config.get("pandoc", {})

    @property
    def pandoc_options(self):
        return self.__original_config.get("pandoc_options", {})

    def merge(self, config_override):
        new_config = always_merger.merge(self.__original_config.copy(), config_override)
        return PandocConfig(self.config_file_path, new_config, merging=True)

    def __process_files_section(self):
        fallback_msg = 'Falling back to default [{"**/*.md": {"from": "markdown", "to": "pdf"}}]'
        files = self.files
        if not isinstance(files, list) or len(files) == 0:
            logger.debug("`files` section is empty, %s", fallback_msg)
            self.files = self.__default_files_list()
            return

        # noinspection PyBroadException
        try:
            new_files = []
            for file in files:
                glob, formats = list(file.items())[0]
                source_format = None  # Will be autodetected
                target_format = "pdf"
                if isinstance(formats, str):
                    target_format = formats
                elif isinstance(formats, dict):
                    source_format = formats["from"]
                    target_format = formats["to"]
                err_msg = "%s is currently not a supported %s format; entry %s will be ignored"
                if KNOWN_TARGET_FORMATS.get(target_format) is None:
                    logger.warning(err_msg, target_format, "output", glob)
                elif source_format is not None and source_format not in KNOWN_SOURCE_FORMATS:
                    logger.warning(err_msg, source_format, "input", glob)
                else:
                    new_files.append({glob: {"from": source_format, "to": target_format}})
            if len(new_files) == 0:
                logger.warning("No valid item found `files` section of %s; %s", self.config_file_path, fallback_msg)
                self.files = self.__default_files_list()
            else:
                self.files = new_files
        except Exception:
            logger.warning("`files` section is malformed; %s", self.config_file_path, fallback_msg)
            self.files = self.__default_files_list()

    @staticmethod
    def __default_files_list():
        return [{"**/*.md": {"from": "markdown", "to": "pdf"}}]

    def __str__(self):
        return json_dumps(self.__original_config, indent=4, sort_keys=True, ensure_ascii=False)

    @staticmethod
    def get_config_file_path(dest):
        return os.path.join(dest, PandocConfig.PANDOC_COMPOSE_FILE)
