import dash_core_components as dcc
import dash_html_components as html


def stereo_controls(slider_controls=[20, 20, 20]):
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
