# Dash Server File Browser

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

*dash-server-file-browser* provides a simple AIO component for [Dash](https://github.com/plotly/dash) applications to browse directories and files on the server.
The componennt is implemented as a `Modal` component of [dash-bootstrap-components](https://github.com/facultyai/dash-bootstrap-components).

![dash-server-file-browser-demo](https://raw.githubusercontent.com/Zoraiyo/dash-server-file-browser/main/docs/images/demo.png)

## Features

The current version of *dash-server-file-browser* supports the following features:

- Browsing the configured "base" directory and all its subdirectories
  - Users cannot navigate outside the defined "base" directory
- Selecting the current directory as component "output" via a `dcc.Store` component
- Two navigation buttons:
  - "Up" button to navigate to the parent directory
  - "Home" button to navigate to the base directory
- Option to display the current path as either a *relative* or *absolute* path

## Installation

Install *dash-server-file-browser* from [PyPI](https://pypi.org/project/dash-server-file-browser/) using pip:

```sh
pip install dash-server-file-browser
```

## Usage

[demo.py](https://github.com/Zoraiyo/dash-server-file-browser/blob/main/demo/demo.py) provides a simple example of how to use the `FileBrowserAIO` component in a `Dash` application.
It demonstrates how to setup the component with the necessary callbacks to open the
component and handle the selected directory.

## Contributing

Contributions are welcome! If you encounter any issues or have feature requests, please open an [issue](https://github.com/Zoraiyo/dash-server-file-browser/issues) or submit a [pull request](https://github.com/Zoraiyo/dash-server-file-browser/pulls).

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/Zoraiyo/dash-server-file-browser/blob/main/LICENSE) file for details.
