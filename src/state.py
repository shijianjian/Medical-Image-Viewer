
class StateSingleton(object):
    def __init__(self):
        self.state = {
            "image": {
                "filename": None,
                "img": None,
                "shape": (None, None, None)
            },
            "plot": {
                "XY": None,
                "ZX": None,
                "YZ": None
            },
            "controls": {
                "i_min": None,
                "i_max": None,
                "j_min": None,
                "j_max": None,
                "k_min": None,
                "k_max": None
            }
        }

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = super().__new__(self)
        return self.instance

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
