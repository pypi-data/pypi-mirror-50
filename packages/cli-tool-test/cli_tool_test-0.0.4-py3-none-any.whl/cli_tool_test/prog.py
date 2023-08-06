import argparse
import sys
import click
import pyfiglet


__version__ = "0.2.0"


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name', help='The person to greet.')
def greet(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s!' % name)

@click.command()
@click.option('--text', default='Hello', help='Generates ascii art')
def generate_ascii_art(text):
    ascii_banner = pyfiglet.figlet_format(text)
    print(ascii_banner)


