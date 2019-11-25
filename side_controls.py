
import dash
import dash_core_components as dcc
import dash_html_components as html

i = 0
i_l = 199
j = 0
j_l = 1023
k = 0
k_l = 199

img_plot_controls = html.Div(children=[
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
    ),
])
