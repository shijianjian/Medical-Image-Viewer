import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app

@app.callback(
    Output('tabs-content', 'children'),
    [
        Input('tabs', 'value')
    ]
)
def render_content(tab):
    print(tab)
    if tab == '2d':
        return html.Div([
            html.H3('Tab content 1')
        ])
    elif tab == '3d':
        return stereo_controls()


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
    stateIns = StateSingleton()
    state = stateIns.get_state()
    if value == "all":
        state['controls']['faces'] = ['xy-up', 'xy-down', 'yz-up', 'yz-down', 'zx-up', 'zx-down']
        stateIns.set_state(state)
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