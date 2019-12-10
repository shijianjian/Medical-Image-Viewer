import dash_core_components as dcc
import dash_html_components as html


def stereo_controls(slider_controls=[20, 20, 20]):
    i, j, k = [0, 0, 0]
    i_l, j_l, k_l = slider_controls
    return html.Div(id="stereo-controls", children=[
        html.Div("Inspect Faces:"),
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
            value=['xy-up'],
            labelStyle={'display': 'block'}
        ),
        dcc.Store(id='slider-control-state', storage_type='session'),
        dcc.Store(id='face-control-state', storage_type='session'),
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


def plane_controls(slider_controls=[20, 20, 20]):
    i, j, k = [0, 0, 0]
    i_l, j_l, k_l = slider_controls
    return html.Div(id="plane-controls", children=[
        dcc.Store(id='slider-control-state_p', storage_type='session'),
        dcc.Store(id='face-control-state_p', storage_type='session'),
        html.Div("x-axis"),
        dcc.Slider(
            id='i-slider_p',
            min=i,
            max=i_l,
            value=i_l
        ),
        html.Div(
            className="img-axis-control",
            children=[
                html.Div(str(i_l), id='i_max_p'),
            ]
        ),
        html.Div("y-axis"),
        dcc.Slider(
            id='j-slider_p',
            min=j,
            max=j_l,
            value=j_l,
        ),
        html.Div(
            className="img-axis-control",
            children=[
                html.Div(str(j_l), id='j_max_p'),
            ]
        ),
        html.Div("z-axis"),
        dcc.Slider(
            id='k-slider_p',
            min=k,
            max=k_l,
            value=k_l
        ),
        html.Div(
            className="img-axis-control",
            children=[
                html.Div(str(k_l), id='k_max_p'),
            ]
        )
    ])


def cnn_inference_control():
    return html.Div(
        children=[
            html.H5("Model Inferencing"),
            html.Div(style={
                "border-style": "solid",
                "border-width": "1px",
                "border-color": "gray",
                "margin-top": "10px",
                "margin-bottom": "5px"
            }),
            html.Button('Load Model', id='load-model-btn'),
            html.Div(
                id='output-load-model-btn',
                children=[
                    html.Div(
                        id="output-load-model-text",
                        children=""
                    ),
                    html.Button('Get CAM', id='model-prediction-btn')
                ]
            )
        ]
    )