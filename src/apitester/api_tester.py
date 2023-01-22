import os
import json
import apitester._version as _version
import apitester.custom_auth_token as custom_auth_token
import apitester.app_logger as app_logger
import apitester.api_request as api_request


logger: app_logger.Logger
configuration: dict


def get_dict_attr(data: dict, key: str, default = None):
    if key in data.keys():
        return data[key]
    else:
        return default


def get_full_path(input: str) -> bool:
    if os.path.isabs(input):
        return input
    else:
        return os.path.join(os.getcwd(), input)


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
    if 'Output' in req.keys() and isinstance(req['Output'], str) and req['Output'] != '':
        outputFileName = get_full_path(req['Output'])
    else:
        outputFileName = None
    request = api_request.ApiRequest(
        verb=req['Verb'],
        url=req['URL'],
        headers=get_dict_attr(req, 'Headers', {}),
        output=outputFileName,
        sslVerify=get_dict_attr(req, 'SSLVerify', True),
        payload=get_dict_attr(req, 'Payload'),
        logger=logger)
    if get_dict_attr(req, 'UseCustomAuthToken', False):
        token, expiresAt = custom_auth_token.generate_token(req['CustomAuthToken']['SecretKey'], req['CustomAuthToken']['ClientId'], req['CustomAuthToken']['ServerId'])
        logger.cdebug('Generated Auth Token will expire at: ', (str(expiresAt), 'cyan'))
        request.setHeader('Authorization', 'Bearer ' + str(token))
    request.execute(True)


def init(config) -> bool:
    global logger, configuration
    # load configuration
    configFileName = get_full_path(config)
    if not os.path.exists(configFileName):
        logger.newLine().clog(('No `', 'red'), ('configuration.json', 'magenta'), ('` file provided!', 'red')).newLine()
        return False
    configFile = open(configFileName)
    configuration = json.load(configFile)
    configFile.close()
    # initialize logger
    logger = app_logger.Logger(configuration['Verbose'])
    return True


def run(config) -> None:
    global logger, configuration
    print('Starting API tester v', _version.__version__, '...')
    if init(config):
        for req in configuration['Requests']:
            if get_dict_attr(req, 'IsActive', True):
                logger.newLine().clog(*get_request_title(req))
                execute_request(req)
    logger.newLine().clog(('DONE!', 'green'))


if __name__ == '__main__':
    run('configuration.json')
