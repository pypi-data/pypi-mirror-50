import click
from PIL import Image
import logging

logging.basicConfig(format='%(asctime)s: %(message)s')

@click.command()
@click.option('-i', '--input', type=click.File('rb'), default='-', help="Input, File or stdin (-)  ", required=True,
              show_default=True)
@click.option('-o', '--output', type=click.Path(), help="Output, Filename", required=True,
              show_default=True)
@click.option('-b', '--box', type=(int, int, int, int), help="Box to crop", required=True)
def crop(input, output, box):
    img = Image.open(input)
    # crop
    # box = [0, 500, 3280, 2464]
    img = img.crop(box)
    # save
    img.save(output)

if __name__ == '__main__':
    crop()
