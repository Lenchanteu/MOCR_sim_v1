import json
from pathlib import Path


class Mission:

    def __init__(self, filepath):
        self.filepath = Path(filepath)
        self.data = {}

        self.load()

    def load(self):

        with self.filepath.open(
            "r",
            encoding="utf-8"
        ) as file:

            self.data = json.load(file)

    @property
    def name(self):
        return self.data.get(
            "mission_name",
            self.filepath.stem
        )

    @property
    def consoles(self):
        return self.data.get(
            "available_consoles",
            []
        )