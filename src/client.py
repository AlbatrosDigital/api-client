
import sys
sys.path.append('src')
import logging
import pathlib
import configparser
from datetime import datetime

from gql import Client
from gql.transport.aiohttp import AIOHTTPTransport
import jwt
import click

from .client_commands.custom import custom
from .client_commands.utils import shipyard_version, config, login, set_env
from .client_commands.ship.ship import ship

@click.group()
@click.option("-q", "--quiet", is_flag=True)
@click.option("-p", "--pretty", is_flag=True)
@click.option("-e", "--env", type=click.Choice(["local", "dev", "prod"]))
@click.pass_context
def shipyard_client(ctx, quiet: bool, pretty: bool, env: str=None):
    ctx.ensure_object(dict)
    ctx.obj["pretty"] = pretty

    ### Set up logging
    log_level = logging.INFO
    if quiet:
        log_level = logging.ERROR

    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s',
        level=log_level,
        datefmt='%Y-%m-%d %H:%M:%S',
        force=True)

    ### Set up config
    home = pathlib.Path.home()
    shipyard_dir = home / ".shipyard"
    config_file = shipyard_dir / "config.ini"

    if not shipyard_dir.is_dir():
        shipyard_dir.mkdir()
    
    if not config_file.is_file():
        config_file.touch()
    
    ctx.obj["shipyard_dir"] = shipyard_dir
    ctx.obj["config_file"] = config_file

    config = configparser.ConfigParser()
    config.read(config_file)

    if not env:
        env = config["DEFAULT"]["env"]
        ctx.obj["env"] = env
    
    if not env in config:
        raise ValueError(f"Environment {env} not found in config file {config_file}")

    ctx.obj["config"] = config
    
    ### Set up client
    transport = AIOHTTPTransport(url=config[env]["url"], headers={})
    client = Client(transport=transport, execute_timeout=30)
    ctx.obj["transport"] = transport
    ctx.obj["client"] = client

    if 'token' in config[env]:
        payload = jwt.decode(config[env]["token"], algorithms=["HS256"], options={"verify_signature": False})
        exp_dt = payload.get("exp")

        if datetime.now().timestamp() > exp_dt:
            del config[env]["token"]
            logging.info("Token expired")
        else:
            logging.info("Valid token found")
            transport.headers["Authorization"] = f"Bearer {config[env]["token"]}"

    with open(ctx.obj["config_file"], 'w') as configfile:
        config.write(configfile)


shipyard_client.add_command(custom)
shipyard_client.add_command(shipyard_version)
shipyard_client.add_command(ship)
shipyard_client.add_command(config)
shipyard_client.add_command(login)
shipyard_client.add_command(set_env)
