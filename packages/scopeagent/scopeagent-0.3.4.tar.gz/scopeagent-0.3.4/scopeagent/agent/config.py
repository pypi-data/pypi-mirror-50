import json
import logging
from os.path import expanduser

SCOPE_CONFIG_PATH = expanduser("~/.scope/config.json")
logger = logging.getLogger(__name__)


def load_config_file(path=SCOPE_CONFIG_PATH):
    """Attempts to read the API endpoint and API key from the native Scope app configuration file.

    :returns a tuple with (API endpoint, API key) if the configuration file exists, (None, None) otherwise
    :rtype (string, string)
    """
    with open(str(path), 'r') as config_file:
        config = json.load(config_file)
        try:
            profile = config['profiles'][config['currentProfile']]
            logger.debug("autodetected config profile: %s", profile)
            return profile['apiEndpoint'], profile['apiKey']
        except KeyError:
            raise Exception("Invalid format in Scope configuration file at %s" % path)
