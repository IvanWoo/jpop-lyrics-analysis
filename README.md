# J-Pop Lyrics Analysis

## Installation Prerequisites

```sh
brew install mecab
brew install mecab-ipadic
brew install swig

python -m venv venv

pip install --upgrade
pip install -r requirements.txt
```

## Work Flow

1. Extract and store the lyrics into SQLite database locally. (get-lyrics.py)
2. Use Mecab, a morphological analysis engine, to splite the lyrics sentences into unit words. (morphological-analysis.py)
3. Use cloud word to analyze and generate the cloud word image. (generate_word_cloud.py)

![word cloud sample](https://raw.githubusercontent.com/IvanWoo/jpop-lyrics-analysis/master/word_cloud_sample.png)

## TODO

- Expand the database.
- Try different extraction criteria.

## Acknowledgments

- Inspired by [猫弟Azz](https://www.douban.com/note/630489583/).