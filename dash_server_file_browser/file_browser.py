from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import dash_bootstrap_components as dbc
from dash import ALL, MATCH, Input, Output, State, callback, ctx, dcc, html
from dash.exceptions import PreventUpdate


@dataclass
class FileBrowserAIOCallbackConfig:
    """Configuration of the FileBrowserAIO used in its callbacks."""

    aio_id: str
    """AIO id of the FileBrowserAIO instance."""
    base_path: str
    """Base path of the FileBrowserAIO instance."""
    display_relative: bool
    """Display the current path relative to the base path."""


class FileBrowserAIO(html.Div):
    """Modal file browser all-in-one component based on Dash Bootstrap Components.

    Currently only directories can be selected. The selected path will be stored in the
    `dcc.Store` component with the id `FileBrowserAIO.IDs.selected_path(aio_id)`. This
    path is an absolute path.

    Args:
        aio_id (str): ID for the AIO instance used to generate the component IDs.
        base_path (str): Base path for the file browser. The user can only navigate
            within this path.
        modal_title (str, optional): Title displayed on the `dbc.ModalHeader`.
            Defaults to "File Browser".
        close_button_text (str, optional): Text for the close button.
            Defaults to "Select".
        color (str, optional): Bootstrap theme color used for buttons and icons.
            Defaults to "primary".
        display_relative (bool, optional): Display the current path only relative to
            `base_path`. Defaults to True.
        modal_props (dict, optional): Passthrough properties to the `dbc.Modal`
            component. Defaults to None.
        modal_header_props (dict, optional): Passthrough properties to the
            `dbc.ModalHeader` component. Defaults to None.
        modal_title_props (dict, optional): Passthrough properties to the
            `dbc.ModalTitle` component. Defaults to None.
        modal_body_props (dict, optional): Passthrough properties to the `dbc.ModalBody`
            component. Defaults to None.
        modal_footer_props (dict, optional): Passthrough properties to the
            `dbc.ModalFooter` component. Defaults to None.
        modal_close_button_props (dict, optional): Passthrough properties to the
            `dbc.Button` component for closing the modal. Defaults to None.
    """

    class IDs:
        """ID generator for the ``FileBrowserAIO`` sub-components."""

        @staticmethod
        def button_base_directory(aio_id: str):
            """ID for the button to go to the base directory."""
            return {
                "component": "FileBrowserAIO",
                "subcomponent": "button_base_directory",
                "aio_id": aio_id,
            }

        @staticmethod
        def button_parent_directory(aio_id: str):
            """ID for the button to go to the current paths parent directory."""
            return {
                "component": "FileBrowserAIO",
                "subcomponent": "button_parent_directory",
                "aio_id": aio_id,
            }

        @staticmethod
        def button_select_path_and_close_modal(aio_id: str):
            """ID for the button to select the current path and close the modal."""
            return {
                "component": "FileBrowserAIO",
                "subcomponent": "button_select_path_and_close_modal",
                "aio_id": aio_id,
            }

        @staticmethod
        def display_current_directory(aio_id: str):
            """ID for the div displaying the current directory."""
            return {
                "component": "FileBrowserAIO",
                "subcomponent": "display_current_directory",
                "aio_id": aio_id,
            }

        @staticmethod
        def display_directory_content(aio_id: str):
            """ID for the div displaying the content of the current directory."""
            return {
                "component": "FileBrowserAIO",
                "subcomponent": "display_directory_content",
                "aio_id": aio_id,
            }

        @staticmethod
        def modal(aio_id: str):
            """ID genarator for the ``dbc.Modal`` component."""
            return {
                "component": "FileBrowserAIO",
                "subcomponent": "modal",
                "aio_id": aio_id,
            }

        @staticmethod
        def selected_path(aio_id: str):
            """ID for the ``dcc.Store`` component that stores the selected path.

            This will only be updated when the user selects and closes the modal.
            """
            return {
                "component": "FileBrowserAIO",
                "subcomponent": "selected_path",
                "aio_id": aio_id,
            }

        @staticmethod
        def aio_config(aio_id: str):
            """Internal ID for the ``dcc.Store`` component to store the AIOs config.

            This is used to access config properties in the callbacks.
            """
            return {
                "component": "FileBrowserAIO",
                "subcomponent": "__aio_config",
                "aio_id": aio_id,
            }

        @staticmethod
        def current_path(aio_id: str):
            """Internal ID for the ``dcc.Store`` component to store the current path."""
            return {
                "component": "FileBrowserAIO",
                "subcomponent": "__current_path",
                "aio_id": aio_id,
            }

        @staticmethod
        def clickable_file_item(aio_id: str, *, path: str):
            """Internal ID for the clickable directory item."""
            return {
                "component": "FileBrowserAIO",
                "subcomponent": "__clickable_directory_item",
                "aio_id": aio_id,
                "path": path,
            }

    IDs = IDs

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        aio_id: str,
        base_path: str,
        *,
        modal_title: str = "File Browser",
        close_button_text: str = "Select",
        color: str = "primary",
        display_relative: bool = True,
        # Sub-component properties
        modal_props=None,
        modal_header_props=None,
        modal_title_props=None,
        modal_body_props=None,
        modal_footer_props=None,
        modal_close_button_props=None,
    ):
        # Merge user-supplied properties into the default properties
        modal_props = {
            "is_open": False,
            "backdrop": False,
            "size": "lg",
            "scrollable": True,
        }
        modal_props.update(modal_props if modal_props else {})

        modal_header_props = modal_header_props if modal_header_props else {}
        modal_title_props = modal_title_props if modal_title_props else {}
        modal_body_props = modal_body_props if modal_body_props else {}
        modal_footer_props = modal_footer_props if modal_footer_props else {}
        modal_close_button_props = (
            modal_close_button_props if modal_close_button_props else {}
        )

        # Validate the base path
        if not base_path or not Path(base_path).exists():
            raise FileNotFoundError(
                f"Base path '{base_path}' does not exist or is not a valid path."
            )

        aio_config = FileBrowserAIOCallbackConfig(
            aio_id=aio_id,
            base_path=base_path,
            display_relative=display_relative,
        )

        # Define the component's layout
        super().__init__(
            dbc.Modal(
                [
                    dcc.Store(
                        id=self.IDs.aio_config(aio_id),
                        data=aio_config.__dict__,
                    ),
                    dcc.Store(id=self.IDs.current_path(aio_id), data=base_path),
                    dcc.Store(id=self.IDs.selected_path(aio_id), data=None),
                    dbc.ModalHeader(
                        dbc.ModalTitle(modal_title, **modal_title_props),
                        **modal_header_props,
                    ),
                    dbc.ModalBody(
                        dbc.Stack(
                            [
                                dbc.Stack(
                                    [
                                        dbc.Button(
                                            class_name="fa fa-house",
                                            id=self.IDs.button_base_directory(aio_id),
                                            color=color,
                                        ),
                                        dbc.Button(
                                            class_name="fa fa-arrow-up",
                                            id=self.IDs.button_parent_directory(aio_id),
                                            color=color,
                                        ),
                                        html.Div(
                                            id=self.IDs.display_current_directory(
                                                aio_id
                                            )
                                        ),
                                    ],
                                    direction="horizontal",
                                    gap=2,
                                ),
                                html.Hr(),
                                html.Div(
                                    id=self.IDs.display_directory_content(aio_id),
                                ),
                            ]
                        ),
                        **modal_body_props,
                    ),
                    dbc.ModalFooter(
                        dbc.Button(
                            close_button_text,
                            id=self.IDs.button_select_path_and_close_modal(aio_id),
                            className="ml-auto",
                            color=color,
                        ),
                        **modal_footer_props,
                    ),
                ],
                id=self.IDs.modal(aio_id),
                **modal_props,
            )
        )

    @callback(
        Output(IDs.display_current_directory(MATCH), "children"),
        Input(IDs.current_path(MATCH), "data"),
        State(IDs.aio_config(MATCH), "data"),
    )
    @staticmethod
    def display_current_directory(current_path_: str, aio_config_: dict):
        """Display the current directory."""
        if not current_path_:
            raise PreventUpdate

        # Dezerialize the current path and aio_config
        current_path = Path(current_path_)
        aio_config = FileBrowserAIOCallbackConfig(**aio_config_)

        if aio_config.display_relative:
            return current_path.relative_to(aio_config.base_path).as_posix()

        return current_path.as_posix()

    @callback(
        Output(IDs.display_directory_content(MATCH), "children"),
        Input(IDs.current_path(MATCH), "data"),
        State(IDs.aio_config(MATCH), "data"),
        # prevent_initial_call=True,
    )
    @staticmethod
    def display_directory_content(current_path_: str, aio_config_: dict):
        """Display the content of the current directory."""
        # Dezerialize the current path and aio_config
        current_path = Path(current_path_)
        aio_config = FileBrowserAIOCallbackConfig(**aio_config_)
        if not current_path or not current_path.exists():
            raise PreventUpdate

        # Get directory content
        files: list[Path] = []
        sub_directories: list[Path] = []
        for item in current_path.iterdir():
            if item.is_file():
                files.append(item)

            elif item.is_dir():
                sub_directories.append(item)

        # Sort files and directories
        files.sort()
        sub_directories.sort()

        # Return content as html unsorted list with clickable sub directories
        return html.Ul(
            [
                html.Li(
                    html.A(
                        str(sub_dir.name),
                        style={"fontWeight": "bold"},
                        id=FileBrowserAIO.IDs.clickable_file_item(
                            aio_config.aio_id, path=str(sub_dir)
                        ),
                        href="#",
                    )
                )
                for sub_dir in sub_directories
            ]
            + [html.Li(str(file.name)) for file in files]
        )

    @callback(
        Output(IDs.current_path(MATCH), "data", allow_duplicate=True),
        Input(IDs.button_base_directory(MATCH), "n_clicks"),
        State(IDs.aio_config(MATCH), "data"),
        prevent_initial_call=True,
    )
    @staticmethod
    def navigate_base_directory(n_clicks: Optional[int], aio_config_: dict):
        """Navigate to the base directory."""
        if n_clicks is None:
            raise PreventUpdate

        # Dezerialize the aio_config
        aio_config = FileBrowserAIOCallbackConfig(**aio_config_)
        # Navigate to the base directory
        return aio_config.base_path

    @callback(
        Output(IDs.current_path(MATCH), "data", allow_duplicate=True),
        Input(IDs.button_parent_directory(MATCH), "n_clicks"),
        [
            State(IDs.current_path(MATCH), "data"),
            State(IDs.aio_config(MATCH), "data"),
        ],
        prevent_initial_call=True,
    )
    @staticmethod
    def navigate_parent_directory(
        n_clicks: Optional[int],
        current_path_: str,
        aio_config_: dict,
    ):
        """Navigate to the parent directory."""
        if not n_clicks:
            raise PreventUpdate

        # Dezerialize the current path and aio_config
        current_path = Path(current_path_)
        aio_config = FileBrowserAIOCallbackConfig(**aio_config_)

        # Check if the current path is the base path
        if current_path.resolve() == Path(aio_config.base_path).resolve():
            raise PreventUpdate

        # Navigate to the parent directory
        return current_path.parent.as_posix()

    @callback(
        Output(IDs.current_path(MATCH), "data", allow_duplicate=True),
        Input(IDs.clickable_file_item(MATCH, path=ALL), "n_clicks"),
        prevent_initial_call=True,
    )
    @staticmethod
    def navigate_sub_directory(n_clicks: Optional[int]):
        """Update the current path when a directory is clicked."""
        if not n_clicks or set(n_clicks) == {None}:
            raise PreventUpdate

        return ctx.triggered_id["path"]

    @callback(
        [Output(IDs.modal(MATCH), "is_open"), Output(IDs.selected_path(MATCH), "data")],
        Input(IDs.button_select_path_and_close_modal(MATCH), "n_clicks"),
        State(IDs.current_path(MATCH), "data"),
    )
    @staticmethod
    def select_current_path_and_close_modal(n_clicks: Optional[int], current_path: str):
        """Select the current path and close the modal."""
        if not n_clicks:
            raise PreventUpdate

        return False, current_path
