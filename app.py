# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import base64
from io import BytesIO
from dash.dependencies import Input, Output, State

from utils import make_cube_face_YZ, make_cube_face_XY, make_cube_face_ZX, get_plot_layout
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
    },
    "plot": {
        "XY": None,
        "ZX": None,
        "YZ": None
    },
    "controls": {
        "i_min": None,
        "i_max": None,
        "j_min": None,
        "j_max": None,
        "k_min": None,
        "k_max": None
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


@app.callback(
    [
        Output("inspect-face-control", "style"),
        Output("inspect-face-control", "value")
    ],
    [
        Input("inspect-faces-control", "value")
    ]
)
def update_faces_control(value):
    if value == "all":
        state['controls']['faces'] = ['xy-up', 'xy-down', 'yz-up', 'yz-down', 'zx-up', 'zx-down']
        return {"display": "none"}, state['controls']['faces']
    else:
        return {"display": "block"}, state['controls']['faces']


@app.callback(
    [
        Output('i-slider', 'disabled'),
        Output('j-slider', 'disabled'),
        Output('k-slider', 'disabled')
    ],
    [
        Input("inspect-face-control", 'value'),
    ]
)
def update_slider_styles(value):
    if 'xy-up' in value or 'xy-down' in value:
        i_style = False
    else:
        i_style = True
    if 'yz-up' in value or 'yz-down' in value:
        j_style = False
    else:
        j_style = True
    if 'zx-up' in value or 'zx-down' in value:
        k_style = False
    else:
        k_style = True
    return j_style, k_style, i_style


def update_surface_plot(i_in, j_in, k_in, state):
    i, i_l = i_in
    j, j_l = j_in
    k, k_l = k_in

    img = state['image']['img']
    x = np.linspace(i, i_l, i_l - i + 1)
    y = np.linspace(j, j_l, j_l - j + 1)
    z = np.linspace(k, k_l, k_l - k + 1)
    faces = state['controls']['faces']
    YZ = make_cube_face_YZ(img, x, y, z, i, i_l)
    state['plot']['YZ'] = YZ
    ZX = make_cube_face_ZX(img, x, y, z, j, j_l)
    state['plot']['ZX'] = ZX
    XY = make_cube_face_XY(img, x, y, z, k, k_l)
    state['plot']['XY'] = XY

    data = []
    if "xy-up" in faces:
        data.append(XY[1])
    if "xy-down" in faces:
        data.append(XY[0])
    if "yz-up" in faces:
        data.append(YZ[1])
    if "yz-down" in faces:
        data.append(YZ[0])
    if "zx-up" in faces:
        data.append(ZX[1])
    if "zx-down" in faces:
        data.append(ZX[0])
    return {
        "data": data,
        'layout': get_plot_layout(state)
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
        state['image']['filename'] = ""
        state['image']['shape'] = (200, 1024, 200)
    elif filename[0] != state['image']['filename']:
        img = base64.b64decode(img[0].split("base64,")[1])
        img = BytesIO(img)
        img = np.frombuffer(img.getbuffer(), np.uint8)

        if filename[0].endswith('.img'):
            if len(img) == 67108864:
                state['image']['shape'] = (128, 1024, 512)
            elif len(img) == 40960000:
                state['image']['shape'] = (200, 1024, 200)
            else:
                raise ValueError("Unknown length of IMG.")
            state['image']['filename'] = filename[0]
            state['image']['img'] = img.reshape(state['image']['shape'])
        else:
            raise ValueError()

    state['image']['i_min'] = 0
    state['image']['j_min'] = 0
    state['image']['k_min'] = 0
    state['image']['i_max'] = state['image']['shape'][0] - 1
    state['image']['j_max'] = state['image']['shape'][1] - 1
    state['image']['k_max'] = state['image']['shape'][2] - 1
    return state['image']['i_max'], state['image']['j_max'], state['image']['k_max'], \
        [0, state['image']['i_max']], [0, state['image']['j_max']], [0, state['image']['k_max']], \
        state['image']['filename']


@app.callback(
    Output('img-3d-plot', 'figure'),
    [
        Input('i-slider', 'value'),
        Input('j-slider', 'value'),
        Input('k-slider', 'value'),
        Input("inspect-face-control", 'value'),
        Input('img-filename', 'children')
    ]
)
def update_surface_plot_data(i_in, j_in, k_in, faces, filename):
    if filename == "":
        return {
            "data": [],
            'layout': get_plot_layout(state)
        }
    state['controls']['faces'] = faces
    res = update_surface_plot(i_in, j_in, k_in, state)
    state['image']['i_min'] = i_in[0]
    state['image']['j_min'] = j_in[0]
    state['image']['k_min'] = k_in[0]
    state['image']['i_max'] = i_in[1]
    state['image']['j_max'] = j_in[1]
    state['image']['k_max'] = j_in[1]
    return res


if __name__ == '__main__':
    app.run_server(debug=True)
