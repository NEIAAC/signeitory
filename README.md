# Signed and certified 📜🪶

With Signeitory it's as simple as possible to write text into a variety of file formats in bulk. The main purpose of the script is to generate massive amounts of custom certificates deriving from a common base.

We use [PyMu](https://github.com/pymupdf/PyMuPDF) under the hood for the massive amount of supported writeable file formats it allows, you can find the full feature list [here](https://pymupdf.readthedocs.io/en/latest/about.html).

## Requirements 📋

- Python 3.12.0+

## Usage 🚀

- Go to the `Releases` page of the GitHub repository.

- Under the `Assets` section for the latest release, click the entry with the name of your operating system.

- After downloading, extract the top content from the `.zip` to anywhere you want.

### Windows

- Run the `main.exe` file inside the extracted folder, you can create a shortcut with any name you like for this file.

### Linux

- Run the `main.bin` file inside the extracted folder. Note that compilation is targeted at Ubuntu (Wayland), other distributions may need additional actions to run the app.

### MacOS

- Run the bundle installer extracted from the `.zip` file.

## Development 🛠️

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

## Tooling 🧰

- Ruff is used as a linter and formatter:

  ```shell
  pip install .[check]
  ruff check --fix
  ruff format

  # To automatically lint and format on every commit install the pre-commit hooks:
  pre-commit install

  # Note that when using pre-commit the git command will fail if any files are linted or formatted. You will have to add them to the staged area again to apply the changes.
  ```

- PyTest and PyTest-Qt are used for testing:

  ```shell
  pip install .[test]
  pytest
  ```

- Nuitka is used for cross-compiling to all supported platforms:

  ```shell
  pip install .[build]
  nuitka <options>
  ```

  See the build [workflow](./.github/workflows/build.yaml) for a list of options used for each platform.
