import click

from globus_cli.parsing import common_options, endpoint_id_arg, role_id_arg
from globus_cli.safeio import FORMAT_TEXT_RAW, formatted_print
from globus_cli.services.transfer import get_client


@click.command("delete", help="Remove a role from an endpoint")
@common_options
@endpoint_id_arg
@role_id_arg
def role_delete(role_id, endpoint_id):
    """
    Executor for `globus endpoint role delete`
    """
    client = get_client()
    res = client.delete_endpoint_role(endpoint_id, role_id)
    formatted_print(res, text_format=FORMAT_TEXT_RAW, response_key="message")
