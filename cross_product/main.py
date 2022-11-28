import click
import re
import sys
from pathlib import Path
from itertools import cycle
from cross_product.catalog import get_catalog, get_work


@click.command()
@click.argument('factors', nargs=-1)
@click.option('--cache', default='pg_cache', help='Cache directory',
              show_default=True)
def cross(factors, cache):
    """
    Squash books together; arguments ("factors") are either
    filenames or Project Gutenberg numbers.
    """
    text_nos = [row['Text#'] for row in get_catalog(cache)]
    works = []
    for f in factors:
        if Path(f'{cache}/{f}').is_file():
            works.append(open(f'{cache}/{f}', 'r').read())
        elif f in text_nos:
            works.append(get_work(f, cache))
        else:
            click.echo(f'{f} is neither a file nor a PG text ID.', err=True)

    if len(works) < 2:
        click.echo('You must specify two or more works.', err=True)
        sys.exit()

    # regex for splitting sentences from https://stackoverflow.com/a/43075629
    texts = [re.split("(?<=[.!?])\s+",  # noqa
                      w.replace("\n", " "))
             for w in works]

    # make the shortest input the first
    texts.sort(key=len)

    # roughly skip frontmatter and endmatter
    for i in range(350, len(texts[0]) - 200):
        j = cycle(range(len(works)))
        wordss = [t[i].split(" ") for t in texts]
        sentence = ' '.join([word[next(j)]
                             for word
                             in zip(*wordss)
                             ]).rstrip().rstrip(',')
        sentence = re.sub(r' +', ' ', sentence)
        click.echo(sentence + '.' if sentence[-1] not in '?.!"”' else '')


if __name__ == '__main__':
    cross()
