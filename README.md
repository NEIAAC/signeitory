# Signed and certified 📜🪶

With Signeitory it's as simple as possible to write text into a variety of file formats in bulk. The main purpose of the script is to generate massive amounts of custom certificates deriving from a common base.

We use [PyMu](https://github.com/pymupdf/PyMuPDF) under the hood for the massive amount of supported writeable file formats it allows, you can find the full feature list [here](https://pymupdf.readthedocs.io/en/latest/about.html).

## Requirements 📋

- Python 3.10.0+

## Usage 🚀

- Clone the repository:

  ```shell
  git clone https://github.com/NEIAAC/signeitory.git
  ```

- Install the dependencies:

  ```shell
  pip install -r requirements.txt
  ```

- Create a `.env` file based on the provided `.env.example` file, with attention to the notes on each variable

- Edit the `table.csv` file in the `data` folder, or add your own, with a single column containing the text you want to write on each file

- Change text, font, color and placement:

  ```python
        #-------------CONFIGURATION-------------#

        text = row[0]

        # Font settings
        font_file_path = "assets/comic_sans.ttf"
        font_size = 24.0

        # RGB color, in range 0-1
        color = (0.2, 0.5, 0.7)

        # Coordinates, in pixels, to start writing text from
        coordinate_x = 200.0
        coordinate_y = 50.0

        # Angle to rotate written text by
        rotation = 0.0

        # Page to write on, 0 is first page
        # Only applies to files with pages, such as PDFs
        page_number = 0

        #---------------------------------------#
  ```

- Run the script:

  ```shell
  python main.py
  ```
