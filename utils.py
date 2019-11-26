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


def make_cube_face_YZ(img, x, y, z, i, i_l, x0, y0, z0):
    Y, Z = np.meshgrid(y, z)
    xm = i * np.ones(Y.shape)
    xM = i_l * np.ones(Y.shape)
    # Y, Z = np.meshgrid(y0, z0)
    trace_xm = make_cube_face(x=xm, y=Y, z=Z, surfacecolor=np.expand_dims(img[i].T, axis=-1), name="x_min")
    trace_xM = make_cube_face(x=xM, y=Y, z=Z, surfacecolor=np.expand_dims(img[i_l].T, axis=-1), name="x_max")
    return [trace_xm, trace_xM]


def make_cube_face_ZX(img, x, y, z, j, j_l, x0, y0, z0):
    Z, X = np.meshgrid(z, x)
    ym = j * np.ones(X.shape)
    yM = j_l * np.ones(X.shape)
    # Z, X = np.meshgrid(z0, x0)
    trace_ym = make_cube_face(x=X, y=ym, z=Z, surfacecolor=np.expand_dims(img[:, j, :], axis=-1), name="y_min")
    trace_yM = make_cube_face(x=X, y=yM, z=Z, surfacecolor=np.expand_dims(img[:, j_l, :], axis=-1), name="y_max")
    return [trace_ym, trace_yM]


def make_cube_face_XY(img, x, y, z, k, k_l, x0, y0, z0):
    X, Y = np.meshgrid(x, y)
    zm = k * np.ones(X.shape)
    zM = k_l * np.ones(X.shape)
    # X, Y = np.meshgrid(x0, y0)
    trace_zm = make_cube_face(x=X, y=Y, z=zm, surfacecolor=np.expand_dims(img[:, :, k].T, axis=-1), name="z_min")
    trace_zM = make_cube_face(x=X, y=Y, z=zM, surfacecolor=np.expand_dims(img[:, :, k_l].T, axis=-1), name="z_max")
    return [trace_zm, trace_zM]


def make_cube_faces(img, i, i_l, j, j_l, k, k_l):
    x0 = np.linspace(0, img.shape[0] - 1, img.shape[0])
    y0 = np.linspace(0, img.shape[1] - 1, img.shape[1])
    z0 = np.linspace(0, img.shape[2] - 1, img.shape[2])

    x = np.linspace(i, i_l, i_l - i + 1)
    y = np.linspace(j, j_l, j_l - j + 1)
    z = np.linspace(k, k_l, k_l - k + 1)

    return make_cube_face_YZ(img, x, y, z, i, i_l, x0, y0, z0) \
        + make_cube_face_ZX(img, x, y, z, j, j_l, x0, y0, z0) \
        + make_cube_face_XY(img, x, y, z, k, k_l, x0, y0, z0)
