#!/usr/bin/env python

from click.types import File
from rich import print
from rich.prompt import Confirm
import click
import rich.console
import rich.logging
import rich.traceback
import sys
import os
import utils
#import nf_core
# conda install -c conda-forge click
# conda install -c conda-forge rich

def run_bu_isciii():
      # Set up rich stderr console
    stderr = rich.console.Console(stderr=True, force_terminal=utils.rich_force_colors())

    # Set up the rich traceback
    rich.traceback.install(console=stderr, width=200, word_wrap=True, extra_lines=1)

    # Print nf-core header
    #stderr.print("\n[green]{},--.[grey39]/[green],-.".format(" " * 42), highlight=False)
    stderr.print("[blue]                 ___              ___    ___   ___  ___   ___   ____   ", highlight=False)
    stderr.print("[blue]   \    |-[grey39]-|  [blue]  |   \   |   |      |    |     |      |     |      |    ", highlight=False)
    stderr.print("[blue]    \   \  [grey39]/ [blue]   |__ /   |   | ___  |    |__   |      |     |      |    ", highlight=False)
    stderr.print("[blue]    /  [grey39] / [blue] \    |   \   |   |      |       |  |      |     |      |    ", highlight=False)
    stderr.print("[blue]   /   [grey39] |-[blue]-|    |__ /   |___|     _|__  ___|  |___  _|_   _|_    _|_   ", highlight=False)


    #stderr.print("[green]                                          `._,._,'\n", highlight=False)
    __version__ = '0.0.1'
    stderr.print("[grey39]    BU-ISCIII-tools version {}".format(__version__), highlight=False)
    try:
        pass
    except:
        pass

    # Lanch the click cli
    bu_isciii_cli()



# Customise the order of subcommands for --help
class CustomHelpOrder(click.Group):
    def __init__(self, *args, **kwargs):
        self.help_priorities = {}
        super(CustomHelpOrder, self).__init__(*args, **kwargs)

    def get_help(self, ctx):
        self.list_commands = self.list_commands_for_help
        return super(CustomHelpOrder, self).get_help(ctx)

    def list_commands_for_help(self, ctx):
        """reorder the list of commands when listing the help"""
        commands = super(CustomHelpOrder, self).list_commands(ctx)
        return (c[1] for c in sorted((self.help_priorities.get(command, 1000), command) for command in commands))

    def command(self, *args, **kwargs):
        """Behaves the same as `click.Group.command()` except capture
        a priority for listing command names in help.
        """
        help_priority = kwargs.pop("help_priority", 1000)
        help_priorities = self.help_priorities

        def decorator(f):
            cmd = super(CustomHelpOrder, self).command(*args, **kwargs)(f)
            help_priorities[cmd.name] = help_priority
            return cmd

        return decorator


@click.group(cls=CustomHelpOrder)
#@click.version_option(nf_core.__version__)
@click.option("-v", "--verbose", is_flag=True, default=False, help="Print verbose output to the console.")
@click.option("-l", "--log-file", help="Save a verbose log to a file.", metavar="<filename>")
def bu_isciii_cli(verbose, log_file):

    # Set the base logger to output DEBUG
    log.setLevel(logging.DEBUG)

     # Set up logs to the console
    log.addHandler(
        rich.logging.RichHandler(
            level=logging.DEBUG if verbose else logging.INFO,
            console=rich.console.Console(stderr=True, force_terminal=nf_core.utils.rich_force_colors()),
            show_time=False,
            markup=True,
        )
    )

    # Set up logs to a file if we asked for one
    if log_file:
        log_fh = logging.FileHandler(log_file, encoding="utf-8")
        log_fh.setLevel(logging.DEBUG)
        log_fh.setFormatter(logging.Formatter("[%(asctime)s] %(name)-20s [%(levelname)-7s]  %(message)s"))
        log.addHandler(log_fh)

# pipeline list
@bu_isciii_cli.command(help_priority=1)
@click.argument("keywords", required=False, nargs=-1, metavar="<filter keywords>")
@click.option(
    "-s",
    "--sort",
    type=click.Choice(["release", "pulled", "name", "stars"]),
    default="release",
    help="How to sort listed pipelines",
)
@click.option("--json", is_flag=True, default=False, help="Print full output as JSON")
@click.option("--show-archived", is_flag=True, default=False, help="Print archived workflows")
def list(keywords, sort, json, show_archived):
    """
    List available bu-isciii workflows used for relecov.
    Checks the web for a list of nf-core pipelines with their latest releases.
    Shows which nf-core pipelines you have pulled locally and whether they are up to date.
    """
    print(nf_core.list.list_workflows(keywords, sort, json, show_archived))


# sftp
@bu_isciii_cli.command(help_priority=2)
@click.argument("pipeline", required=False, metavar="<pipeline name>")
@click.option("-r", "--revision", help="Release/branch/SHA of the project to run (if remote)")
@click.option("-i", "--id", help="ID for web-gui launch parameter set")
@click.option(
    "-c", "--command-only", is_flag=True, default=False, help="Create Nextflow command with params (no params file)"
)
@click.option(
    "-o",
    "--params-out",
    type=click.Path(),
    default=os.path.join(os.getcwd(), "nf-params.json"),
    help="Path to save run parameters file",
)
def sftp(pipeline, id, revision, command_only, params_in, params_out, save_all, show_hidden, url):
    '''
    Download files located in sftp server.

    '''
    print(nf_core.list.list_workflows(keywords, sort, json, show_archived))

# metadata
@bu_isciii_cli.command(help_priority=3)
@click.argument("pipeline", required=False, metavar="<pipeline name>")
@click.option("-r", "--revision", help="Release/branch/SHA of the project to run (if remote)")
@click.option("-i", "--id", help="ID for web-gui launch parameter set")
@click.option(
    "-c", "--command-only", is_flag=True, default=False, help="Create Nextflow command with params (no params file)"
)
@click.option(
    "-o",
    "--params-out",
    type=click.Path(),
    default=os.path.join(os.getcwd(), "nf-params.json"),
    help="Path to save run parameters file",
)
def metadata(pipeline, id, revision, command_only, params_in, params_out, save_all, show_hidden, url):
    '''
    Read Metadata .

    '''
    print(nf_core.list.list_workflows(keywords, sort, json, show_archived))
    
if __name__ == "__main__":
    run_bu_isciii()