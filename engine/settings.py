from PySide6.QtCore import QSettings


class Settings:

    def __init__(self):
        self.settings = QSettings(
            "MOCR",
            "Simulator"
        )

    def get(self, key, default=None):
        return self.settings.value(key, default)

    def set(self, key, value):
        self.settings.setValue(key, value)