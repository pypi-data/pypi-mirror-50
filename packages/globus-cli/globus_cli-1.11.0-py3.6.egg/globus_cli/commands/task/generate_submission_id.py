import click

from globus_cli.parsing import common_options
from globus_cli.safeio import FORMAT_TEXT_RAW, formatted_print
from globus_cli.services.transfer import get_client


@click.command(
    "generate-submission-id",
    short_help="Get a submission ID",
    help=(
        "Generate a new task submission ID for use in "
        "`globus transfer` and `gloubs delete`. Submission IDs "
        "allow you to safely retry submission of a task in the "
        "presence of network errors. No matter how many times "
        "you submit a task with a given ID, it will only be "
        "accepted and executed once. The response status may "
        "change between submissions."
    ),
)
@common_options
def generate_submission_id():
    """
    Executor for `globus task generate-submission-id`
    """
    client = get_client()

    res = client.get_submission_id()
    formatted_print(res, text_format=FORMAT_TEXT_RAW, response_key="value")
