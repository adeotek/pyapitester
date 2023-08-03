import os
from typing import List
from charset_normalizer import detect
import fileencoding.app_logger as app_logger

logger: app_logger.Logger


def convert_encoding(file, source_encoding: str, target_encoding: str) -> None:
    global logger
    try:
        with open(file, "w+b") as fp:
            fs = fp.read()
            nfs = fs.decode(source_encoding).encode(target_encoding)
            fp.write(nfs)
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
                        (target_encoding.upper(), 'magenta'))
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
    if not isinstance(req['TargetPath'], str) or req['TargetPath'] == '' or not os.path.exists(req['TargetPath']):
        logger.new_line() .clog(('Invalid target path `', 'red'), (req['TargetPath'], 'magenta'),
                                ('` provided!', 'red')).new_line()
        return
    if isinstance(req['FileExtensions'], List):
        file_extensions = req['FileExtensions']
    else:
        file_extensions = []
    if isinstance(req['SkipDirs'], List):
        skip_dirs = req['SkipDirs']
    else:
        skip_dirs = []
    check_only = isinstance(req['CheckOnly'], bool) and req['CheckOnly']
    add_bom = isinstance(req['AddBom'], bool) and req['AddBom']
    process_dir(req['TargetPath'], file_extensions, skip_dirs, add_bom, check_only)


def convert_utf8_bom(req: dict, version: str) -> None:
    global logger
    logger = app_logger.Logger(verbose=isinstance(req['Verbose'], bool) and req['Verbose'])
    logger.clog(('Starting Encoding Converter ', 'white'), ('v' + version, 'green'), (' ...', 'white')).new_line()
    convert_files_encoding(req)
