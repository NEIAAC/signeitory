import os
import pandas as pd
import pymupdf
from math import isnan
from PySide6.QtCore import QThread, Signal
from typing import Tuple

from utils.logger import logger


class WriterThread(QThread):
    outputSignal = Signal(str, str)

    def __init__(
        self,
        filePath: str,
        tablePath: str,
        outputPath: str,
        fontFilePath: str,
        coordinateX: float = 200.0,
        coordinateY: float = 50.0,
        fontSize: float = 24.0,
        color: Tuple[float, float, float] = (0.2, 0.5, 0.7),
        rotation: float = 0.0,
        pageNumber: int = 0,
    ):
        super().__init__()
        self.filePath = filePath
        self.tablePath = tablePath
        self.outputPath = outputPath
        self.fontFilePath = fontFilePath
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
            table = pd.read_csv(self.tablePath, index_col=False)
        elif self.tablePath.endswith(".xlsx"):
            table = pd.read_excel(self.tablePath, index_col=False)
        else:
            raise ValueError("Unsupported file extension")

        records = table.values.tolist()

        # Convert NaN to empty string to match EmailerThread behavior
        for i, record in enumerate(records):
            if isinstance(record[0], float) and isnan(record[0]):
                records[i][0] = ""

        return records

    def readFile(self) -> bytes:
        try:
            file = pymupdf.open(self.filePath)
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
            try:
                data = self.readFile()
                self.output("Writeable file loaded")
            except Exception as e:
                self.output(f"Failed to open file: {e}", "ERROR")
                return

            try:
                table = self.readTable()
                self.output(
                    f"Table loaded, found {len(table)} {len(table) == 1 and 'row' or 'rows'}"
                )
            except Exception as e:
                self.output(f"Failed to load table: {e}", "ERROR")
                return

            if not table:
                self.output("Given table is empty", "ERROR")
                return

            total: int = 0
            successful: int = 0

            for row in table:
                total += 1
                text = row[0]

                if not text:
                    self.output(f"[{total}] Text is empty on this row", "ERROR")
                    continue

                pdf: pymupdf.Document = pymupdf.open(data, filetype="pdf")

                try:
                    fontName = os.path.basename(self.fontFilePath)
                    page: pymupdf.Page = pdf[self.pageNumber]
                    page.insert_font(
                        fontfile=self.fontFilePath, fontname=fontName
                    )
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
                    outputFile = os.path.join(self.outputPath, f"{text}.pdf")
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
