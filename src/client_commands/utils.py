
import logging
import json
from configparser import ConfigParser
from pathlib import Path

import click
from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

from .queries import login as login_query

@click.command()
@click.pass_context
def shipyard_version(ctx):
    """Return the current api version."""

    query = """query {
      version
    }
    """

    client: Client = ctx.obj["client"]
    result = client.execute(gql(query), variable_values={})
    
    if ctx.obj["pretty"]:
        click.echo(json.dumps(result, indent=4))
    else:
        click.echo(json.dumps(result))


@click.command()
@click.pass_context
def login(ctx):
    """Obtain a valid jwt token."""
    
    logging.info("Logging in...")
    logging.getLogger().setLevel("WARNING")

    config: ConfigParser = ctx.obj["config"]
    client: Client = ctx.obj["client"]
    transport: AIOHTTPTransport = ctx.obj["transport"]
    config_file: Path = ctx.obj["config_file"]
    env = ctx.obj["env"]

    query = gql(login_query)
    params = {"username": config[env]["username"], "password": config[env]["password"]}
    result = client.execute(query, variable_values=params)

    if result['login']['__typename'] == "LoginError":
        logging.error(result['login']['message'])
        return
    
    token = result['login']['token']['accessToken']
    config[env]["token"] = token
    transport.headers["Authorization"] = f"Bearer {token}"

    with open(config_file, 'w') as configfile:
        config.write(configfile)


@click.command()
@click.pass_context
def config(ctx):
    """Print the current config."""

    for section in ctx.obj["config"]:
        click.echo(f"[{section}]")
        for key in ctx.obj["config"][section]:
            if key == "password":
                click.echo(f"{key} = ********")
            else:
                click.echo(f"{key} = {ctx.obj['config'][section][key]}")

@click.command()
@click.argument("env", type=click.Choice(["local", "dev", "prod"]))
@click.pass_context
def set_env(ctx, env: str):
    """Set the current environment."""

    config: ConfigParser = ctx.obj["config"]
    config_file: Path = ctx.obj["config_file"]

    config["DEFAULT"]["env"] = env

    with open(config_file, 'w') as configfile:
        config.write(configfile)