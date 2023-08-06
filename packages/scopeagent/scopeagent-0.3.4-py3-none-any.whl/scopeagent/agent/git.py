import logging
import subprocess


logger = logging.getLogger(__name__)


def detect_git_info():
    info = {}
    try:
        info['commit'] = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()
        info['root'] = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).decode('utf-8').strip()
        info['repository'] = subprocess.check_output(['git', 'remote', 'get-url', 'origin']).decode('utf-8').strip()
        info['branch'] = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8').strip()
    except (FileNotFoundError, subprocess.CalledProcessError,):
        logger.debug("couldn't autodetect git information", exc_info=True)
    logger.debug("autodetected git info: %s", info)
    return info
