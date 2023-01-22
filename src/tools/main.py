import click
import apitester.api_tester as api_tester


@click.group()
def cli():
    pass


@click.command()
@click.option('--config', default='configuration.json', help='JSON configuration file')
def apitester(config) -> None:
    api_tester.run(config)


cli.add_command(apitester)


if __name__ == '__main__':
    cli()
