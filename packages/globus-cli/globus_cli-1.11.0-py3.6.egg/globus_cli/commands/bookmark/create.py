import click

from globus_cli.parsing import ENDPOINT_PLUS_REQPATH, common_options
from globus_cli.safeio import formatted_print
from globus_cli.services.transfer import get_client


@click.command("create", help="Create a bookmark for the current user")
@common_options
@click.argument("endpoint_plus_path", type=ENDPOINT_PLUS_REQPATH)
@click.argument("bookmark_name")
def bookmark_create(endpoint_plus_path, bookmark_name):
    """
    Executor for `globus bookmark create`
    """
    endpoint_id, path = endpoint_plus_path
    client = get_client()

    submit_data = {"endpoint_id": str(endpoint_id), "path": path, "name": bookmark_name}

    res = client.create_bookmark(submit_data)
    formatted_print(res, simple_text="Bookmark ID: {}".format(res["id"]))
