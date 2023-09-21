import os
from typing import List
from helpers.app_logger import Logger
from helpers.dict_helpers import get_dict_attr, get_dict_bool, get_dict_list

logger: Logger


def run_action(action: dict, version: str) -> None:
    global logger
    logger = Logger(verbose=get_dict_bool(action, 'Verbose'))
    logger.clog(('Starting Docker Container action ', 'white'), ('v' + version, 'green'), (' ...', 'white')).new_line()
    # convert_files_encoding(req)
