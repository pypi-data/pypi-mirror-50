import click
import wget
import urllib.request
from tqdm import tqdm


opener=urllib.request.build_opener()
opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36 OPR/62.0.3331.116')]
urllib.request.install_opener(opener)

url = 'https://click.palletsprojects.com/en/7.x/_static/click-logo-sidebar.png'
@click.group()
def cli():
    "RUSH B"
    pass

@cli.command()
def cli1(dw):
    
    click.echo(dw)
  



@cli.command(help="Download a file")
@click.option('-url', prompt=True, confirmation_prompt=True, help='File link')

@click.option('-dir', prompt=True, confirmation_prompt=True, help='Download directory')
def down(url, dir):
    wget.download(url, out=dir)

cli.add_command(down)
cli.add_command(cli1)

if __name__ == '__main__':
    cli()
    cli1()
    down()
