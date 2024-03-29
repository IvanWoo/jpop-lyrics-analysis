from functools import partial

import click

from jpop_lyrics_analysis.utils import (
    generate_word_cloud,
    get_artists,
    get_lyrics,
    morphological_analysis,
)

click.option = partial(click.option, show_default=True)


@click.group()
@click.version_option()
def cli():
    pass


@cli.command()
@click.option("-u", "--url", required=True, help="Target url to scrape")
def scrape(url):
    """
    \b
    Save lyrics into local database.
    Examples:
      - jla scrape -u https://www.uta-net.com/artist/39/
    """
    get_lyrics(url)


@cli.command()
@click.option(
    "-a",
    "--artist",
    type=click.Choice(get_artists()),
    required=True,
    help="Target artist to analyze",
)
def analyze(artist):
    """
    \b
    Analyze and generate the word cloud.
    Examples:
      - jla analyze -a aiko
    """
    morphological_analysis(artist)
    generate_word_cloud()


main = cli()

if __name__ == "__main__":
    main()
