import logging
import src
from src.config import get_config

config = get_config()
_LOGGER = logging.getLogger(__name__)


def main():
    _LOGGER.debug("here goes.")
    print(config)


if __name__ == '__main__':
    _LOGGER.debug('Starting')
    main()
