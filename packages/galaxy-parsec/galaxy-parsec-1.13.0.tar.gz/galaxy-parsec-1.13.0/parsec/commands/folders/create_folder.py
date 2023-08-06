import click
from parsec.cli import pass_context, json_loads
from parsec.decorators import custom_exception, dict_output


@click.command('create_folder')
@click.argument("parent_folder_id", type=str)
@click.argument("name", type=str)
@click.option(
    "--description",
    help="folder's description",
    type=str
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, parent_folder_id, name, description=""):
    """Create a folder.

Output:

    details of the updated folder
    """
    return ctx.gi.folders.create_folder(parent_folder_id, name, description=description)
