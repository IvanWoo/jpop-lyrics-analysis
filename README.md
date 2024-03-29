# J-Pop Lyrics Analysis

## Requirements

- [pyenv](https://github.com/pyenv/pyenv)
- [pdm](https://pdm.fming.dev/latest/)

## Building and deployment

```sh
brew install mecab-ipadic dbmate

pdm install
pdm run pre-commit install
```

## Workflow

1. Extract and store the lyrics into SQLite database locally.

```sh
pdm run jla scrape --help
```

2. Analyze then generate the word cloud

```sh
pdm run jla analyze --help
```

![word cloud sample](examples/word_cloud_sample.png)

## TODO

- Expand the database.
- Try different extraction criteria.

## References
- [【Python】MacにMeCabを入れて自然言語処理をしてみよう(unidic-lite編)](https://www.teamxeppet.com/python-mecab-unidic-lite_mac/)

## Acknowledgments

- Inspired by [猫弟Azz](https://www.douban.com/note/630489583/).