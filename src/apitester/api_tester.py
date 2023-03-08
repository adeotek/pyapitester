import os
import json
import apitester._version as _version
import apitester.custom_auth_token as custom_auth_token
import apitester.app_logger as app_logger
import apitester.api_request as api_request

logger: app_logger.Logger
configuration: dict


def get_dict_attr(data: dict, key: str, default=None):
    if key in data.keys():
        return data[key]
    else:
        return default


def get_full_path(input_path: str) -> str:
    if os.path.isabs(input_path):
        return input_path
    else:
        return os.path.join(os.getcwd(), input_path)


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
        logger = app_logger.Logger()
        logger.new_line()\
            .clog(('No `', 'red'), ('configuration.json', 'magenta'), ('` file provided!', 'red')).new_line()
        return False
    config_file = open(config_file_name)
    configuration = json.load(config_file)
    config_file.close()
    # initialize logger
    logger = app_logger.Logger(configuration['Verbose'])
    return True


def run(config) -> None:
    global logger, configuration
    print('Starting API tester v', _version.__version__, ' ...', sep='')
    if init(config):
        for req in configuration['Requests']:
            if get_dict_attr(req, 'IsActive', True):
                logger.new_line().clog(*get_request_title(req))
                execute_request(req)
    logger.new_line().clog(('DONE!', 'green'))


def direct_run(req: dict) -> None:
    global logger
    print('Starting API tester v', _version.__version__, ' ...', sep='')
    logger = app_logger.Logger()
    execute_request(req)


if __name__ == '__main__':
    run('configuration.json')
