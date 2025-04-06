# Dash Server File Browser

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Overview

`dash-server-file-browser` provides a simple AIO component for [Dash](https://github.com/plotly/dash) applications to browse directories and files on the server.
The componennt is implemented as a `Modal` component of [dash-bootstrap-components](https://github.com/facultyai/dash-bootstrap-components).

## Features

The current version of `dash-server-file-browser` supports the following features:

- Browsing the configured "base" directory and all its subdirectories
  - Users cannot navigate outside the defined "base" directory
- Selecting the current directory as component "output" via a `dcc.Store` component
- Two navigation buttons:
  - "Up" button to navigate to the parent directory
  - "Base" button to navigate to the base directory
- Option to display the current path as either a *relative* or *absolute* path

## Installation

To install `dash-server-file-browser`, use pip:

```bash
# Install the package from PyPI
pip install dash-server-file-browser
```

## Usage

[demo.py](https://github.com/Zoraiyo/dash-server-file-browser/blob/main/demo/demo.py) provides a simple example of how to use the `FileBrowserAIO` component in a `Dash` application.
It demonstrates how to setup the component with the necessary callbacks to open the
component and handle the selected directory.

## Contributing

Contributions are welcome! If you encounter any issues or have feature requests, please open an issue or submit a pull request on the [GitHub repository](https://github.com/Zoraiyo/dash-server-file-browser).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
