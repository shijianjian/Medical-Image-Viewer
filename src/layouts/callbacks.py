import numpy as np
import base64
from io import BytesIO
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from state import StateSingleton
from utils.stereo_utils import update_surface_plot, get_plot_layout


def register_slider_callbacks(app):
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
        stateIns = StateSingleton()
        state = stateIns.get_state()
        state["controls"]['i_min'] = i_in[0]
        state["controls"]['i_max'] = i_in[1]
        stateIns.set_state(state)
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
        stateIns = StateSingleton()
        state = stateIns.get_state()
        state["controls"]['j_min'] = i_in[0]
        state["controls"]['j_max'] = i_in[1]
        stateIns.set_state(state)
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
        stateIns = StateSingleton()
        state = stateIns.get_state()
        state["controls"]['k_min'] = i_in[0]
        state["controls"]['k_max'] = i_in[1]
        stateIns.set_state(state)
        return i_in[0], i_in[1]

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
        stateIns = StateSingleton()
        state = stateIns.get_state()
        old_shape = state['image']['shape']
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

        if old_shape == state['image']['shape']:
            stateIns.set_state(state)
            return state['image']['shape'][0] - 1, state['image']['shape'][1] - 1, state['image']['shape'][2] - 1, \
                [state['controls']['i_min'], state['controls']['i_max']], \
                [state['controls']['j_min'], state['controls']['j_max']], \
                [state['controls']['k_min'], state['controls']['k_max']], \
                state['image']['filename']
        else:
            # Refresh slider only when shape updated
            state['controls']['i_min'] = 0
            state['controls']['j_min'] = 0
            state['controls']['k_min'] = 0
            state['controls']['i_max'] = state['image']['shape'][0] - 1
            state['controls']['j_max'] = state['image']['shape'][1] - 1
            state['controls']['k_max'] = state['image']['shape'][2] - 1
            stateIns.set_state(state)
            return state['controls']['i_max'], state['controls']['j_max'], state['controls']['k_max'], \
                [0, state['controls']['i_max']], [0, state['controls']['j_max']], [0, state['controls']['k_max']], \
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
        stateIns = StateSingleton()
        state = stateIns.get_state()
        state['controls']['faces'] = faces
        state['controls']['i_min'] = i_in[0]
        state['controls']['j_min'] = j_in[0]
        state['controls']['k_min'] = k_in[0]
        state['controls']['i_max'] = i_in[1]
        state['controls']['j_max'] = j_in[1]
        state['controls']['k_max'] = j_in[1]
        stateIns.set_state(state)
        if filename == "":
            return {
                "data": [],
                'layout': get_plot_layout(stateIns.get_state())
            }
        res = update_surface_plot(i_in, j_in, k_in, stateIns.get_state())
        return res


def register_face_callbacks(app):
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
        stateIns = StateSingleton()
        state = stateIns.get_state()
        if value == "all":
            state['controls']['faces'] = ['xy-up', 'xy-down', 'yz-up', 'yz-down', 'zx-up', 'zx-down']
            stateIns.set_state(state)
            return {"display": "none"}, state['controls']['faces']
        else:
            return {"display": "block"}, state['controls']['faces']
