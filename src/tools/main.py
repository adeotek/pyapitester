import os
import json

import click
from . import __version__
from tools.custom_decorators import add_version
import apitester.api_tester
import fileencoding.file_encoding


@click.group()
@click.version_option(__version__, '-v', '--version', message="%(prog)s, version %(version)s")
@click.pass_context
@add_version
def cli(ctx):
    pass


@click.command()
@click.option('--config', default='configuration.json', help='JSON configuration file')
def apitester(config) -> None:
    apitester.api_tester.run(config, version=__version__)


@click.command()
@click.argument('url')
@click.option('--headers', default=None, help='HTTP Headers')
@click.option('--ssl-verify', default=True, help='SSL Verify flag')
@click.option('--output', default=None, help='Output file')
def wget(url, headers, ssl_verify, output) -> None:
    apitester.api_tester.direct_run({
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
def wpost(url, payload, headers, ssl_verify, output) -> None:
    if os.path.exists(payload):
        payload_file = open(payload)
        payload = json.load(payload_file)
        payload_file.close()
    apitester.api_tester.direct_run({
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
def wcall(verb, url, payload, headers, ssl_verify, output) -> None:
    if payload:
        if os.path.exists(payload):
            payload_file = open(payload)
            payload = json.load(payload_file)
            payload_file.close()
    else:
        payload = {}
    apitester.api_tester.direct_run({
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


@click.command()
@click.argument('target-path')
@click.option('--file-extensions', default=None, help='Include only files with these extensions (coma-separated list)')
@click.option('--exclude-dirs', default=None, help='Exclude sub-directories (coma-separated list)')
@click.option('--check-only', is_flag=True, default=False, help="Don't change anything, just check  (flag)")
@click.option('--add-bom', is_flag=True, default=False, help='Add BOM instead removing it (flag)')
@click.option('--verbose', '-v', is_flag=True, default=False, help='Verbose mode (flag)')
def utf8bom(target_path: str, file_extensions, exclude_dirs, check_only: bool, add_bom: bool, verbose: bool) -> None:
    file_extensions_list = []
    exclude_dirs_list = []
    if isinstance(file_extensions, str) and file_extensions != '':
        for ext in file_extensions.split(','):
            if isinstance(ext, str) and ext != '' and ext.strip('* ').startswith('.'):
                file_extensions_list.append(ext.strip('* '))
    if isinstance(exclude_dirs, str) and exclude_dirs != '':
        for sub_dir in exclude_dirs.split(','):
            if isinstance(sub_dir, str) and sub_dir.strip(' ') != '':
                exclude_dirs_list.append(sub_dir.strip(' '))
    fileencoding.file_encoding.convert_utf8_bom({
        'TargetPath': target_path,
        'FileExtensions': file_extensions_list,
        'ExcludeDirs': exclude_dirs_list,
        'CheckOnly': check_only,
        'AddBom': add_bom,
        'Verbose': verbose
    }, version=__version__)


cli.add_command(apitester)
cli.add_command(wget)
cli.add_command(wpost)
cli.add_command(wcall)
cli.add_command(utf8bom)


if __name__ == '__main__':
    cli()
