import click
from parsec.cli import pass_context, json_loads
from parsec.decorators import custom_exception, list_output


@click.command('create_folder')
@click.argument("library_id", type=str)
@click.argument("folder_name", type=str)
@click.option(
    "--description",
    help="description of the new folder in the data library",
    type=str
)
@click.option(
    "--base_folder_id",
    help="id of the folder where to create the new folder. If not provided, the root folder will be used",
    type=str
)
@pass_context
@custom_exception
@list_output
def cli(ctx, library_id, folder_name, description="", base_folder_id=""):
    """Create a folder in a library.

Output:

    List with a single dictionary containing information about the new folder
    """
    return ctx.gi.libraries.create_folder(library_id, folder_name, description=description, base_folder_id=base_folder_id)
