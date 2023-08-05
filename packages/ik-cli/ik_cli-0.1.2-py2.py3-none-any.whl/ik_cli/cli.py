import sys
from pathlib import Path

import click


class Context:
    def __init__(self):
        self.verbose = False
        self.debug = False

    def log(self, msg, *args, color=None):
        if args:
            msg %= args
        color = color
        if self.debug:
            color = 'red'
        click.echo(msg, file=sys.stderr, color=color)

    def v_log(self, msg, *args):
        if self.verbose:
            self.log(msg, *args, color='yellow')


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = Path(__file__).parent / 'commands'


class ComplexCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for path in list(cmd_folder.glob('cmd_*.py')):
            rv.append(path.name[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, cmd_name):
        try:
            mod = __import__('ik_cli.commands.cmd_' + cmd_name, fromlist=['cli'])
        except ImportError:
            return
        return mod.cli


@click.command(cls=ComplexCLI)
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose mode.')
@pass_context
def cli(ctx, verbose):
    ctx.verbose = verbose
