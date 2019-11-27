import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from app import app
from state import StateSingleton


def stereo_controls(slider_controls=[199, 1023, 199]):
    i, j, k = [0, 0, 0]
    i_l, j_l, k_l = slider_controls
    return html.Div(children=[
        html.Div("Inspect Faces:"),
        dcc.Dropdown(
            id="inspect-faces-control",
            options=[
                {'label': 'Show All faces', 'value': 'all'},
                {'label': 'Inspect Selected face', 'value': 'custom'},
            ],
            value='all',
            style={'color': "#141414"}
        ),
        dcc.Checklist(
            id="inspect-face-control",
            options=[
                {'label': 'XY Up', 'value': 'xy-up'},
                {'label': 'XY Down', 'value': 'xy-down'},
                {'label': 'YZ Up', 'value': 'yz-up'},
                {'label': 'YZ Down', 'value': 'yz-down'},
                {'label': 'ZX Up', 'value': 'zx-up'},
                {'label': 'ZX Down', 'value': 'zx-down'}
            ],
            value=['xy-up', 'xy-down', 'yz-up', 'yz-down', 'zx-up', 'zx-down'],
            labelStyle={'display': 'block'}
        ),
        html.Div("x-axis"),
        dcc.RangeSlider(
            id='i-slider',
            count=1,
            min=i,
            max=i_l,
            step=1,
            value=[i, i_l],
            allowCross=False
        ),
        html.Div(
            className="img-axis-control",
            children=[
                html.Div(str(i), id='i_min'),
                html.Div(str(i_l), id='i_max'),
            ]
        ),
        html.Div("y-axis"),
        dcc.RangeSlider(
            id='j-slider',
            count=1,
            min=j,
            max=j_l,
            step=1,
            value=[j, j_l],
            allowCross=False
        ),
        html.Div(
            className="img-axis-control",
            children=[
                html.Div(str(j), id='j_min'),
                html.Div(str(j_l), id='j_max'),
            ]
        ),
        html.Div("z-axis"),
        dcc.RangeSlider(
            id='k-slider',
            count=1,
            min=k,
            max=k_l,
            step=1,
            value=[k, k_l],
            allowCross=False
        ),
        html.Div(
            className="img-axis-control",
            children=[
                html.Div(str(k), id='k_min'),
                html.Div(str(k_l), id='k_max'),
            ]
        )
    ])


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
