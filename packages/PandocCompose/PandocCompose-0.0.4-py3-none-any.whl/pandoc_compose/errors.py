from textwrap import dedent


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
