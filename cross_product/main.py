import click
import re
import sys
from pathlib import Path
from itertools import cycle
from cross_product.catalog import get_work


@click.command()
@click.argument('factors', nargs=-1)
@click.option('--cache', default='pg_cache', help='Cache directory',
              show_default=True)
def cross(factors, cache):
    """
    Squash books together; arguments ("factors") are either
    filenames or Project Gutenberg numbers.
    """
    if len(factors) < 2:
        click.echo('You must specify two or more works.', err=True)
        sys.exit()

    works = [
        open(f'{cache}/{f}', 'r').read() if Path(f'{cache}/{f}').is_file()
        else get_work(f, cache)
        for f in factors
    ]

    # regex for splitting sentences from https://stackoverflow.com/a/43075629
    texts = [re.split("(?<=[.!?])\s+",  # noqa
                      w.replace("\n", " "))
             for w in works]

    # make the shortest input the first
    texts.sort(key=len)

    # roughly skip frontmatter and endmatter
    for i in range(350, len(texts[0]) - 200):
        j = cycle(range(len(factors)))
        wordss = [t[i].split(" ") for t in texts]
        sentence = ' '.join([word[next(j)]
                             for word
                             in zip(*wordss)
                             ]).rstrip().rstrip(',')
        sentence = re.sub(r' +', ' ', sentence)
        click.echo(sentence + '.' if sentence[-1] not in '?.!"”' else '')


if __name__ == '__main__':
    cross()
