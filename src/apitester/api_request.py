import json
from typing import Optional

from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from requests import request as requests_request
from requests.exceptions import ConnectionError
import apitester.app_logger as app_logger

disable_warnings(InsecureRequestWarning)


class ApiRequest:
    __logger: app_logger.Logger
    verb: str
    url: str
    headers: dict
    sslVerify: bool
    payload = None
    response = None
    output = None

    def __init__(self, verb: str, url: str, payload=None, headers=None, output=None, ssl_verify: bool = True,
                 logger=None) -> None:
        if headers is None:
            headers = {}
        if isinstance(logger, app_logger.Logger):
            self.__logger = logger
        else:
            self.__logger = app_logger.Logger(False)
        self.verb = verb
        self.url = url
        self.headers = headers
        self.output = output
        self.sslVerify = ssl_verify
        if 'Content-Type' not in self.headers.keys():
            self.set_header('Content-Type', 'application/json')
        if 'User-Agent' not in self.headers.keys():
            self.set_header('User-Agent', 'Python-API-Tester')
        self.payload = payload

    def set_header(self, key, value):
        self.headers[key] = value
        return self

    def print_response(self) -> None:
        if self.response is None:
            self.__logger.clog(('No response!', 'red'))
            if isinstance(self.output, str) and self.output != '':
                output_file = open(self.output, "w")
                output_file.write('')
                output_file.close()
        else:
            try:
                json_output = self.response.json()
                output = json.dumps(json_output, indent=4)
            except (ValueError, json.decoder.JSONDecodeError):
                output = self.response.text
            if isinstance(self.output, str) and self.output != '':
                output_file = open(self.output, "w")
                output_file.write(output)
                output_file.close()
            else:
                self.__logger.log(output)

    def execute(self, print_response: bool = True):
        self.__logger.cdebug(('Request ', 'yellow'), (self.verb, 'cyan'), ('(', 'yellow'), (self.url, 'cyan'),
                             (')...', 'yellow'))
        self.__logger.cdebug(('Headers:', 'yellow'), (json.dumps(self.headers, indent=4), 'cyan'))
        if self.verb == "GET":
            body = None
        else:
            if isinstance(self.payload, str):
                body = self.payload
                self.__logger.cdebug(('Body:', 'yellow'), (self.payload, 'cyan'))
            else:
                body = json.dumps(self.payload)
                self.__logger.cdebug(('Body:', 'yellow'), (json.dumps(self.payload, indent=4), 'cyan'))
        try:
            self.response = requests_request(self.verb, self.url, headers=self.headers, verify=self.sslVerify,
                                             data=body)
            if self.response.status_code == 200:
                self.__logger.clog(('Response: ', 'green'), (self.verb, 'cyan'), '(', (self.url, 'cyan'),
                                   ') Status code: [', (self.response.status_code, 'green'), ']')
            else:
                self.__logger.clog(('Response: ', 'red'), (self.verb, 'cyan'), '(', (self.url, 'cyan'),
                                   ') Status code: [', (self.response.status_code, 'magenta'), ']')
        except (ValueError, ConnectionError) as err:
            self.response = None
            self.__logger.clog(('ERROR: [', 'red'), (str(err.errno), 'magenta'), ('] ' + str(err), 'red'))
        if print_response:
            self.print_response()
        return self

    def __get_response_code(self) -> Optional[int]:
        if self.response is None:
            return None
        else:
            return self.response.status_code

    response_code = property(__get_response_code)
