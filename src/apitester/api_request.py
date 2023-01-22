import json
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from requests import request as requests_request
from requests.exceptions import ConnectionError
import apitester.app_logger as app_logger


disable_warnings(InsecureRequestWarning)


class ApiRequest():
    __logger: app_logger.Logger
    verb: str
    url: str
    headers: dict
    sslVerify: bool
    payload = None
    response = None
    output = None

    def __init__(self, verb: str, url: str, payload = None, headers: dict = {}, output = None, sslVerify: bool = True, logger = None) -> None:
        if isinstance(logger, app_logger.Logger):
            self.__logger = logger
        else:
            self.__logger = app_logger.Logger(False)
        self.verb = verb
        self.url = url
        self.headers = headers
        self.output = output
        self.sslVerify = sslVerify
        if 'Content-Type' not in self.headers.keys():
            self.setHeader('Content-Type', 'application/json')
        if 'User-Agent' not in self.headers.keys():
            self.setHeader('User-Agent', 'Python-API-Tester')
        self.payload = payload

    def setHeader(self, key, value):
        self.headers[key] = value
        return self

    def printResponse(self) -> None:
        if self.response is None:
            self.__logger.clog(('No response!', 'red'))
            if isinstance(self.output, str) and self.output != '':
                outputFile = open(self.output, "w")
                outputFile.write('')
                outputFile.close()
        else:
            try:
                jsonOutput = self.response.json()
                output = json.dumps(jsonOutput, indent=4)
            except (ValueError, json.decoder.JSONDecodeError):
                output = self.response.text
            if isinstance(self.output, str) and self.output != '':
                outputFile = open(self.output, "w")
                outputFile.write(output)
                outputFile.close()
            else:
                self.__logger.log(output)

    def execute(self, printResponse: bool = True):
        self.__logger.cdebug(('Request ', 'yellow'), (self.verb, 'cyan'), ('(', 'yellow'), (self.url, 'cyan'), (')...', 'yellow'))
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
            self.response = requests_request(self.verb, self.url, headers=self.headers, verify=self.sslVerify, data=body)
            if self.response.status_code == 200:
                self.__logger.clog(('Response: ', 'green'), (self.verb, 'cyan'), '(', (self.url, 'cyan'), ') Status code: [', (self.response.status_code, 'green'), ']')
            else:
                self.__logger.clog(('Response: ', 'red'), (self.verb, 'cyan'), '(', (self.url, 'cyan'), ') Status code: [', (self.response.status_code, 'magenta'), ']')
        except (ValueError, ConnectionError) as err:
            self.response = None
            self.__logger.clog(('ERROR: [', 'red'), (str(err.errno), 'magenta'), ('] ' + str(err), 'red'))
        if printResponse:
            self.printResponse()
        return self

    def __getResponseCode(self) -> None:
        if self.response is None:
            return None
        else:
            return self.response.status_code
    response_code = property(__getResponseCode)
