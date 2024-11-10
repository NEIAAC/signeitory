import os
from math import isnan
from typing import Tuple

from PySide6.QtCore import QThread, Signal
import pandas as pd
import openpyxl
import pymupdf

from utils.logger import logger

MAX_TEXT_LENGTH = 200


class WriterThread(QThread):
    outputSignal = Signal(str, str)

    def __init__(
        self,
        coordinateX: float,
        coordinateY: float,
        fontSize: float,
        rotation: int,
        pageNumber: int,
        color: Tuple[float, float, float],
        fontPath: str,
        documentPath: str,
        tablePath: str,
        outputPath: str,
    ):
        super().__init__()
        self.documentPath = documentPath
        self.tablePath = tablePath
        self.outputPath = outputPath
        self.fontPath = fontPath
        self.coordinateX = coordinateX
        self.coordinateY = coordinateY
        self.fontSize = fontSize
        self.color = color
        self.rotation = rotation
        self.pageNumber = pageNumber

    def output(self, text: str, level: str = "INFO"):
        logger.log(level, text)
        self.outputSignal.emit(text, level)

    def readTable(self) -> list[list[str]]:
        if self.tablePath.endswith(".csv"):
            self.output(
                f"Using pandas {pd.__version__} to read {self.tablePath}"
            )
            table = pd.read_csv(self.tablePath, index_col=False)
        elif self.tablePath.endswith(".xlsx"):
            self.output(
                f"Using pandas {pd.__version__} and openpyxl {openpyxl.__version__} to read {self.tablePath}"
            )
            table = pd.read_excel(self.tablePath, index_col=False)
        else:
            raise ValueError("Unsupported file extension")

        records = table.to_dict("records")
        headers = list(table.columns)

        # Convert NaN, which is parsed in empty cells, to empty string
        for record in records:
            for key in record:
                if type(record[key]) is float and isnan(record[key]):
                    record[key] = ""

        return records, headers

    def readDocument(self) -> bytes:
        try:
            self.output(
                f"Using PyMuPDF {pymupdf.__version__} to read {self.documentPath}"
            )
            file = pymupdf.open(self.documentPath)
            data = file.convert_to_pdf()
            return data
        except Exception as e:
            self.output(f"Failed to read file: {e}", "ERROR")
            raise

    def run(self):
        inputs = self.__dict__.copy()
        logger.info(f"Starting writer thread with input parameters: {inputs}")
        self.output("...")

        with logger.catch():
            if not os.path.isdir(self.outputPath):
                self.output(
                    f"Output directory {self.outputPath} not found or is not a directory",
                    "ERROR",
                )
                return

            try:
                data = self.readDocument()
                logger.info(
                    f"Document loaded, extension is \"{self.documentPath.split('.')[-1]}\""
                )
            except Exception as e:
                self.output(f"Failed to open file: {e}", "ERROR")
                return

            try:
                rows, cols = self.readTable()
            except Exception as e:
                self.output(f"Failed to load table: {e}", "ERROR")
                return

            logger.info(
                f"Table loaded, found {len(rows)} {len(rows) == 1 and 'row' or 'rows'}"
            )
            logger.info(f"Table columns read: {cols}")
            logger.info(f"Table rows read: {rows}")

            if not rows or not cols:
                self.output("Given table is empty", "ERROR")
                return
            if len(cols) != 1:
                self.output(
                    "Given table must have exactly one column with the text to write on each row",
                    "ERROR",
                )
                return
            if len(rows) < 1:
                self.output(
                    "Given table must have at least another row in addition to the headers!",
                    "ERROR",
                )
                return

            total: int = 0
            successful: int = 0
            for row in rows:
                total += 1
                text = row[cols[0]].strip()

                if not text:
                    self.output(
                        f"[{total}] Text to write is empty on this row", "ERROR"
                    )
                    continue
                if len(text) > MAX_TEXT_LENGTH:
                    self.output(
                        f"[{total}] Text to write has more than {MAX_TEXT_LENGTH} characters on this row",
                        "ERROR",
                    )
                    continue

                pdf = pymupdf.open("pdf", data)

                try:
                    fontName = os.path.basename(self.fontPath)
                    page = pdf[self.pageNumber]
                    page.clean_contents()
                    page.insert_font(fontfile=self.fontPath, fontname=fontName)
                    page.insert_text(
                        pymupdf.Point(self.coordinateX, self.coordinateY),
                        text,
                        fontname=fontName,
                        fontsize=self.fontSize,
                        color=self.color,
                        rotate=self.rotation,
                    )
                except Exception as e:
                    self.output(
                        f"[{total}] Failed to write text '{text}': {e}", "ERROR"
                    )
                    continue

                try:
                    safeName: str = ""
                    for char in text:
                        if char.isalnum():
                            safeName += char
                        else:
                            safeName += "_"
                    outputFile = os.path.join(
                        self.outputPath, f"{safeName.lower()}.pdf"
                    )
                    pdf.save(outputFile)
                    successful += 1
                    self.output(f"[{total}] Wrote text '{text}' to file")
                except Exception as e:
                    self.output(
                        f"[{total}] Failed to save file for text '{text}': {e}",
                        "ERROR",
                    )
                    continue

            self.output(f"Successfully wrote {successful} out of {total} files")
