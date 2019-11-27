# -*- coding: utf-8 -*-
import numpy as np
from io import BytesIO

from state import StateSingleton
from app import app
from utils.stereo_utils import make_cube_face_YZ, make_cube_face_XY, make_cube_face_ZX, get_plot_layout


def update_surface_plot(i_in, j_in, k_in, state):
    i, i_l = i_in
    j, j_l = j_in
    k, k_l = k_in

    stateIns = StateSingleton()
    state = stateIns.get_state()
    img = state['image']['img']
    x = np.linspace(i, i_l, i_l - i + 1)
    y = np.linspace(j, j_l, j_l - j + 1)
    z = np.linspace(k, k_l, k_l - k + 1)
    faces = state['controls']['faces']
    YZ = make_cube_face_YZ(img, x, y, z, i, i_l)
    state['plot']['YZ'] = YZ
    ZX = make_cube_face_ZX(img, x, y, z, j, j_l)
    state['plot']['ZX'] = ZX
    XY = make_cube_face_XY(img, x, y, z, k, k_l)
    state['plot']['XY'] = XY
    stateIns.set_state(state)

    data = []
    if "xy-up" in faces:
        data.append(XY[1])
    if "xy-down" in faces:
        data.append(XY[0])
    if "yz-up" in faces:
        data.append(YZ[1])
    if "yz-down" in faces:
        data.append(YZ[0])
    if "zx-up" in faces:
        data.append(ZX[1])
    if "zx-down" in faces:
        data.append(ZX[0])
    return {
        "data": data,
        'layout': get_plot_layout(state)
    }


@app.callback(
    [
        Output('i-slider', 'max'),
        Output('j-slider', 'max'),
        Output('k-slider', 'max'),
        Output('i-slider', 'value'),
        Output('j-slider', 'value'),
        Output('k-slider', 'value'),
        Output('img-filename', 'children')
    ],
    [
        Input('upload-img-data', 'contents'),
    ],
    [
        State('upload-img-data', 'filename')
    ]
)
def update_img_state(img, filename):
    stateIns = StateSingleton()
    state = stateIns.get_state()
    if img is None:
        state['image']['filename'] = ""
        state['image']['shape'] = (200, 1024, 200)
    elif filename[0] != state['image']['filename']:
        img = base64.b64decode(img[0].split("base64,")[1])
        img = BytesIO(img)
        img = np.frombuffer(img.getbuffer(), np.uint8)

        if filename[0].endswith('.img'):
            if len(img) == 67108864:
                state['image']['shape'] = (128, 1024, 512)
            elif len(img) == 40960000:
                state['image']['shape'] = (200, 1024, 200)
            else:
                raise ValueError("Unknown length of IMG.")
            state['image']['filename'] = filename[0]
            state['image']['img'] = img.reshape(state['image']['shape'])
        else:
            raise ValueError()

    state['image']['i_min'] = 0
    state['image']['j_min'] = 0
    state['image']['k_min'] = 0
    state['image']['i_max'] = state['image']['shape'][0] - 1
    state['image']['j_max'] = state['image']['shape'][1] - 1
    state['image']['k_max'] = state['image']['shape'][2] - 1
    stateIns.set_state(state)
    return state['image']['i_max'], state['image']['j_max'], state['image']['k_max'], \
        [0, state['image']['i_max']], [0, state['image']['j_max']], [0, state['image']['k_max']], \
        state['image']['filename']


@app.callback(
    Output('img-3d-plot', 'figure'),
    [
        Input('i-slider', 'value'),
        Input('j-slider', 'value'),
        Input('k-slider', 'value'),
        Input("inspect-face-control", 'value'),
        Input('img-filename', 'children')
    ]
)
def update_surface_plot_data(i_in, j_in, k_in, faces, filename):
    stateIns = StateSingleton()
    state = stateIns.get_state()
    if filename == "":
        return {
            "data": [],
            'layout': get_plot_layout(state)
        }
    state['controls']['faces'] = faces
    res = update_surface_plot(i_in, j_in, k_in, state)
    state['image']['i_min'] = i_in[0]
    state['image']['j_min'] = j_in[0]
    state['image']['k_min'] = k_in[0]
    state['image']['i_max'] = i_in[1]
    state['image']['j_max'] = j_in[1]
    state['image']['k_max'] = j_in[1]
    stateIns.set_state(state)
    return res
