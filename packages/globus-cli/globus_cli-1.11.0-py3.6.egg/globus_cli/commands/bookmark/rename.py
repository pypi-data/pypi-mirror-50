import click

from globus_cli.commands.bookmark.helpers import resolve_id_or_name
from globus_cli.parsing import common_options
from globus_cli.safeio import formatted_print
from globus_cli.services.transfer import get_client


@click.command("rename", help="Change a bookmark's name")
@common_options
@click.argument("bookmark_id_or_name")
@click.argument("new_bookmark_name")
def bookmark_rename(bookmark_id_or_name, new_bookmark_name):
    """
    Executor for `globus bookmark rename`
    """
    client = get_client()
    bookmark_id = resolve_id_or_name(client, bookmark_id_or_name)["id"]

    submit_data = {"name": new_bookmark_name}

    res = client.update_bookmark(bookmark_id, submit_data)
    formatted_print(res, simple_text="Success")
