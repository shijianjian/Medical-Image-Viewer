
from layouts.main_layout import main_plot_layout
from layouts.callbacks import (
    register_face_callbacks,
    register_slider_callbacks
)


if __name__ == '__main__':
    from state import AppSingleton

    appIns = AppSingleton()
    app = appIns.get_app()
    server = appIns.get_server()

    # Push an application context so we can use Flask's 'current_app'
    with server.app_context():
        # load the rest of our Dash app
        # from . import index

        # configure the Dash instance's layout
        app.layout = main_plot_layout()
        register_face_callbacks(app)
        register_slider_callbacks(app)
    # For GUI application
    # from pyfladesk import init_gui
    # init_gui(app.server, window_title="Cirrus IMG Viewer")
    # For development
    app.config['suppress_callback_exceptions'] = True
    app.run_server(debug=True)
