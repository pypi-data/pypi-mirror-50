import click
from .common import *
from .tsne import main

@click.command()
@click.option('--root', required=True)
@click.option('--out', required=True)
@click.option('--tsne_input', required=True)
@click.option('--target', required=True)
def main_cli(root, out, tsne_input, target):
    args = None
    args.__setattr__('root', root)
    args.__setattr__('out', out)
    args.__setattr__('tsne_input', tsne_input)
    args.__setattr__('target', target)
    main(args)
    