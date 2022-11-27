import click
import re
import sys
from itertools import cycle


@click.command()
@click.argument('factors', type=click.File('r'), nargs=-1)
def cross(factors):
    """ Squash books together """
    error = None
    if len(factors) == 0:
        error = 'You must specify one or more files'
    elif len(factors) == 1:
        error = 'Output is the same as input'
    if error:
        click.echo(error, err=True)
        sys.exit()

    # regex for splitting sentences from https://stackoverflow.com/a/43075629
    texts = [re.split("(?<=[.!?])\s+",  # noqa
                      f.read().replace("\n", " "))
             for f in factors]

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
