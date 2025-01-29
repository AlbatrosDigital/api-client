
import json
import logging

import click
from gql import gql, Client
import pandas as pd

from lib.queries import fueltable
from lib.polar_plot import polar_plot as pp

from .ship import ship

DraftNames = [
    "scantling_draft",
    "design_draft",
    "ballast_draft",
]


@ship.command()
@click.argument("id")
@click.option("--format", "-f", type=click.Choice(["json", "csv"]), default="json")
@click.pass_context
def fuel_table(ctx, id: str, format: str):
    """Download the fueltable of specified ship.
    available output formats: json, csv
    """

    client: Client = ctx.obj["client"]
    result = client.execute(gql(fueltable), variable_values={"id": id})

    if format == "json":
        click.echo(json.dumps(result))
    elif format == "csv":
        fuel_table = result["digitalShip"]["get"]["fuelTable"]
        keys = tuple(fuel_table.keys())
        click.echo(', '.join(keys))
        for i in range(len(fuel_table[keys[0]])):
            click.echo(', '.join([str(fuel_table[key][i]) for key in keys]))


@ship.command()
@click.argument("id")
@click.option("--draft", "-d", type=click.Choice([dn for dn in DraftNames]), default=DraftNames[1])
@click.option("--speed", "-s", type=float, default=0)
@click.option("--wave-direction", "-wd", type=float, default=0)
@click.option("--significant-wave-height", "-wh", type=float, default=0)
@click.pass_context
def polar_plot(ctx, id: str, draft: str, speed: float, wave_direction: float, significant_wave_height: float):
    """Plot one output variable as polarplot.

    id: The uuid identifying the ship

    output_variable: The output variable to plot
    """
    logging.getLogger().setLevel("WARNING")

    sorting_cols = [
        "Draft [m]",
        "Speed [m/s]",
        "TWA [deg]",
        "TWS [m/s]",
        "Wave direction [deg]",
        "Wave height Hs [m]"
    ]
    variables = {
        "id": id,
        "draft": draft,
        "speed": speed,
        "waveDir": wave_direction,
        "sigWaveHeight": significant_wave_height
    }

    default_variable = "FC ME [ton/day]"

    client: Client = ctx.obj["client"]
    result = client.execute(gql(fueltable), variable_values=variables)

    name = result["digitalShip"]["get"]["name"]
    fuel_table = pd.DataFrame(result["digitalShip"]["get"]["fuelTable"])

    fig = pp(fuel_table, name, default_variable, sorting_cols)

    fig.show()
