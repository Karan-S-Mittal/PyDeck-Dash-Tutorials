import os

mapbox_api_token = os.getenv("MAPBOX_ACCESS_TOKEN")

import pydeck

pydeck.settings.custom_libraries = [
    {
        "libraryName": "LabeledGeoJsonLayerLibrary",
        "resourceUri": "https://unpkg.com/pydeck-custom-layer-demo/dist/bundle.js",
    }
]

DATA_URL = (
    "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
)

custom_layer = pydeck.Layer(
    "LabeledGeoJsonLayer",
    data=DATA_URL,
    filled=False,
    billboard=False,
    get_line_color=[180, 180, 180],
    get_label="properties.name",
    get_label_size=200000,
    get_label_color=[0, 255, 255],
    label_size_units=pydeck.types.String("meters"),
    line_width_min_pixels=1,
)

view_state = pydeck.ViewState(latitude=0, longitude=0, zoom=1)

r = pydeck.Deck(
    custom_layer, initial_view_state=view_state, api_keys={"mapbox": mapbox_api_token}
)

# r.to_html("custom_layer.html", css_background_color="#333")

import dash_deck

custom_layer_map = dash_deck.DeckGL(
    r.to_json(), id="custom-layer-map", mapboxKey=r.mapbox_key
)
