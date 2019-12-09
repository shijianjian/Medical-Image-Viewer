
import dash_core_components as dcc
import dash_html_components as html
import uuid

from layouts.side_controls_layout import stereo_controls, plane_controls


def main_side_controls():
    return html.Div(children=[
        dcc.Upload(
            id='upload-img-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        dcc.RadioItems(
            id="view-switch-radio",
            options=[
                {'label': '2D View', 'value': '2d'},
                {'label': '3D View', 'value': '3d'},
            ],
            value='2d'
        ),
        dcc.Store(id='view-switch-store', storage_type='session'),
        stereo_controls(),
        plane_controls()
    ], style={
        'minWidth': '100px'
    })


def main_plot_layout():
    session_id = str(uuid.uuid4())
    return html.Div(
        className="main-layout",
        children=[
            html.Div(session_id, id='session-id', style={'display': 'none'}),
            html.Div(
                children=[
                    html.H1(children='Cirrus IMG Viewer'),
                    dcc.Loading(
                        loading_state={'is_loading': True},
                        children=[
                            html.Div(
                                id="img-filename",
                                children=""
                            )
                        ],
                        type="dot"
                    ),
                    dcc.Store(id='img-3d-state', storage_type='memory'),
                    dcc.Graph(id='img-3d-plot'),
                    html.Div(id='img-2d-plot', children=[
                        html.Div(children=[
                            html.H4("x-axis"),
                            dcc.Graph(id='img-2d-plot-i'),
                        ], className="four columns"),
                        html.Div(children=[
                            html.H4("y-axis"),
                            dcc.Graph(id='img-2d-plot-j'),
                        ], className="four columns"),
                        html.Div(children=[
                            html.H4("z-axis"),
                            dcc.Graph(id='img-2d-plot-k'),
                        ], className="four columns")
                    ], className="row")
                ],
                className="main-board"
            ),
            html.Div(
                className="side-board",
                children=[
                    main_side_controls()
                ]
            )
        ]
    )
