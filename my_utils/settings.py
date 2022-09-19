import configparser

from my_log import LOG
from my_utils import SETTINGS_INI_FILE


def get_settings(section: str, key: str):
    """
    Gets a configuration parameter from the settings.ini file.
    :param section: the section name
    :param key: the key of the parameter
    :return: The value if the key exists, otherwise - None
    """
    try:
        config = configparser.ConfigParser()
        config.read(SETTINGS_INI_FILE)
        ret = config[section][key]
        # LOG.debug(f'get_settings [{section}][{key}] : {ret}')
    except Exception as e:
        LOG.exception(f'get_settings [{section}][{key}] : {e}')
        ret = None
    return ret


def get_hostname():
    """
    Get the hostname or IP address
    """
    ret = get_settings('Service', 'hostname')
    return ret.encode('utf-8')


def get_authkey():
    """
    Get the authkey
    """
    ret = get_settings('Service', 'authkey')
    return ret.encode('utf-8')


def get_internal_port():
    """
    Get the port of the internal connection
    """
    try:
        ret = int(get_settings('Service', 'internal_port'))
    except Exception:
        ret = 54321
    return ret


def get_github_token():
    """
    Get GitHub token
    """
    try:
        ret = get_settings('GitHub', 'token')
    except Exception:
        ret = 'momo'
    return ret
