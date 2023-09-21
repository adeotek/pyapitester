import os
import json
from helpers.app_logger import Logger
from helpers.path_helpers import get_full_path
from helpers.dict_helpers import get_dict_attr
import apitester.custom_auth_token as custom_auth_token
import apitester.api_request as api_request

logger: Logger
configuration: dict


def get_request_title(req: dict) -> tuple:
    title = ['-']
    group = get_dict_attr(req, 'Group', '')
    if group != '':
        title.append(' [')
        title.append((group, 'blue'))
        title.append('] ')
    name = get_dict_attr(req, 'Name', '')
    if name != '':
        title.append((' ' + name, 'magenta'))
    else:
        title.append(('----', 'magenta'))
    return tuple(title)


def execute_request(req: dict) -> None:
    global logger
    if req['Verb'] not in ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']:
        logger.new_line() \
            .clog(('Invalid verb `', 'red'), (req['Verb'], 'magenta'), ('` provided!', 'red')).new_line()
        return
    if 'Output' in req.keys() and isinstance(req['Output'], str) and req['Output'] != '':
        output_file_name = get_full_path(req['Output'])
    else:
        output_file_name = None
    request = api_request.ApiRequest(
        verb=req['Verb'],
        url=req['URL'],
        headers=get_dict_attr(req, 'Headers', {}),
        output=output_file_name,
        ssl_verify=get_dict_attr(req, 'SSLVerify', True),
        payload=get_dict_attr(req, 'Payload'),
        logger=logger)
    if get_dict_attr(req, 'UseCustomAuthToken', False):
        token, expires_at = custom_auth_token.generate_token(req['CustomAuthToken']['SecretKey'],
                                                             req['CustomAuthToken']['ClientId'],
                                                             req['CustomAuthToken']['ServerId'])
        logger.cdebug('Generated Auth Token will expire at: ', (str(expires_at), 'cyan'))
        request.set_header('Authorization', 'Bearer ' + str(token))
    request.execute(True)


def init(config) -> bool:
    global logger, configuration
    # load configuration
    config_file_name = get_full_path(config)
    if not os.path.exists(config_file_name):
        logger = Logger()
        logger.new_line()\
            .clog(('No `', 'red'), ('configuration.json', 'magenta'), ('` file provided!', 'red')).new_line()
        return False
    config_file = open(config_file_name)
    configuration = json.load(config_file)
    config_file.close()
    # initialize logger
    logger = Logger(configuration['Verbose'])
    return True


def run(config, version: str) -> None:
    global logger, configuration
    if not init(config):
        return
    logger.clog(('Starting API tester ', 'white'), ('v' + version, 'green'), (' ...', 'white')).new_line()
    for req in configuration['Requests']:
        if get_dict_attr(req, 'IsActive', True):
            logger.new_line().clog(*get_request_title(req))
            execute_request(req)
    logger.new_line().clog(('DONE!', 'green'))


def direct_run(req: dict, version: str) -> None:
    global logger
    logger = Logger()
    logger.clog(('Starting API tester ', 'white'), ('v' + version, 'green'), (' ...', 'white')).new_line()
    execute_request(req)


if __name__ == '__main__':
    run('configuration.json', 'N/A')
