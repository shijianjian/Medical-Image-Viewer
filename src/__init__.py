""" Structure comes from https://github.com/ned2/slapdash
"""

from flask import Flask
from dash import Dash
import sys
import os


# def get_dash_args_from_flask_config(config):
#     """Get a dict of Dash params that were specified """
#     # all arg names less 'self'
#     dash_args = set(inspect.getfullargspec(dash.Dash.__init__).args[1:])
#     return {key.lower(): val for key, val in config.items() if key.lower() in dash_args}


def resource_path(relative_path):
    # get absolute path to resource
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def create_flask():
    """Create the Flask instance for this application"""
    server = Flask(__package__)

    # load default settings
    # server.config.from_object(config_object)

    # load additional settings that will override the defaults in settings.py. eg
    # $ export {{ cookiecutter.project_slug.upper() }}_SETTINGS=/some/path/prod_settings.py
    # server.config.from_envvar(
    #     "{{ cookiecutter.project_slug.upper() }}_SETTINGS", silent=True
    # )

    return server


def create_dash(server):
    """Create the Dash instance for this application"""
    app = Dash(
        name=__package__,
        server=server,
        suppress_callback_exceptions=True,
        assets_folder=resource_path('assets'),
        # **get_dash_args_from_flask_config(server.config),
    )

    # Update the Flask config a default "TITLE" and then with any new Dash
    # configuration parameters that might have been updated so that we can
    # access Dash config easily from anywhere in the project with Flask's
    # 'current_app'
    server.config.setdefault("TITLE", "Dash")
    server.config.update({key.upper(): val for key, val in app.config.items()})

    app.title = server.config["TITLE"]

    if "SERVE_LOCALLY" in server.config:
        app.scripts.config.serve_locally = server.config["SERVE_LOCALLY"]
        app.css.config.serve_locally = server.config["SERVE_LOCALLY"]

    return app
