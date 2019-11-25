# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import base64
from io import BytesIO
from dash.dependencies import Input, Output, State

from utils import make_cube_faces
from side_controls import img_plot_controls

external_stylesheets = [
    # 'https://codepen.io/chriddyp/pen/bWLwgP.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

state = {
    "image": {
        "filename": None,
        "img": None,
        "shape": (None, None, None)
    }
}

app.layout = html.Div(
    className="main-layout",
    children=[
        html.Div(
            children=[
                html.H1(children='Cirrus IMG Viewer'),
                html.Div(children='''
                    Cirrus OCT raw IMG viewer.
                '''),
                html.Div(
                    id="img-filename",
                    children=""
                ),
                dcc.Graph(id='img-3d-plot')
            ],
            className="main-board"
        ),
        html.Div(
            className="side-board",
            children=[
                img_plot_controls
            ]
        )
    ]
)

plot_layout = {
    "title": "",
    "type": "surface",
    "margin": {"t": 0, "b": 0, "l": 0, "r": 0},
    # "font": {"size": 12, "color": "white"},
    "showlegend": False,
    "showscale": False,
    "plot_bgcolor": "#1D1D1D",
    "paper_bgcolor": "#1D1D1D",
    "scene": {
        # "xaxis": axis_template,
        # "yaxis": axis_template,
        # "zaxis": axis_template,
        "aspectratio": {"x": 1, "y": 1.2, "z": 1},
        "camera": {"eye": {"x": 1.25, "y": 1.25, "z": 1.25}},
        "annotations": [],
    },
}


@app.callback(
    [
        Output("i_min", "children"),
        Output("i_max", "children")
    ],
    [
        Input("i-slider", "value")
    ]
)
def update_i_slider(i_in):
    return i_in[0], i_in[1]


@app.callback(
    [
        Output("j_min", "children"),
        Output("j_max", "children")
    ],
    [
        Input("j-slider", "value")
    ]
)
def update_j_slider(i_in):
    return i_in[0], i_in[1]


@app.callback(
    [
        Output("k_min", "children"),
        Output("k_max", "children")
    ],
    [
        Input("k-slider", "value")
    ]
)
def update_k_slider(i_in):
    return i_in[0], i_in[1]

def update_surface_plot(i_in, j_in, k_in):
    i, i_l = i_in
    j, j_l = j_in
    k, k_l = k_in
    data = make_cube_faces(state['image']['img'], i, i_l, j, j_l, k, k_l)
    return {
        "data": data,
        'layout': plot_layout
    }

@app.callback(
    [
        Output('i-slider', 'max'),
        Output('j-slider', 'max'),
        Output('k-slider', 'max'),
        Output('i-slider', 'value'),
        Output('j-slider', 'value'),
        Output('k-slider', 'value'),
        Output('img-filename', 'children')
    ],
    [
        Input('upload-img-data', 'contents'),
    ],
    [
        State('upload-img-data', 'filename')
    ]
)
def update_img_state(img, filename):
    if img is None:
        return 199, 1024, 199, [0, 199], [0, 1023], [0, 199], ""
    elif filename[0] != state['image']['filename']:
        img = base64.b64decode(img[0].split("base64,")[1])
        img = BytesIO(img)
        img = np.frombuffer(img.getbuffer(), np.uint8)

        if filename[0].endswith('.img'):
            if len(img) == 67108864:
                img = img.reshape(128, 1024, 512)
                state['image']['shape'] = (128, 1024, 512)
            elif len(img) == 40960000:
                img = img.reshape(200, 1024, 200)
                state['image']['shape'] = (200, 1024, 200)
            else:
                raise ValueError()
            state['image']['filename'] = filename[0]
            state['image']['img'] = img
        else:
            raise ValueError()
    
    return state['image']['shape'][0] - 1, state['image']['shape'][1] - 1, state['image']['shape'][2] - 1, \
        [0, state['image']['shape'][0] -  1], [0, state['image']['shape'][1] - 1], [0, state['image']['shape'][2] - 1], \
        state['image']['filename']


@app.callback(
    Output('img-3d-plot', 'figure'),
    [
        Input('i-slider', 'value'),
        Input('j-slider', 'value'),
        Input('k-slider', 'value'),
        Input('img-filename', 'children')
    ]
)
def update_surface_plot_data(i_in, j_in, k_in, filename):
    if filename == "":
        return {
            "data": [],
            'layout': plot_layout
        }

    return update_surface_plot(i_in, j_in, k_in)


if __name__ == '__main__':
    app.run_server(debug=True)
