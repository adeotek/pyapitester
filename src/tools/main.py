import os
import json

import click
from . import __version__
from tools.custom_decorators import add_version
import apitester.api_tester
import fileencoding.file_encoding
import dockertools.docker_containers


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
@click.option('--add-bom', '-a', is_flag=True, default=False, help='Add BOM (flag)')
@click.option('--remove-bom', '-r', is_flag=True, default=False, help='Remove BOM (flag)')
@click.option('--file-extensions', '-f', default=None,
              help='Include only files with these extensions (coma-separated list)')
@click.option('--skip-dirs', '-s', default=None, help='Skip sub-directories (coma-separated list)')
@click.option('--check-only', '-c', is_flag=True, default=False,
              help='Check only, do not change anything (flag)')
@click.option('--verbose', '-v', is_flag=True, default=False, help='Verbose mode (flag)')
def utf8bom(target_path: str, add_bom: bool, remove_bom: bool, file_extensions, skip_dirs,
            check_only: bool, verbose: bool) -> None:
    file_extensions_list = []
    skip_dirs_list = []
    if isinstance(file_extensions, str) and file_extensions != '':
        for ext in file_extensions.split(','):
            if isinstance(ext, str) and ext != '' and ext.strip('* ').startswith('.'):
                file_extensions_list.append(ext.strip('* '))
    if isinstance(skip_dirs, str) and skip_dirs != '':
        for sub_dir in skip_dirs.split(','):
            if isinstance(sub_dir, str) and sub_dir.strip(' ') != '':
                skip_dirs_list.append(sub_dir.strip(' '))
    fileencoding.file_encoding.convert_utf8_bom({
        'TargetPath': target_path,
        'FileExtensions': file_extensions_list,
        'SkipDirs': skip_dirs_list,
        'CheckOnly': check_only or (not add_bom and not remove_bom) or (add_bom and remove_bom),
        'AddBom': add_bom and not remove_bom,
        'Verbose': verbose
    }, version=__version__)


@click.command()
@click.argument('image')
@click.option('--dry-run', is_flag=True, default=False,
              help='Do not change anything, just print the actions to be taken (flag)')
@click.option('--verbose', '-v', is_flag=True, default=False, help='Verbose mode (flag)')
def dockerct(image: str, 
            dry_run: bool, verbose: bool) -> None:
    
    dockertools.docker_containers.run_action({
        'Image': image,
        'DryRun': dry_run,
        'Verbose': verbose
    }, version=__version__)


cli.add_command(apitester)
cli.add_command(wget)
cli.add_command(wpost)
cli.add_command(wcall)
cli.add_command(utf8bom)
cli.add_command(dockerct)


if __name__ == '__main__':
    cli()
