import os
import sys
import logging
import configparser


class TraceLog:
    default_level = 'INFO'

    def __init__(self, path=__name__, file_name='file'):
        # Set default log level:
        level = self.get_log_level()

        # Create a logger:
        if sys.platform == 'win32':
            self._f_handler = logging.StreamHandler(sys.stdout)
        else:
            # Creating file if not exists
            if not os.path.exists(path) and not os.path.islink(path):
                os.makedirs(path)

            full_path = f'{path}/{file_name}.log'
            self._f_handler = logging.FileHandler(full_path)

        self._f_handler.setLevel(level)
        logging.root.setLevel(level)  # fix when level info or debug, logging not working

        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)-08s - %(message)s')
        self._f_handler.setFormatter(f_format)

        # Set logger parameters:
        self._logger = logging.getLogger(file_name)
        self._logger.addHandler(self._f_handler)

    def get_log_level(self):
        try:
            from my_utils import SETTINGS_INI_FILE

            # LOG_SETTINGS_INI_FILE = 'settings.ini'

            config = configparser.ConfigParser()
            # config.read(LOG_SETTINGS_INI_FILE)
            config.read(SETTINGS_INI_FILE)
            level = config['DEFAULT']['log_level']
        except KeyError:
            level = None

        if not level:
            level = self.default_level

        return level

    def info(self, msg):
        return self._logger.info(msg)

    def warning(self, msg):
        return self._logger.warning(msg)

    def error(self, msg):
        return self._logger.error(msg)

    def exception(self, msg):
        return self._logger.exception(msg)

    def debug(self, msg):
        return self._logger.debug(msg)

    def critical(self, msg):
        return self._logger.critical(msg)


if __name__ == '__main__':
    LOG = TraceLog('/root', 'nova')

    LOG.info('sami')
