
from layouts.main_layout import main_plot_layout
from layouts.callbacks import (
    register_sidebar_callbacks,
    register_stereo_control_callbacks,
    register_2d_plot_callbacks,
    register_3d_plot_callbacks,
    register_plane_control_callbacks
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
        register_sidebar_callbacks(app)
        register_plane_control_callbacks(app)
        register_stereo_control_callbacks(app)
        register_2d_plot_callbacks(app)
        register_3d_plot_callbacks(app)
    # For GUI application
    # from pyfladesk import init_gui
    # init_gui(app.server, window_title="Cirrus IMG Viewer")
    # For development
    app.config['suppress_callback_exceptions'] = True
    app.run_server(debug=True)
