import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from engine.loader import Loader


def main():
    app = QApplication(sys.argv)

    # Project root (folder containing main.py)
    project_root = Path(__file__).resolve().parent

    loader = Loader(project_root)
    loader.show()

    app.exec()

    config = loader.get_configuration()

    if config:
        print(config)


if __name__ == "__main__":
    main()