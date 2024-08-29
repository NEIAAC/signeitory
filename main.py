import os
import logging
import copy
import dotenv
import pandas as pd
import pymupdf

def get_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        logging.critical(f"Environment variable for {var_name} is not set")
        exit(1)
    return value

def read_table(table_path: str) -> list[list[str]]:
    if table_path.endswith(".csv"):
        table = pd.read_csv(table_path, index_col=False)
    elif table_path.endswith(".xlsx"):
        table = pd.read_excel(table_path, index_col=False)
    else:
        logging.critical("Table data file type extension not supported")
        exit(1)
    if len(table.columns) > 1:
        logging.critical("Table data file has more than one column")
        exit(1)
    return table.values.tolist()

def read_file_data(file_path: str) -> bytes:
    try:
        file = pymupdf.open(file_path)
        file_data = file.convert_to_pdf()
        return file_data
    except Exception as e:
        logging.critical(f"Failed to open file: {e}")
        exit(1)

def main():
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=logging.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler("e-neiler.log"),
            logging.StreamHandler(),
        ],
    )

    logging.info("Process started")

    # Load environment variables
    dotenv.load_dotenv(dotenv.find_dotenv())

    file_path = get_env("FILE_PATH")
    table_path = get_env("TABLE_PATH")
    output_path = get_env("OUTPUT_PATH")

    logging.info(f"Loaded environment variables")

    CONVERTED_EXTENSION = "pdf"

    table = read_table(table_path)

    logging.info(f"Loaded table data")

    file_data = read_file_data(file_path)

    logging.info(f"Loaded base file")

    total: int = 0
    successful: int = 0
    for row in table:
        total += 1

        file: pymupdf.Document = pymupdf.open(CONVERTED_EXTENSION, file_data)

        #----------------------------CONFIGURATION----------------------------#

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

        #---------------------------------------------------------------------#

        try:
            font_name = os.path.basename(font_file_path)
            page = file[page_number]
            page.insert_font(fontfile=font_file_path, fontname=font_name)
            page.insert_text(pymupdf.Point(coordinate_x, coordinate_y),
                             text,
                             fontname=font_name,
                             fontsize=font_size,
                             color=color,
                             rotate=rotation)
        except Exception as e:
            logging.error(f"[{total}] Failed to write {text}: {e}")
            continue

        try:
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            file.save(f"{output_path}/{text}.{CONVERTED_EXTENSION}")
            successful += 1
            logging.info(f"[{total}] Wrote {text} on file")
        except Exception as e:
            logging.error(f"[{total}] Failed to write {text} output: {e}")
            continue

    logging.info(f"Successfully wrote {successful} of {total} files")

    logging.info("Process finished")

if __name__ == "__main__":
    main()
