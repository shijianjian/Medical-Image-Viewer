# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np

external_stylesheets = [
    # 'https://codepen.io/chriddyp/pen/bWLwgP.css'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

img = np.fromfile("/raid/datasets/AIRI/OCT/PAIRI0002 20181006/PAIRI0002_Macular Cube 512x128_10-6-2018_10-53-39_OD_sn31091_cube_z.img", np.uint8)
img = img.reshape(128, 1024, 512)


def make_cube_face(x, y, z, surfacecolor, text='Plotly cube'):
    return {
        "type": "surface",
        "x": x,
        "y": y,
        "z": z,
        "surfacecolor": surfacecolor,
        "text": text,
        "hoverinfo": 'text'
    }


def get_surface_data(img, i, i_l, j, j_l, k, k_l):
    x = np.linspace(0, img.shape[0] - 1, img.shape[0])
    y = np.linspace(0, img.shape[1] - 1, img.shape[1])
    z = np.linspace(0, img.shape[2] - 1, img.shape[2])

    Y, Z = np.meshgrid(y, z)
    xm = np.zeros(Y.shape)
    xM = len(x) * np.ones(Y.shape)
    print(xm.shape, img[i].T.shape, img[i_l].T.shape)
    trace_xm = make_cube_face(x=xm, y=Y, z=Z, surfacecolor=np.expand_dims(img[i].T, axis=-1))
    trace_xM = make_cube_face(x=xM, y=Y, z=Z, surfacecolor=np.expand_dims(img[i_l].T, axis=-1))

    Z, X = np.meshgrid(z, x)
    ym = np.zeros(X.shape)
    yM = len(y) * np.ones(X.shape)
    print(ym.shape, img[:, j, :].shape, img[:, j_l, :].shape)
    trace_ym = make_cube_face(x=X, y=ym, z=Z, surfacecolor=np.expand_dims(img[:, j, :], axis=-1))
    trace_yM = make_cube_face(x=X, y=yM, z=Z, surfacecolor=np.expand_dims(img[:, j_l, :], axis=-1))

    X, Y = np.meshgrid(x, y)
    zm = np.zeros(X.shape)
    zM = len(z) * np.ones(X.shape)
    print(zm.shape, img[:, :, k].T.shape, img[:, :, k_l].T.shape)
    trace_zm = make_cube_face(x=X, y=Y, z=zm, surfacecolor=np.expand_dims(img[:, :, k].T, axis=-1))
    trace_zM = make_cube_face(x=X, y=Y, z=zM, surfacecolor=np.expand_dims(img[:, :, k_l].T, axis=-1))
    return [trace_zm, trace_zM, trace_xm, trace_xM, trace_ym, trace_yM]


app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': get_surface_data(img, i=0, i_l=127, j=0, j_l=1023, k=0, k_l=511),
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
