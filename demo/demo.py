from pathlib import Path

import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, callback, html
from dash.exceptions import PreventUpdate

from dash_server_file_browser import FileBrowserAIO, __version__

if __name__ == "__main__":
    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
        title="Demo: dash-server-file-browser",
    )

    app.layout = dbc.Container(
        [
            dbc.Stack(
                [
                    html.H1(f"Demo: dash-server-file-browser v{__version__}"),
                ],
                direction="horizontal",
            ),
            dbc.Button(
                "Open Directory Browser",
                id="btn-open-modal",
                n_clicks=0,
                color="primary",
            ),
            html.P(id="selected-path"),
            FileBrowserAIO(
                aio_id="demo",
                base_path=(Path(__file__).parent).as_posix(),
            ),
        ],
        class_name="p-3",
    )

    @callback(
        Output("selected-path", "children"),
        Input(FileBrowserAIO.IDs.selected_path("demo"), "data"),
    )
    def update_selected_path(selected_path):
        return f"Selected path: {selected_path}"

    @callback(
        Output(FileBrowserAIO.IDs.modal("demo"), "is_open", allow_duplicate=True),
        Input("btn-open-modal", "n_clicks"),
        prevent_initial_call=True,
    )
    def open_directory_browser(n_clicks):
        if not n_clicks:
            raise PreventUpdate

        return True

    app.run(debug=True)
