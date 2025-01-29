
import logging
import json

import click
from gql import gql, Client


@click.command()
@click.argument("query", required=True)
@click.pass_context
def custom(ctx, query: str=None):
    """Run a custom query."""

    if query is None:
        logging.error("Please provide a query.")
        return

    client: Client = ctx.obj["client"]
    result = client.execute(gql(query), variable_values={})
    click.echo(json.dumps(result))

    if ctx.obj["pretty"]:
        click.echo(json.dumps(result, indent=4))
    else:
        click.echo(json.dumps(result))