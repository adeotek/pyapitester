import os
from typing import List
from charset_normalizer import detect
from helpers.app_logger import Logger
from helpers.dict_helpers import get_dict_attr, get_dict_bool, get_dict_list

logger: Logger


def convert_encoding(file, source_encoding: str, target_encoding: str) -> None:
    global logger
    try:
        with open(file, mode="r", encoding=source_encoding) as sfp:
            data = sfp.read()
        with open(file, mode="w", encoding=target_encoding) as fp:
            fp.write(data)
        logger.clog((file, 'cyan'), ': ', (source_encoding.upper(), 'yellow'), (' -> ', 'magenta'),
                    (target_encoding.upper(), 'magenta'), (' OK', 'green'))
    except (ValueError, UnicodeError, UnicodeDecodeError, UnicodeEncodeError) as error:
        logger.clog((file, 'cyan'), ': ', (source_encoding.upper(), 'yellow'), (' -> ', 'magenta'),
                    (target_encoding.upper(), 'magenta'), (' ERROR', 'red'))
        logger.cdebug(('Error: [', 'red'), (str(error.errno), 'magenta'), ('] ' + str(error), 'yellow'))


def process_file(file, add_bom: bool = False, check_only: bool = False) -> None:
    global logger
    with open(file, "r+b") as fp:
        fs = fp.read()
        file_encoding = '' if detect(fs)['encoding'] is None else detect(fs)['encoding'].lower()

    if add_bom:
        skip = file_encoding == 'utf-8-sig'
        source_encoding = 'utf-8'
        target_encoding = 'utf-8-sig'
    else:
        skip = file_encoding != 'utf-8-sig'
        source_encoding = 'utf-8-sig'
        target_encoding = 'utf-8'

    if skip:
        logger.cdebug((file, 'cyan'), ': ', (target_encoding.upper(), 'green'), ' [', file_encoding.upper(), ']',
                      (' -> ', 'magenta'), 'SKIPPED')
    else:
        if check_only:
            logger.clog((file, 'cyan'), ': ', (source_encoding.upper(), 'yellow'), (' -> ', 'magenta'),
                        (target_encoding.upper(), 'magenta'), ' - NOT CHANGED')
        else:
            convert_encoding(file, source_encoding, target_encoding)


def process_dir(path, file_extensions: List[str] = (), skip_dirs: List[str] = (),
                add_bom: bool = False, check_only: bool = False) -> None:
    global logger
    for item_name in os.listdir(path):
        item = os.path.join(path, item_name)
        if os.path.isdir(item):
            if len(skip_dirs) == 0 or item_name not in skip_dirs:
                process_dir(item, file_extensions, skip_dirs, add_bom, check_only)
            else:
                logger.cdebug('Directory: ', (item, 'cyan'), (' -> ', 'magenta'), 'SKIPPED')
        else:
            _, ext = os.path.splitext(item_name)
            if len(file_extensions) == 0 or ext in file_extensions:
                process_file(item, add_bom, check_only)
            else:
                logger.cdebug('File: ', (item, 'cyan'), (' -> ', 'magenta'), 'SKIPPED')


def convert_files_encoding(req: dict) -> None:
    global logger
    target_path = get_dict_attr(req, 'TargetPath')
    if not isinstance(target_path, str) or target_path == '' or not os.path.exists(target_path):
        logger.new_line() .clog(('Invalid target path `', 'red'), (target_path, 'magenta'),
                                ('` provided!', 'red')).new_line()
        return
    process_dir(target_path, get_dict_list(req, 'FileExtensions'), get_dict_list(req, 'SkipDirs'),
                get_dict_bool(req, 'AddBom'), get_dict_bool(req, 'CheckOnly'))


def convert_utf8_bom(req: dict, version: str) -> None:
    global logger
    logger = Logger(verbose=get_dict_bool(req, 'Verbose'))
    logger.clog(('Starting Encoding Converter ', 'white'), ('v' + version, 'green'), (' ...', 'white')).new_line()
    convert_files_encoding(req)
