import dash

# UI Libraries
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

# Imports for Callbacks
from dash.dependencies import Input, Output

# Application Definition
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Import your visualisations here
from arc_layer import arc_layer_map
from hexagonal_layer import hexagonal_layer_map
from custom_layer import custom_layer_map
from column_layer import column_layer_map

# add the visualisation name to the list like in this format
# then add them in the callback. that's it
map_list = [
    "arc-layer",
    "hexagonal-layer",
    "custom-layer-map",
    "column-layer-map",
]

app.layout = dbc.Container(
    [
        # Header
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H1("Deck GL Visualization"),
                    ]
                )
            ]
        ),
        html.Hr(),
        # Main
        dbc.Row(
            [
                # Controls
                dbc.Col(
                    [
                        html.H3("Map Controls"),
                        dcc.Dropdown(
                            id="map-controls",
                            options=map_list,
                            value=map_list[1],
                        ),
                    ],
                    width=3,
                    md=3,
                ),
                # Maps
                dbc.Col(
                    [
                        html.Div(
                            [],
                            id="map-graph",
                            style={
                                "height": "600px",
                                "width": "100%",
                                "position": "relative",
                            },
                        ),
                    ],
                    width=9,
                    md=9,
                ),
            ],
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("map-graph", "children"),
    [
        Input("map-controls", "value"),
    ],
)
def update_map(map_type):
    if map_type == "arc-layer":
        return arc_layer_map
    elif map_type == "hexagonal-layer":
        return hexagonal_layer_map
    elif map_type == "custom-layer-map":
        return custom_layer_map
    elif map_type == "column-layer-map":
        return column_layer_map
    # simply add them like this comment
    # elif map_type == "map-type-2":
    #     return map_type_2


if __name__ == "__main__":
    app.run_server(debug=True)
