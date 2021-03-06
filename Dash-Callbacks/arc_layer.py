"""
ArcLayer
========

Map of commutes to work within a segment of downtown San Francisco using a deck.gl ArcLayer.

Green indicates a start point, and red indicates the destination.

The data is collected by the US Census Bureau and viewable in the 2017 LODES data set: https://lehd.ces.census.gov/data/
"""


import pydeck as pdk
import pandas as pd

import os

mapbox_api_token = os.getenv("MAPBOX_ACCESS_TOKEN")

DATA_URL = "https://raw.githubusercontent.com/ajduberstein/sf_public_data/master/bay_area_commute_routes.csv"
# A bounding box for downtown San Francisco, to help filter this commuter data
DOWNTOWN_BOUNDING_BOX = [
    -122.43135291617365,
    37.766492914983864,
    -122.38706428091974,
    37.80583561830737,
]


def in_bounding_box(point):
    """Determine whether a point is in our downtown bounding box"""
    lng, lat = point
    in_lng_bounds = DOWNTOWN_BOUNDING_BOX[0] <= lng <= DOWNTOWN_BOUNDING_BOX[2]
    in_lat_bounds = DOWNTOWN_BOUNDING_BOX[1] <= lat <= DOWNTOWN_BOUNDING_BOX[3]
    return in_lng_bounds and in_lat_bounds


df = pd.read_csv(DATA_URL)
# print(df.info())
# Filter to bounding box
df = df[df[["lng_w", "lat_w"]].apply(lambda row: in_bounding_box(row), axis=1)]
# print(df.info())
print(df.head())
GREEN_RGB = [0, 255, 0, 40]  # takes in values for RGB and Opacity
RED_RGB = [240, 100, 0, 40]  # takes in values for RGB and Opacity

# Specify a deck.gl ArcLayer
arc_layer = pdk.Layer(
    "ArcLayer",
    data=df,
    get_width="S000 * 2",
    get_source_position=["lng_h", "lat_h"],
    get_target_position=["lng_w", "lat_w"],
    get_tilt=20,
    get_source_color=RED_RGB,
    get_target_color=GREEN_RGB,
    pickable=True,
    auto_highlight=True,
)

# An object that represents where the state of a viewport, essentially where the screen is focused.
view_state = pdk.ViewState(
    latitude=37.7576171,
    longitude=-122.5776844,
    bearing=45,
    pitch=50,
    zoom=8,
)


TOOLTIP_TEXT = {
    "html": "{S000} jobs <br /> Home of commuter in red; work location in green"
}

r = pdk.Deck(
    arc_layer,
    initial_view_state=view_state,
    tooltip=TOOLTIP_TEXT,
    api_keys={"mapbox": mapbox_api_token},
)  # converts the arc_layer to a deck.gl object
# r.to_html("arc_layer.html")  # uncomment to save to file

# Dash Code
import dash_deck

arc_layer_map = dash_deck.DeckGL(
    r.to_json(), id="arc-deck-gl", tooltip=TOOLTIP_TEXT, mapboxKey=r.mapbox_key
)
