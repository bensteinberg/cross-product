import click
import csv
import requests
from pathlib import Path
from lxml import etree

pg = 'https://www.gutenberg.org'


def get_catalog(cache):
    """Get and cache catalog"""
    catalog = Path(f'{cache}/pg_catalog.csv')
    catalog_url = f'{pg}/cache/epub/feeds/pg_catalog.csv'
    cache_file(catalog_url, catalog)

    with open(catalog, 'r') as f:
        reader = csv.DictReader(f)
        works = [row for row in reader]

    return works


def get_work(text_no, cache):
    """Get a work"""
    metadata = Path(f'{cache}/{text_no}.rdf')
    metadata_url = f'{pg}/ebooks/{text_no}.rdf'
    cache_file(metadata_url, metadata)

    with open(metadata, 'rb') as f:
        rdf = f.read()

    tree = etree.fromstring(rdf)

    ns = {"pgterms": "http://www.gutenberg.org/2009/pgterms/",
          "dcterms": "http://purl.org/dc/terms/",
          "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"}

    utf8a = 'text/plain; charset="utf-8"'
    utf8b = 'text/plain; charset=utf-8'

    hits = [h.attrib['{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about']
            for h in tree.findall(".//pgterms:file", namespaces=ns)
            # the following does not always work, because PG metadata
            # is inconsistent
            if (h.findall(f".//*[rdf:value = '{utf8a}']", namespaces=ns)
                or h.findall(f".//*[rdf:value = '{utf8b}']", namespaces=ns)
                or 'utf-8' in h.attrib[
                    '{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about'
                ])
            ]

    if len(hits) > 1:
        click.echo(
            f'Too many files returned for text number {text_no}', err=True
        )
    elif len(hits) == 0:
        raise Exception(f'No UTF-8 files found for text number {text_no}')

    url = hits[0]
    filename = Path(f'{cache}/{url.split("/")[-1]}')
    cache_file(url, filename)
    with open(filename, 'r') as f:
        text = f.read()

    return text


def cache_file(url, path):
    """Get a file if necessary"""
    if not path.is_file():
        r = requests.get(url)
        with open(path, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=128):
                fd.write(chunk)
        click.echo(f'got {path}', err=True)
