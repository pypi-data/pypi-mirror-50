import click
import click_config_file
import requests

__API_URL_BASE = 'http://api.wolframalpha.com/v1/result'


@click.command()
@click.argument('query', nargs=-1)
@click.option('--appid', '-a', required=True)
@click.option('--units', '-u', type=click.Choice(['metric', 'imperial']), default='metric', show_default=True)
@click.option('--timeout', '-t', type=int, default=5, show_default=True)
@click_config_file.configuration_option(show_default=True)
def wat(query, appid, units, timeout):
    query_string = " ".join(query)
    payload = {'appid': appid, 'units': units, 'timeout': timeout, 'i': query_string}
    response = requests.get(__API_URL_BASE, params=payload)
    click.echo(response.text)


if __name__ == '__main__':
    wat()
