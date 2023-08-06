from gevent import monkey  # isort:skip

monkey.patch_all()  # noqa

import logging
import sys
from pathlib import Path

from appdirs import user_config_dir, user_data_dir
from huey.contrib.minimal import MiniHuey

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

CONFIG_DIR = Path(user_config_dir('chitanda', 'dazuling'))
DATA_DIR = Path(user_data_dir('chitanda', 'dazuling'))

huey = MiniHuey()
