
import dash_core_components as dcc
import dash_html_components as html
import uuid


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
        html.Div([
            dcc.Tabs(id="tabs", value='2d', children=[
                dcc.Tab(label='2D', value='2d'),
                dcc.Tab(label='3D', value='3d'),
            ]),
            html.Div(id="tabs-content")
        ]),
    ])


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