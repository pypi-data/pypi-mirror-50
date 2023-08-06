import click

from globus_cli.parsing import common_options, endpoint_id_arg
from globus_cli.safeio import formatted_print
from globus_cli.services.auth import LazyIdentityMap
from globus_cli.services.transfer import get_client


@click.command("list", help="List of permissions on an endpoint")
@common_options
@endpoint_id_arg
def list_command(endpoint_id):
    """
    Executor for `globus endpoint permission list`
    """
    client = get_client()

    rules = client.endpoint_acl_list(endpoint_id)

    resolved_ids = LazyIdentityMap(
        x["principal"] for x in rules if x["principal_type"] == "identity"
    )

    def principal_str(rule):
        principal = rule["principal"]
        if rule["principal_type"] == "identity":
            username = resolved_ids.get(principal)
            return username or principal
        elif rule["principal_type"] == "group":
            return (u"https://app.globus.org/groups/{}").format(principal)
        else:
            principal = rule["principal_type"]

        return principal

    formatted_print(
        rules,
        fields=[
            ("Rule ID", "id"),
            ("Permissions", "permissions"),
            ("Shared With", principal_str),
            ("Path", "path"),
        ],
    )
