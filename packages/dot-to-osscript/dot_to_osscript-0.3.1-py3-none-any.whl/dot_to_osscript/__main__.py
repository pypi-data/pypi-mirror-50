import click
from .generate import *


@click.command()
@click.option("--powershell", "-p", is_flag=True, help='Generate .env.ps1')
@click.option("--shell", "-s", is_flag=True, help='Generate .env.sh')
@click.option("--env-file", "-e", default="./.env", show_default=True, type=str, help='Input file')
@click.option("--path-append", "-a", is_flag=True, help='Appent to existing Path variable')
def cli(powershell, shell, env_file, path_append):
    from_dotenv(ps=powershell, sh=shell, env_file=env_file, path_append=path_append)


if __name__ == "__main__":
    cli()
