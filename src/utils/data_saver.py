import os

import qfluentwidgets
from qfluentwidgets import (
    qconfig,
    QConfig,
    EnumSerializer,
    OptionsConfigItem,
    OptionsValidator,
    BoolValidator,
    ColorSerializer,
    ColorValidator,
    RangeValidator,
)

from config.metadata import DATA_PATH

CONFIG_PATH = os.path.join(DATA_PATH, "config.json")


class ConfigItem(OptionsConfigItem):
    def set(self, value, save=False):
        self.value = value
        if save:
            self.parent.save()  # type: ignore

    def get(self):
        return self.value


class Config(QConfig):
    """Global object for app data."""

    maximized = ConfigItem("Window", "Maximized", False, BoolValidator())
    width = ConfigItem("Window", "Width", 500)
    height = ConfigItem("Window", "Height", 500)
    x = ConfigItem("Window", "X", 0)
    y = ConfigItem("Window", "Y", 0)
    style = ConfigItem(
        "Window",
        "Style",
        qfluentwidgets.Theme.DARK,
        OptionsValidator(qfluentwidgets.Theme),
        EnumSerializer(qfluentwidgets.Theme),
    )
    color = ConfigItem(
        "Window",
        "Color",
        qfluentwidgets.QColor("#FA8E8F"),
        ColorValidator(qfluentwidgets.QColor()),
        ColorSerializer(),
    )

    textSize = ConfigItem("Write", "TextSize", 16, RangeValidator(1, 9999))
    textColor = ConfigItem(
        "Write",
        "TextColor",
        qfluentwidgets.QColor("#AAD58F"),
        ColorValidator(qfluentwidgets.QColor()),
        ColorSerializer(),
    )

    def reset(self):
        for _, attr in self.__class__.__dict__.items():
            if isinstance(attr, ConfigItem):
                attr.set(attr.defaultValue)


config = Config()

qconfig.load(CONFIG_PATH, config)
