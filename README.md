# J-Pop Lyrics Analysis

## Requirements

- [pyenv](https://github.com/pyenv/pyenv)
- [pipenv](https://github.com/pypa/pipenv)

## Building and deployment

```sh
$ brew install mecab
$ brew install mecab-ipadic
$ brew install swig

$ pipenv install --dev
$ pre-commit install
```

## Workflow

1. Extract and store the lyrics into SQLite database locally.

```sh
jla scrape --help
```

2. Analyze then generate the word cloud

```sh
jla analyze --help
```

![word cloud sample](examples/word_cloud_sample.png)

## TODO

- Expand the database.
- Try different extraction criteria.

## Acknowledgments

- Inspired by [猫弟Azz](https://www.douban.com/note/630489583/).