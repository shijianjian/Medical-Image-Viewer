from __init__ import create_flask, create_dash
from layouts.main_layout import main_plot_layout


# The Flask instance
server = create_flask()

# The Dash instance
app = create_dash(server)

# Push an application context so we can use Flask's 'current_app'
with server.app_context():
    # load the rest of our Dash app
    # from . import index

    # configure the Dash instance's layout
    app.layout = main_plot_layout()


if __name__ == '__main__':
    # For GUI application
    # from pyfladesk import init_gui
    # init_gui(app.server, window_title="Cirrus IMG Viewer")
    # For development
    app.run_server(debug=True)
