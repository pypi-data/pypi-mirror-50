import click
from parsec.cli import pass_context, json_loads
from parsec.decorators import custom_exception, dict_output


@click.command('delete_group_user')
@click.argument("group_id", type=str)
@click.argument("user_id", type=str)
@pass_context
@custom_exception
@dict_output
def cli(ctx, group_id, user_id):
    """Remove a user from the given group.

Output:

    The user which was removed
    """
    return ctx.gi.groups.delete_group_user(group_id, user_id)
