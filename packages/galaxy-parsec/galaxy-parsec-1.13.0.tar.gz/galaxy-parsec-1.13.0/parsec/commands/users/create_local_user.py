import click
from parsec.cli import pass_context, json_loads
from parsec.decorators import custom_exception, dict_output


@click.command('create_local_user')
@click.argument("username", type=str)
@click.argument("user_email", type=str)
@click.argument("password", type=str)
@pass_context
@custom_exception
@dict_output
def cli(ctx, username, user_email, password):
    """Create a new Galaxy local user.

Output:

    a dictionary containing information about the created user
    """
    return ctx.gi.users.create_local_user(username, user_email, password)
