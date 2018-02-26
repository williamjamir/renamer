import sys

import click

from commands.detect_modifications import track_modifications
from commands.rename_import import run_rename

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='0.0.1')
def app():
    pass


@app.command()
@click.argument('project_path', type=click.Path(exists=True))
@click.option('--origin_branch', default='master', help='Branch to start the evaluation')
@click.option('--work_branch', default=False, help='Name of the branch that has the modifications')
@click.option('--output_file', default='list_output.py', help='Change the name of the output file')
def track(**kwargs):
    track_modifications(**kwargs)


@app.command()
@click.argument('project_path', nargs=-1, type=click.Path(exists=True))
@click.argument('moved_imports_file', type=click.Path(exists=True, resolve_path=True))
def rename(**kwargs):
    run_rename(**kwargs)


if __name__ == '__main__':
    # The sys.argv[1:] is necessary for debug on python2
    # Link: https://goo.gl/vp5hfz
    app(sys.argv[1:])
