cross-product
=============

This is [an entry](https://github.com/NaNoGenMo/2022/issues/40) for
NaNoGenMo 2022. It takes two or more texts and forms a "novel" of
words taken alternately from each input, with a number of "sentences"
equal to those in the text with the least number of sentences. Each
"sentence" in the output has a number of words equal to the sentence
with the least number of words at the given position in all inputs.

Usage
-----

[Install Poetry](https://python-poetry.org/docs/#installation), clone
this repository, then run

```
cd cross-product
poetry install
poetry run cross <text1> <text2> <etc> > output.txt
```

By default, the program will look for input files in the `pg_cache/`
directory. You can also supply Project Gutenberg text numbers; the
metadata files and text files will be cached in the same location.

Example
-------

A [sample](moby-jones-march.txt) is included in this repo, produced by
operating on _[Moby Dick](https://gutenberg.org/ebooks/2701)_, _[The History of Tom Jones, a Foundling](https://gutenberg.org/ebooks/6593)_, and
_[Middlemarch](https://gutenberg.org/ebooks/145)_, each obtained from Project Gutenberg:

```
poetry run cross 2701-0.txt 6593-0.txt pg145.txt > moby-jones-march.txt
```

[Another sample output](war-crime-karenina.txt) was produced by squashing _[War and Peace](https://gutenberg.org/ebooks/2600)_, _[Crime and Punishment](https://gutenberg.org/ebooks/2554)_, and _[Anna Karenina](https://gutenberg.org/ebooks/1399)_:

```
poetry run cross 2600 2554 1399 > war-crime-karenina.txt
```
