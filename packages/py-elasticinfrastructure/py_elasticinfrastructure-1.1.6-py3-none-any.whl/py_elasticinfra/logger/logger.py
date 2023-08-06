import logging
import logging.config
from pathlib import Path
from py_elasticinfra.utils.json import read_json


class Logger:
    def __init__(self):
        pass

    def config_py_logger(self,
                         log_dir,
                         log_config="py_elasticinfra/logger/py_logger.json",
                         log_levels={
                             0: logging.WARNING,
                             2: logging.DEBUG,
                             3: logging.ERROR
                         },
                         default_level=logging.ERROR):
        log_config = Path(log_config)
        if log_config.is_file():
            config = read_json(log_config)
            for _, handler in config["handlers"].items():
                if "filename" in handler:
                    handler["filename"] = str(log_dir / handler['filename'])
            logging.config.dictConfig(config)
        else:
            print("Warning: logging configuration "
                  "file is not found in {}.".format(log_config))
            logging.basicConfig(level=default_level)

        self.configure_es_logger(default_level)
        self.log_levels = log_levels
        self.log_dir = log_dir

    def get_py_logger(self, name, verbosity):
        msg_verbosity = "verbosity option {} is invalid. Valid options are {}.".format(
            verbosity, self.log_levels.keys())
        assert verbosity in self.log_levels, msg_verbosity
        logger = logging.getLogger(name)
        logger.setLevel(self.log_levels[verbosity])
        return logger

    def configure_es_logger(self, default_level):
        es_logger = logging.getLogger('elasticsearch')
        es_logger.setLevel(default_level)
