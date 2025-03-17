# Signed and certified 📜🪶

With Signeitory it's as simple as possible to write text into a variety of file formats in bulk. The main purpose of the script is to generate massive amounts of custom certificates deriving from a common base.

We use [PyMu](https://github.com/pymupdf/PyMuPDF) under the hood for the massive amount of supported writeable file formats it allows, you can find the full feature list [here](https://pymupdf.readthedocs.io/en/latest/about.html).

## Usage 🚀

The app is automatically built by a pipeline with every release, so we provide **direct download links** for most operating systems.

- ### Windows 🪟

  - [Use this link to start the download.](https://github.com/NEIAAC/signeitory/releases/latest/download/Windows.zip)

  - Start the `main.exe` file **inside** the extracted folder by _double clicking_ on it, you can create a shortcut with any name you like for this file.

  - If you get a message from Windows with a warning that blocks the app from running, look for the **hidden** continue **button** and use it to **safely ignore** this warning.

- ### Linux 🐧

  - [Use this link to start the download.](https://github.com/NEIAAC/signeitory/releases/latest/download/Linux.zip)

  - Start the `main.bin` file **inside** the extracted folder, remember to **update the execution permissions** first by opening a terminal and running:

      ```shell
      chmod +x main.bin
      ./main.bin
      ```

  - This binary has been successfully tested on Ubuntu and Arch with both the Wayland and X11 protocols, other setups may need additional tinkering.

- ### MacOS 🍎

  - [Use this link to start the download.](https://github.com/NEIAAC/signeitory/releases/latest/download/MacOS.zip)

  - Start the extracted bundle app by _clicking_ on it.

  - If the app fails to open, go to [this support page](https://support.apple.com/guide/mac-help/open-a-mac-app-from-an-unknown-developer-mh40616/mac) and select your OS version at the top, then follow the instructions.

Further detailed usage instructions can be found in the [wiki](https://github.com/NEIAAC/signeitory/wiki) page.

See the [example](./example/) directory for demo files.

## Development 🛠️

- ### Requirements 📋

  - Python ([version](pyproject.toml#L5))

- ### Setup ⚙️

  - Clone the repository and open a terminal **inside** it.

  - Install the dependencies:

    ```shell
    # It is it recommend that a virtual environment is set before doing this!

    pip install .
    ```

  - Start the app:

    ```shell
    python src/main.py
    ```

- ### Tooling 🧰

  - Ruff is used as a linter and formatter:

    ```shell
    pip install .[check]
    ruff check --fix
    ruff format

    # To automatically lint and format on every commit install the pre-commit hooks:
    pre-commit install

    # When using pre-commit hooks, git commands will fail if any files are checked with errors.
    # Changed files must be added to the staged area and commited again to apply fixes.
    ```

  - PyTest and PyTest-Qt are used for testing:

    ```shell
    pip install .[test]
    pytest
    ```

  - Nuitka is used for cross-compiling to all supported platforms, with most details available in the build [workflow](./.github/workflows/build.yaml).
