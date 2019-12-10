import numpy as np
import base64
from io import BytesIO
from PIL import Image
import plotly.graph_objects as go
import cv2
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import IncorrectTypeException, PreventUpdate

from state import StateSingleton
from utils.stereo_utils import update_surface_plot, get_plot_layout


def register_sidebar_callbacks(app):
    @app.callback(
        [
            Output('img-3d-state', 'data'),
            Output('img-filename', 'children')
        ],
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
        return img_state, filename

    @app.callback(
        [
            Output('stereo-controls', 'style'),
            Output('plane-controls', 'style'),
            Output('img-3d-plot', 'style'),
            Output('img-2d-plot', 'style'),
            Output('view-switch-store', 'data')
        ],
        [
            Input("view-switch-radio", "value"),
        ]
    )
    def switch_controls(value):
        if value == "2d":
            return {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "block"}, {"view": value}
        if value == "3d":
            return {"display": "block"}, {"display": "none"}, {"display": "block"}, {"display": "none"}, {"view": value}


def register_stereo_control_callbacks(app):
    @app.callback(
        Output('slider-control-state', 'data'),
        [
            Input("i-slider", "value"),
            Input("j-slider", "value"),
            Input("k-slider", "value")
        ]
    )
    def update_slider_state(i_in, j_in, k_in):
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
            Input('img-3d-state', 'modified_timestamp')
        ],
        [
            State('img-3d-state', 'data')
        ]
    )
    def update_slider_range(_, img):
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
        [
            Output("i_min", "children"),
            Output("i_max", "children"),
            Output("j_min", "children"),
            Output("j_max", "children"),
            Output("k_min", "children"),
            Output("k_max", "children"),
        ],
        [
            Input("i-slider", "value"),
            Input("j-slider", "value"),
            Input("k-slider", "value"),
        ]
    )
    def update_slider_range(i_m, j_m, k_m):
        return i_m[0], i_m[1], j_m[0], j_m[1], k_m[0], k_m[1]

    @app.callback(
        Output("face-control-state", "data"),
        [
            Input("inspect-face-control", "value")
        ]
    )
    def update_faces_control(faces):
        face_state = {}
        face_state['faces'] = faces
        return face_state

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


def register_plane_control_callbacks(app):
    @app.callback(
        Output('slider-control-state_p', 'data'),
        [
            Input("i-slider_p", "value"),
            Input("j-slider_p", "value"),
            Input("k-slider_p", "value")
        ]
    )
    def update_slider_state(i_in, j_in, k_in):
        controls = {}
        controls['i'] = i_in
        controls['j'] = j_in
        controls['k'] = k_in
        return controls

    @app.callback(
        [
            Output('i-slider_p', 'max'),
            Output('j-slider_p', 'max'),
            Output('k-slider_p', 'max'),
            Output('i-slider_p', 'value'),
            Output('j-slider_p', 'value'),
            Output('k-slider_p', 'value')
        ],
        [
            Input('img-3d-state', 'modified_timestamp')
        ],
        [
            State('img-3d-state', 'data')
        ]
    )
    def update_slider_range(_, img):
        # Use modified_timestamp to get the initial value
        if img is None:
            i_m = 20
            j_m = 20
            k_m = 20
        else:
            i_m = img['shape'][0] - 1
            j_m = img['shape'][1] - 1
            k_m = img['shape'][2] - 1
        return i_m, j_m, k_m, i_m, j_m, k_m
    
    @app.callback(
        [
            Output('i_max_p', 'children'),
            Output('j_max_p', 'children'),
            Output('k_max_p', 'children'),
        ],
        [
            Input('i-slider_p', 'value'),
            Input('j-slider_p', 'value'),
            Input('k-slider_p', 'value'),
        ]
    )
    def update_slider_view(i_m, j_m, k_m):
        return i_m, j_m, k_m



def register_cnn_model_callbacks(app):
    @app.callback(
        [
            Output('output-load-model-btn', 'style'),
            Output('output-load-model-text', 'children'),
        ],
        [
            Input('load-model-btn', 'n_clicks')
        ]
    )
    def on_load_model_btn_clicked(click):
        if click is None:
            return {'display': 'none'}, ''
        # import tensorflow as tf
        # model = tf.saved_model.load("./assets/saved_model")
        return {'display': 'block'}, 'Not implemented.'


def register_2d_plot_callbacks(app):
    @app.callback(
        Output('img-2d-plot-i', 'figure'),
        [
            Input('img-3d-state', 'data'),
            Input('i-slider_p', 'value'),
            Input("face-control-state", "data"),
            Input('view-switch-store', 'data')
        ]
    )
    def update_2d_plot_data_i(img_state, slider_control, face_control, view_mode):
        return update_2d_plot_data_by_axis(img_state, slider_control, face_control, view_mode, "i")

    @app.callback(
        Output('img-2d-plot-j', 'figure'),
        [
            Input('img-3d-state', 'data'),
            Input('j-slider_p', 'value'),
            Input("face-control-state", "data"),
            Input('view-switch-store', 'data')
        ]
    )
    def update_2d_plot_data_i(img_state, slider_control, face_control, view_mode):
        return update_2d_plot_data_by_axis(img_state, slider_control, face_control, view_mode, "j")

    @app.callback(
        Output('img-2d-plot-k', 'figure'),
        [
            Input('img-3d-state', 'data'),
            Input('k-slider_p', 'value'),
            Input("face-control-state", "data"),
            Input('view-switch-store', 'data')
        ]
    )
    def update_2d_plot_data_i(img_state, slider_control, face_control, view_mode):
        return update_2d_plot_data_by_axis(img_state, slider_control, face_control, view_mode, "k")

    def update_2d_plot_data_by_axis(img_state, slider_control, face_control, view_mode, axis):
        if view_mode is None or view_mode["view"] == "3d":
            raise PreventUpdate
        layout = go.Layout(
            autosize=True,
            plot_bgcolor="#1D1D1D",
            paper_bgcolor="#1D1D1D",
            margin=dict(
                l=0,
                r=0,
                t=0,
                b=0,
                pad=0,
            ),
            xaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=False,
                showline=False,
                ticks='',
                showticklabels=False
            ),
            yaxis=dict(
                autorange=True,
                showgrid=False,
                zeroline=False,
                showline=False,
                ticks='',
                showticklabels=False
            )
        )
        if img_state is None or slider_control is None:
            res = {
                "data": [],
                'layout': layout
            }
        else:
            stateIns = StateSingleton()
            state = stateIns.get_state()
            if axis == "i":
                z = cv2.cvtColor(np.expand_dims(state['data'][slider_control], axis=-1), cv2.COLOR_GRAY2RGB)
            if axis == "j":
                z = cv2.cvtColor(np.expand_dims(state['data'][:, slider_control], axis=-1), cv2.COLOR_GRAY2RGB)
            if axis == "k":
                z = cv2.cvtColor(np.expand_dims(state['data'][:, :, slider_control].T, axis=-1), cv2.COLOR_GRAY2RGB)
            res = go.Figure(data=go.Image(z=z), layout=layout)
        return res


def register_3d_plot_callbacks(app):
    @app.callback(
        Output('img-3d-plot', 'figure'),
        [
            Input('img-3d-state', 'data'),
            Input('slider-control-state', 'data'),
            Input("face-control-state", "data"),
            Input('view-switch-store', 'data')
        ]
    )
    def update_surface_plot_data(img_state, slider_control, face_control, view_mode):
        if view_mode is None or view_mode["view"] == "2d":
            raise PreventUpdate
        stateIns = StateSingleton()
        state = stateIns.get_state()
        state['image'] = img_state
        state['controls']['slider'] = slider_control
        state['controls']['faces'] = face_control
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
