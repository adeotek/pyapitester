import os
import json

import click
from . import __version__
from tools.custom_decorators import add_version
import apitester.api_tester as api_tester


@click.group()
@click.version_option(__version__, '-v', '--version', message="%(prog)s, version %(version)s")
@click.pass_context
@add_version
def cli(ctx):
    pass


@click.command()
@click.option('--config', default='configuration.json', help='JSON configuration file')
@add_version
def apitester(config) -> None:
    api_tester.run(config, version=__version__)


@click.command()
@click.argument('url')
@click.option('--headers', default=None, help='HTTP Headers')
@click.option('--ssl-verify', default=True, help='SSL Verify flag')
@click.option('--output', default=None, help='Output file')
@add_version
def wget(url, headers, ssl_verify, output) -> None:
    api_tester.direct_run({
        'Group': None,
        'Name': url,
        'IsActive': True,
        'Verb': 'GET',
        'URL': url,
        'Headers': headers or {},
        'SSLVerify': ssl_verify,
        'Payload': {},
        'Output': output
    }, version=__version__)


@click.command()
@click.argument('url')
@click.argument('payload')
@click.option('--headers', default=None, help='HTTP Headers')
@click.option('--ssl-verify', default=True, help='SSL Verify flag')
@click.option('--output', default=None, help='Output file')
@add_version
def wpost(url, payload, headers, ssl_verify, output) -> None:
    if os.path.exists(payload):
        payload_file = open(payload)
        payload = json.load(payload_file)
        payload_file.close()
    api_tester.direct_run({
        'Group': None,
        'Name': url,
        'IsActive': True,
        'Verb': 'POST',
        'URL': url,
        'Headers': headers or {'ContentType': 'application/json'},
        'SSLVerify': ssl_verify,
        'Payload': payload,
        'Output': output
    }, version=__version__)


@click.command()
@click.argument('verb')
@click.argument('url')
@click.option('--payload', default=None, help='HTTP payload')
@click.option('--headers', default=None, help='HTTP Headers')
@click.option('--ssl-verify', default=True, help='SSL Verify flag')
@click.option('--output', default=None, help='Output file')
@add_version
def wcall(verb, url, payload, headers, ssl_verify, output) -> None:
    if payload:
        if os.path.exists(payload):
            payload_file = open(payload)
            payload = json.load(payload_file)
            payload_file.close()
    else:
        payload = {}
    api_tester.direct_run({
        'Group': None,
        'Name': url,
        'IsActive': True,
        'Verb': verb.upper(),
        'URL': url,
        'Headers': headers or {'ContentType': 'application/json'},
        'SSLVerify': ssl_verify,
        'Payload': payload,
        'Output': output
    }, version=__version__)


cli.add_command(apitester)
cli.add_command(wget)
cli.add_command(wpost)
cli.add_command(wcall)


if __name__ == '__main__':
    cli()
