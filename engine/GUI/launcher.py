"""
MOCR Simulator Launcher

MIT License

Copyright (c) 2026 Lenchanteu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software.
"""


import sys
import subprocess
from pathlib import Path

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QMessageBox,
)

from PySide6.QtCore import Qt


# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parents[2]

MISSION_DIR = ROOT_DIR / "data" / "missions"

SIMULATOR_PATH = ROOT_DIR / "engine" / "simulator.py"


# ------------------------------------------------------------
# Console configuration
# ------------------------------------------------------------

# Later this can be loaded from a JSON configuration file.
AVAILABLE_CONSOLES = {
    "Flight Director Console": "FD",
    "Flight Dynamics Console": "FDYN",
    "Telemetry Console": "TM",
    "Power Systems Console": "EPS",
    "Communication Console": "COMM",
    "Payload Console": "PAYLOAD",
}


# ------------------------------------------------------------
# Main Launcher
# ------------------------------------------------------------

class MOCRLauncher(QWidget):

    def __init__(self):
        super().__init__()

        self.selected_mission = None

        self.setWindowTitle(
            "MOCR Simulator Launcher"
        )

        self.resize(
            900,
            600
        )

        self.setup_ui()
        self.load_missions()

    # --------------------------------------------------------

    def setup_ui(self):

        layout = QVBoxLayout()


        title = QLabel(
            "Mission Operation Control Room Simulator"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setStyleSheet(
            """
            font-size: 26px;
            font-weight: bold;
            margin: 15px;
            """
        )

        layout.addWidget(title)



        # ----------------------------
        # Console selection
        # ----------------------------

        console_box = QGroupBox(
            "Available Consoles"
        )

        console_layout = QVBoxLayout()


        self.console_list = QListWidget()

        self.console_list.setSelectionMode(
            QListWidget.SelectionMode.MultiSelection
        )


        for console in AVAILABLE_CONSOLES:
            item = QListWidgetItem(console)
            self.console_list.addItem(item)


        console_layout.addWidget(
            self.console_list
        )

        console_box.setLayout(
            console_layout
        )

        layout.addWidget(
            console_box
        )


        # ----------------------------
        # Mission selection
        # ----------------------------

        mission_box = QGroupBox(
            "Mission File"
        )

        mission_layout = QHBoxLayout()


        self.mission_label = QLabel(
            "No mission selected"
        )

        self.mission_button = QPushButton(
            "Choose Mission"
        )

        self.mission_button.clicked.connect(
            self.choose_mission
        )


        mission_layout.addWidget(
            self.mission_label
        )

        mission_layout.addWidget(
            self.mission_button
        )


        mission_box.setLayout(
            mission_layout
        )


        layout.addWidget(
            mission_box
        )



        # ----------------------------
        # Start button
        # ----------------------------

        self.start_button = QPushButton(
            "START SIMULATION"
        )

        self.start_button.setMinimumHeight(
            60
        )

        self.start_button.setStyleSheet(
            """
            QPushButton {
                background-color: #1565c0;
                color: white;
                font-size: 18px;
                font-weight: bold;
                border-radius: 8px;
            }

            QPushButton:hover {
                background-color: #1976d2;
            }
            """
        )


        self.start_button.clicked.connect(
            self.start_simulator
        )


        layout.addWidget(
            self.start_button
        )


        # ----------------------------
        # Copyright
        # ----------------------------

        copyright_label = QLabel(
            "MOCR Simulator © 2026 Lenchanteu\n"
            "Released under the MIT License"
        )


        copyright_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )


        copyright_label.setStyleSheet(
            """
            color: grey;
            font-size: 11px;
            margin-top: 15px;
            """
        )


        layout.addWidget(
            copyright_label
        )


        self.setLayout(
            layout
        )


        self.apply_theme()


    # --------------------------------------------------------

    def apply_theme(self):

        self.setStyleSheet(
            """

            QWidget {
                background-color: #121212;
                color: #eeeeee;
                font-size: 14px;
            }


            QListWidget {
                background-color: #1e1e1e;
                border: 1px solid #333;
                border-radius: 5px;
            }


            QGroupBox {
                border: 1px solid #444;
                border-radius: 8px;
                margin-top: 10px;
                padding: 10px;
            }


            QPushButton {
                padding: 8px;
            }

            """
        )


    # --------------------------------------------------------

    def load_missions(self):

        if not MISSION_DIR.exists():
            MISSION_DIR.mkdir(
                parents=True
            )


    # --------------------------------------------------------

    def choose_mission(self):

        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Mission File",
            str(MISSION_DIR),
            "MOCR Mission Files (*.mission)"
        )


        if file:

            self.selected_mission = Path(file)

            self.mission_label.setText(
                self.selected_mission.name
            )


    # --------------------------------------------------------

    def start_simulator(self):

        if not self.selected_mission:

            QMessageBox.warning(
                self,
                "Missing Mission",
                "Please select a mission file."
            )

            return


        consoles = [
            AVAILABLE_CONSOLES[item.text()]
            for item in self.console_list.selectedItems()
        ]


        if not consoles:

            QMessageBox.warning(
                self,
                "No Consoles",
                "Select at least one console."
            )

            return



        command = [
            sys.executable,
            str(SIMULATOR_PATH),

            "--mission",
            str(self.selected_mission),

            "--consoles",
            ",".join(consoles),
        ]


        try:

            subprocess.Popen(
                command,
                cwd=ROOT_DIR
            )


            self.close()


        except Exception as error:

            QMessageBox.critical(
                self,
                "Launch Error",
                str(error)
            )



# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------

if __name__ == "__main__":

    app = QApplication(
        sys.argv
    )


    window = MOCRLauncher()

    window.show()


    sys.exit(
        app.exec()
    )