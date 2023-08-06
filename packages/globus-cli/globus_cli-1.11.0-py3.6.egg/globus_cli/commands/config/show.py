import click

from globus_cli.config import lookup_option
from globus_cli.parsing import common_options


@click.command("show", help="Show a value from the Globus config file")
@common_options(no_format_option=True)
@click.argument("parameter", required=True)
def show_command(parameter):
    """
    Executor for `globus config show`
    """
    section = "cli"
    if "." in parameter:
        section, parameter = parameter.split(".", 1)

    value = lookup_option(parameter, section=section)

    if value is None:
        click.echo("{} not set".format(parameter))
    else:
        click.echo("{} = {}".format(parameter, value))
