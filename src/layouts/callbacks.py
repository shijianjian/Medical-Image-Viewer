import numpy as np
import base64
from io import BytesIO
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import IncorrectTypeException, PreventUpdate

from state import StateSingleton
from utils.stereo_utils import update_surface_plot, get_plot_layout


def register_callbacks(app):
    @app.callback(
        Output('slider-control-state', 'data'),
        [
            Input("i-slider", "value"),
            Input("j-slider", "value"),
            Input("k-slider", "value")
        ]
    )
    def update_slider_state(i_in, j_in, k_in):
        print(i_in, j_in, k_in)
        controls = {}
        controls['i_min'] = i_in[0]
        controls['i_max'] = i_in[1]
        controls['j_min'] = j_in[0]
        controls['j_max'] = j_in[1]
        controls['k_min'] = k_in[0]
        controls['k_max'] = k_in[1]
        return controls

    @app.callback(
        [
            Output("i-slider", "value"),
            Output("j-slider", "value"),
            Output("k-slider", "value"),
            Output('i-slider', 'max'),
            Output('j-slider', 'max'),
            Output('k-slider', 'max'),
        ],
        [
            Input('img-3d-state', 'data')
        ]
    )
    def update_slider_range(img):
        # Use modified_timestamp to get the initial value
        if img is None:
            i_m = 20
            j_m = 20
            k_m = 20
        else:
            i_m = img['shape'][0] - 1
            j_m = img['shape'][1] - 1
            k_m = img['shape'][2] - 1
        return [0, i_m], [0, j_m], [0, k_m], i_m, j_m, k_m

    @app.callback(
        Output('img-3d-state', 'data'),
        [
            Input('upload-img-data', 'contents'),
        ],
        [
            State('upload-img-data', 'filename')
        ]
    )
    def update_img_3d_state(img, filename):
        if img is None:
            raise PreventUpdate
        stateIns = StateSingleton()
        state = stateIns.get_state()
        print("Recieving file:", filename)
        img_state = {}
        img = base64.b64decode(img[0].split("base64,")[1])
        img = BytesIO(img)
        img = np.frombuffer(img.getbuffer(), np.uint8)

        if filename[0].endswith('.img'):
            if len(img) == 67108864:
                img_state['shape'] = (128, 1024, 512)
            elif len(img) == 40960000:
                img_state['shape'] = (200, 1024, 200)
            else:
                raise IncorrectTypeException
            img_state['filename'] = filename[0]
            state['data'] = img.reshape(img_state['shape'])
        else:
            raise IncorrectTypeException
        return img_state

    @app.callback(
        [
            Output("inspect-face-control", "style"),
            Output("face-control-state", "data")
        ],
        [
            Input("inspect-faces-control", "value"),
            Input("face-control-state", "modified_timestamp")
        ],
        [
            State("face-control-state", "data"),
            State("inspect-face-control", "value")
        ]
    )
    def update_faces_control(value, _, data, faces):
        face_state = {}
        face_state['mode'] = value
        if value == "all":
            face_state['faces'] = ['xy-up', 'xy-down', 'yz-up', 'yz-down', 'zx-up', 'zx-down']
            return {"display": "none"}, face_state
        else:
            if data is not None:
                face_state['faces'] = data['faces']
            else:
                face_state['faces'] = faces
            return {"display": "block"}, data

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
        Output('img-3d-plot', 'figure'),
        [
            Input('img-3d-state', 'data'),
            Input('slider-control-state', 'data'),
            Input("face-control-state", "data")
        ]
    )
    def update_surface_plot_data(img_state, slider_control, face_control):
        stateIns = StateSingleton()
        state = stateIns.get_state()
        state['image'] = img_state
        state['controls']['slider'] = slider_control
        state['controls']['faces'] = face_control
        print(state['controls'])
        print(state['image'])
        stateIns.set_state(state)
        if img_state is None:
            print("Return Empty Graph.")
            s = {}
            s['image'] = {}
            s['image']['shape'] = (20, 20, 20)
            res = {
                "data": [],
                'layout': get_plot_layout(s)
            }
        else:
            print("Graph Calculated.")
            res = update_surface_plot(stateIns.get_state())
        return res
