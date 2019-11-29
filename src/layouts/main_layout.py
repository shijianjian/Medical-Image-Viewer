
import dash_core_components as dcc
import dash_html_components as html
import uuid

from layouts.side_controls_layout import stereo_controls


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
        stereo_controls()
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
                    html.Div(children='''
                        Cirrus OCT raw IMG viewer.
                    '''),
                    html.Div(
                        id="img-filename",
                        children=""
                    ),
                    dcc.Store(id='img-3d-state', storage_type='memory'),
                    dcc.Graph(id='img-3d-plot')
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
