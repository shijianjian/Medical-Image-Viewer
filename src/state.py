from __init__ import create_flask, create_dash


class AppSingleton(object):
    def __new_app__(self):
        # The Flask instance
        self.server = create_flask()
        # The Dash instance
        self.app = create_dash(self.server)

    def __new__(self):
        if not hasattr(self, 'instance'):
            print("create app")
            self.instance = super().__new__(self)
            self.__new_app__(self)
        return self.instance

    def get_app(self):
        return self.app

    def get_server(self):
        return self.server


class StateSingleton(object):
    def __init_state__(self):
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
            print("create state")
            self.instance = super().__new__(self)
            self.__init_state__(self)
        return self.instance

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state
