import click
from parsec.cli import pass_context, json_loads
from parsec.decorators import custom_exception, dict_output


@click.command('delete_user')
@click.argument("user_id", type=str)
@click.option(
    "--purge",
    help="if ``True``, also purge (permanently delete) the history",
    is_flag=True
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, user_id, purge=False):
    """Delete a user.

Output:

    a dictionary containing information about the deleted user
    """
    return ctx.gi.users.delete_user(user_id, purge=purge)
