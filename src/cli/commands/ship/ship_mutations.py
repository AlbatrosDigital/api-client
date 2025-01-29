

import json
from pathlib import Path

import click
from gql import gql, Client


from lib.jsonify import jsonify
from .ship import ship


@ship.command()
@click.option("--name", type=str)
@click.option("--model-type", type=str)
@click.option("--depth", type=float)
@click.option("--csr", type=float)
@click.option("-i", "--input-file", type=click.Path(exists=True), multiple=True)
@click.pass_context
def create(ctx, name: str, model_type: str, depth: float, csr: float, input_file: list[str]):
    """Run a custom query."""

    out_vars = [
        "Draft [m]",
        "Speed [m/s]",
        "TWS [m/s]",
        "TWA [deg]",
        "Wave direction [deg]",
        "Wave height Hs [m]",
        "FC ME [ton/day]",
        "Heel [deg]",
        "Leeway [deg]",
        "Rudder angle [deg]",
        "FC ME [ton/day]",
        "Power brake [kW]"
    ]
    inputs = [jsonify(Path(file)) for file in input_file]

    ship_data = {
        "name": name,
        "modelType": model_type,
        "depth": depth,
        "inputs": inputs,
        "csr": csr,
        "outputVariables": out_vars
    }

    query = """mutation createShip($shipdata: ShipInput!) {
        digitalShip {
            custom(shipInput: $shipdata) {
                ... on DigitalShip {
                    id
                    name
                    status
                }
                ... on Error {
                    message
                }
            }
        }
    }
    """

    client: Client = ctx.obj["client"]
    result = client.execute(gql(query), variable_values={"shipdata": ship_data})

    if ctx.obj["pretty"]:
        click.echo(json.dumps(result, indent=4))
    else:
        click.echo(json.dumps(result))