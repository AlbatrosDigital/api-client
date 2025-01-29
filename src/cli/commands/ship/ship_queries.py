import json

import click
from gql import gql, Client

from .ship import ship

@ship.command()
@click.argument("id")
@click.option("--include-fueltable", is_flag=True)
@click.pass_context
def get(ctx, id: str, include_fueltable: bool):
    """Run a custom query."""

    query = """query ships($id: String!) {
        digitalShip {
            get(id: $id) {
                modelType {
                    readableName
                }
                id
                status
                name
                shipData {
                    shipType
                    lengthOverall
                    beam
                    depth
                    drafts
                    csr
                    deadweight
                    grossTonnage
                    typeOfFuel
                    speedAtCsr
                }
                outputVariables
                company {
                    name
                }
                drafts {
                    name
                    draft
                    loadcaseCount
                    failureCount
                }
            }
        }
    }
    """

    query_ft = """query ships($id: String!) {
        digitalShip {
            get(id: $id) {
                modelType {
                    readableName
                }
                id
                status
                name
                shipData {
                    shipType
                    lengthOverall
                    beam
                    depth
                    drafts
                    csr
                    deadweight
                    grossTonnage
                    typeOfFuel
                    speedAtCsr
                }
                outputVariables
                company {
                    name
                }
                drafts {
                    name
                    draft
                    loadcaseCount
                    failureCount
                }
                fuelTable
            }
        }
    }
    """

    client: Client = ctx.obj["client"]
    if include_fueltable:
        result = client.execute(gql(query_ft), variable_values={"id": id})
    else:
        result = client.execute(gql(query), variable_values={"id": id})

    if ctx.obj["pretty"]:
        click.echo(json.dumps(result, indent=4))
    else:
        click.echo(json.dumps(result))

@ship.command()
@click.pass_context
@click.option("--limit", "-l", type=int, default=10)
@click.option("--offset", "-o", type=int, default=0)
def list(ctx, limit: int, offset: int):
    """Run a custom query."""

    query = """query ships ($limit: Int!, $offset: Int!) {
        digitalShip {
            list(limit: $limit, offset: $offset) {
                meta {
                    count
                    limit
                    offset
                }
                data {
                    modelType {
                        readableName
                    }
                    id
                    status
                    name
                    shipData {
                        shipType
                        lengthOverall
                        beam
                        depth
                        drafts
                        csr
                        deadweight
                        grossTonnage
                        typeOfFuel
                        speedAtCsr
                    }
                    outputVariables
                    company {
                        name
                    }
                }
            }
        }
    }
    """

    client: Client = ctx.obj["client"]
    result = client.execute(gql(query), variable_values={"limit": limit, "offset": offset})

    if ctx.obj["pretty"]:
        click.echo(json.dumps(result, indent=4))
    else:
        click.echo(json.dumps(result))