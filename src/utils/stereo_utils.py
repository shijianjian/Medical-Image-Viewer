import numpy as np


def make_cube_face(x, y, z, surfacecolor, name="face"):
    return {
        "type": "surface",
        "name": name,
        "x": x,
        "y": y,
        "z": z,
        "showscale": False,
        "surfacecolor": surfacecolor,
        "hoverinfo": 'closest'
    }


def get_plot_layout(state):
    return {
        "title": "",
        "type": "surface",
        "margin": {"t": 0, "b": 0, "l": 0, "r": 0},
        # "font": {"size": 12, "color": "white"},
        "showlegend": False,
        "showscale": False,
        "plot_bgcolor": "#1D1D1D",
        "paper_bgcolor": "#1D1D1D",
        "dragmode": "orbit",
        "scene": {
            "xaxis": {"range": [0, state['image']['shape'][0]]},
            "yaxis": {"range": [0, state['image']['shape'][1]]},
            "zaxis": {"range": [0, state['image']['shape'][2]]},
            "aspectratio": {"x": 1, "y": 1.2, "z": 1},
            "camera": {"eye": {"x": 1.25, "y": 1.25, "z": 1.25}},
            "annotations": [],
        },
    }


def make_cube_face_YZ(img, x, y, z, i, i_l):
    Y, Z = np.meshgrid(y, z)
    xm = i * np.ones(Y.shape)
    xM = i_l * np.ones(Y.shape)
    trace_xm = make_cube_face(x=xm, y=Y, z=Z, surfacecolor=np.expand_dims(img[i].T, axis=-1), name="x_min")
    trace_xM = make_cube_face(x=xM, y=Y, z=Z, surfacecolor=np.expand_dims(img[i_l].T, axis=-1), name="x_max")
    return [trace_xm, trace_xM]


def make_cube_face_ZX(img, x, y, z, j, j_l):
    Z, X = np.meshgrid(z, x)
    ym = j * np.ones(X.shape)
    yM = j_l * np.ones(X.shape)
    trace_ym = make_cube_face(x=X, y=ym, z=Z, surfacecolor=np.expand_dims(img[:, j, :], axis=-1), name="y_min")
    trace_yM = make_cube_face(x=X, y=yM, z=Z, surfacecolor=np.expand_dims(img[:, j_l, :], axis=-1), name="y_max")
    return [trace_ym, trace_yM]


def make_cube_face_XY(img, x, y, z, k, k_l):
    X, Y = np.meshgrid(x, y)
    zm = k * np.ones(X.shape)
    zM = k_l * np.ones(X.shape)
    trace_zm = make_cube_face(x=X, y=Y, z=zm, surfacecolor=np.expand_dims(img[:, :, k].T, axis=-1), name="z_min")
    trace_zM = make_cube_face(x=X, y=Y, z=zM, surfacecolor=np.expand_dims(img[:, :, k_l].T, axis=-1), name="z_max")
    return [trace_zm, trace_zM]