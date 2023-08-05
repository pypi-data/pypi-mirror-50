"""
Simple cli that interfaces https://emojipedia.org
"""
from bs4 import BeautifulSoup
import click
import clipboard
import logging
import requests
import sys

logger = logging.getLogger(__name__)


def search(search_phrase):
    search_url = 'https://emojipedia.org/search/?q=' \
            + requests.utils.requote_uri(search_phrase)
    search = requests.get(search_url)
    soup = BeautifulSoup(search.content, 'html.parser')
    search_results = soup.findAll("ol", {"class": "search-results"})
    return search_results[0]


def add_options(options:list):
    "Aggregate click options from a list and pass as single decorator."
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options

_search_options = [
    click.argument('search_phrase', nargs=-1, type=click.UNPROCESSED)
        ]

@click.group()
@click.pass_context
def cli(ctx, **kwargs):
    logging.basicConfig(
        format = '%(asctime)s.%(msecs)03d, %(levelname)s: %(message)s',
        datefmt = '%Y-%m-%d %H:%M:%S',
        filename = None,
        level = logging.DEBUG if ctx.params.get('debug') else logging.WARNING,
        )
    

@cli.command()
@add_options(_search_options)
def find(search_phrase):
    '''Search for phrase in clipboard or arguments and print results.'''
    search_results = search(' '.join(search_phrase))
    print(search_results.get_text())

@cli.command()
@add_options(_search_options)
def clip(search_phrase):
    '''Search clipboard or arguments and put first result back in clipboard and print it.'''
    search_result = ""
    if len(search_phrase):
        search_result = search(' '.join(search_phrase))
    else:
        search_result = search(clipboard.paste())
    emoji = search_result.getText()[2:3]
    clipboard.copy(emoji)
    print(emoji)

