import numpy as np
import pandas as pd
import plotly.graph_objects as go

def polar_plot(fuel_table: pd.DataFrame, name: str, default_variable: str, sorting_cols: list[str]) -> go.Figure:

    twa_theta = fuel_table["TWA [deg]"]
    tws_r = fuel_table["TWS [m/s]"]
    default_col = fuel_table[default_variable]

    max_r = max(tws_r)
    
    X = tws_r * np.sin(np.deg2rad(twa_theta))
    Y = tws_r * np.cos(np.deg2rad(twa_theta))
 
    fig = go.Figure()

    # The colored contour
    fig.add_trace(go.Contourcarpet(
        a=twa_theta,
        b=tws_r,
        z=default_col,
        line = dict(
            width = 0, # otherwise it draws a black line between two colors
            smoothing=1 # smooth the colors
        ),
        contours=dict(
            start=min(default_col), # start at the minimum value of z
            end=max(default_col), # end at the maximum value of z
            size=(max(default_col) - min(default_col)) / 180, # step size: 180 equal steps. There seems to be a weird bug fucking up the colors at some random step sizes
        ),
        colorbar=dict(
            title=dict(
                text=default_variable,
                side='right',
            ),
        )
    ))

    # The labeled blacklines over the contour
    fig.add_trace(go.Contourcarpet(
        a=twa_theta,
        b=tws_r,
        z=default_col,
        line=dict(
            width=1,
            smoothing=1
        ),
        contours=dict(
            coloring='none', # no coloring. For that we have the previous trace
            showlabels=True, # we want our lines to be labeled with the value they represent
        ),
    ))

    # The white polar axes
    fig.add_trace(go.Carpet(
        a=twa_theta,
        b=tws_r,
        x=X,
        y=Y,
        aaxis=dict(
            showticklabels='end', # show ticks on the outside of the polar
            ticksuffix='°'
        ),
        baxis=dict(
            title='TWS [m/s]'
        ),
    ))

    # Separately add aaxis title since it's not supported to put the title at the end of the axis in plotly
    fig.add_annotation(
        text="TWA [deg]",
        xref="x",
        yref="y",
        textangle=45,
        x=0.8 * max_r,
        y=0.8 * max_r,
        font=dict(
            size=15,
        ),
        showarrow=False)
    
    # various updates to the layout
    fig.update_layout(
        # add the title
        title=dict(
            text=name,
            x=0.5,
        ),
    )

    fig.update_layout(
        # remove x and y axis
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            visible=False,
        ),
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
            range=[-1.15*max_r, 1.15*max_r],
            showgrid=False,
            zeroline=False,
            visible=False
        ),
        plot_bgcolor='rgba(0,0,0,0)',
    )

    variable_options = get_variable_options(fuel_table, sorting_cols)

    fig.update_layout(
        # add buttons to switch between output variables
        updatemenus=[
            dict(
                active = 0,
                buttons=variable_options,
            ),
        ]
    )

    return fig


def get_variable_options(fuel_table: pd.DataFrame, sorting_cols: list[str]) -> list[dict]:
    variable_options = []
    for col_name in fuel_table.columns:
        if col_name in sorting_cols:
            continue

        col = fuel_table[col_name]

        button_dict = dict(
            args=[
                dict(
                    z=[col, col, None],
                    contours=[
                        dict(
                            start=min(col), # start at the minimum value of z
                            end=max(col), # end at the maximum value of z
                            size=(max(col) - min(col)) / 180, # step size: 180 equal steps. There seems to be a weird bug fucking up the colors at some random step sizes
                        ),
                        dict(
                            coloring='none', # no coloring. For that we have the previous trace
                            showlabels=True, # we want our lines to be labeled with the value they represent
                        ),
                        None
                    ],
                    colorbar=[
                        dict(
                            title=dict(
                                text=col_name,
                                side='right',
                            ),
                        ),
                        None,
                        None,
                    ],
                    line=[
                        dict(
                            width=0,
                            smoothing=1
                        ),
                        dict(
                            width=1, # otherwise it draws a black line between two colors
                            smoothing=1 # smooth the colors
                        ),
                        None,
                    ]
                )
            ],
            label=col_name,
            method="restyle",
        )

        variable_options.append(button_dict)
    return variable_options