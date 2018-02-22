import click

from commands.detect_modifications import track_modifications
from commands.rename_import import execute_rename

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='0.0.1')
def app():
    print('app')


@app.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--origin', default='master', help='Name of the branch to start the evaluation')
@click.option('--destination', default=False, help='Name of the branch that has the modifications')
def track(**kwargs):
    track_modifications(**kwargs)


@app.command()
def rename(**kwargs):
    print('rename')
    # execute_rename()


if __name__ == '__main__':
    app()
