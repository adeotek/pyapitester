import os
import json

import click
import apitester.api_tester as api_tester


@click.group()
def cli():
    pass


@click.command()
@click.option('--config', default='configuration.json', help='JSON configuration file')
def apitester(config) -> None:
    api_tester.run(config)


@click.command()
@click.argument('url')
@click.option('--ssl-verify', default=True, help='SSL Verify flag')
@click.option('--output', default=None, help='Output file')
def wget(url, ssl_verify, output) -> None:
    api_tester.direct_run({
        'Group': None,
        'Name': url,
        'IsActive': True,
        'Verb': 'GET',
        'URL': url,
        'Headers': {},
        'SSLVerify': ssl_verify,
        'Payload': {},
        'Output': output
    })


@click.command()
@click.argument('url')
@click.argument('payload')
@click.option('--ssl-verify', default=True, help='SSL Verify flag')
@click.option('--output', default=None, help='Output file')
def wpost(url, payload, ssl_verify, output) -> None:
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
        'Headers': {
            'ContentType': 'application/json'
        },
        'SSLVerify': ssl_verify,
        'Payload': payload,
        'Output': output
    })


cli.add_command(apitester)
cli.add_command(wget)
cli.add_command(wpost)


if __name__ == '__main__':
    cli()
