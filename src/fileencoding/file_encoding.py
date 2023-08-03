import os
from typing import List
from charset_normalizer import detect
import fileencoding.app_logger as app_logger

logger = app_logger.Logger()


def convert_encoding(data, source_encoding: str, target_encoding: str, verbose: bool = False):
    try:
        decoded_data = data.decode(source_encoding)
        new_data = decoded_data.encode(target_encoding)
        success = True
    except (ValueError, UnicodeError, UnicodeDecodeError, UnicodeEncodeError) as error:
        success = False
        new_data = None
        if verbose:
            print(str(error))
    return success, new_data


def process_file(file, add_bom: bool = False, check_only: bool = False, verbose: bool = False) -> None:
    with open(file, "r+b") as fp:
        fs = fp.read()
        result = detect(fs)
        skip = True
        if add_bom and result['encoding'] != 'UTF-8-SIG':
            skip = False
            print(file, ':', result['encoding'], '->', 'UTF-8-SIG')
            if not check_only:
                success, nfs = convert_encoding(fs, 'utf-8', 'utf-8-sig', verbose) 
                if success:
                    fp.write(nfs)
                else:
                    print('')
        if not add_bom and result['encoding'] == 'UTF-8-SIG':
            skip = False
            print(file, ':', result['encoding'], '->', 'UTF-8')
            if not check_only:
                success, nfs = convert_encoding(fs, 'utf-8-sig', 'utf-8', verbose)
                if success:
                    fp.write(nfs)
                else:
                    print('')
        if skip and verbose:
            print('SKIPPED', file, '->', result['encoding'])


def process_dir(path,
                include_exts: List[str] = (),
                exclude_dir: List[str] = (),
                add_bom: bool = False,
                check_only: bool = False,
                verbose: bool = False) -> None:
    for item_name in os.listdir(path):
        item = os.path.join(path, item_name)
        if os.path.isdir(item):
            if len(exclude_dir) == 0 or item_name not in exclude_dir:
                process_dir(item, include_exts, exclude_dir, add_bom, check_only, verbose)
            else:
                if verbose:
                    print('SKIPPED Directory:', item)
        else:
            _, ext = os.path.splitext(item_name)
            if len(include_exts) == 0 or ext in include_exts:
                process_file(item, add_bom, check_only, verbose)
            else:
                if verbose:
                    print('SKIPPED File:', item)


def convert_files_encoding(req: dict) -> None:
    global logger
    if not isinstance(req['TargetPath'], str) or req['TargetPath'] == '' or not os.path.exists(req['TargetPath']):
        logger.new_line() \
            .clog(('Invalid target path `', 'red'), (req['TargetPath'], 'magenta'), ('` provided!', 'red')).new_line()
        return
    if isinstance(req['FileExtensions'], List):
        include_ext = req['FileExtensions']
    else:
        include_ext = []
    if isinstance(req['ExcludeDirs'], List):
        exclude_dir = req['ExcludeDirs']
    else:
        exclude_dir = []
    check_only = isinstance(req['CheckOnly'], bool) and req['CheckOnly']
    add_bom = isinstance(req['AddBom'], bool) and req['AddBom']
    verbose = isinstance(req['Verbose'], bool) and req['Verbose']
    process_dir(req['TargetPath'], include_ext, exclude_dir, add_bom, check_only, verbose)


def convert_utf8_bom(req: dict, version: str) -> None:
    global logger
    logger = app_logger.Logger()
    logger.clog(('Starting Encoding Converter ', 'white'), ('v' + version, 'green'), (' ...', 'white')).new_line()
    convert_files_encoding(req)
