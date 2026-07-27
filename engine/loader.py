from pathlib import Path
import os

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QComboBox,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QHBoxLayout,
)

from PySide6.QtCore import Qt

from engine.mission import Mission
from engine.console import Console
from engine.settings_window import SettingsWindow

class Loader(QWidget):

    def __init__(self, project_root):
        super().__init__()

        self.project_root = Path(project_root)

        self.missions_path = (
            self.project_root
            / "data"
            / "missions"
        )

        self.configuration = None

        self.setup_ui()
        self.scan_missions()

    def open_settings(self):
        dialog = SettingsWindow(self)
        dialog.exec()
    def setup_ui(self):

        self.setWindowTitle(
            "MOCR Simulator - Mission Initialization"
        )

        self.resize(
            600,
            600
        )


        layout = QVBoxLayout()


        title = QLabel(
            "MISSION OPERATIONS CONTROL ROOM"
        )

        title.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            title
        )


        subtitle = QLabel(
            "Operator Initialization"
        )

        subtitle.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            subtitle
        )



        self.operator_name = QLineEdit()

        self.operator_name.setPlaceholderText(
            "Operator name"
        )

        layout.addWidget(
            self.operator_name
        )



        self.operator_id = QLineEdit()

        self.operator_id.setPlaceholderText(
            "Operator ID"
        )

        layout.addWidget(
            self.operator_id
        )



        layout.addWidget(
            QLabel("Mission Package")
        )


        self.mission_list = QComboBox()

        layout.addWidget(
            self.mission_list
        )



        layout.addWidget(
            QLabel("Assigned Stations")
        )


        self.console_list = QListWidget()


        for code, name in Console.get_all().items():

            item = QListWidgetItem(
                f"{code} - {name}"
            )

            item.setData(
                Qt.UserRole,
                code
            )


            item.setFlags(
                item.flags()
                |
                Qt.ItemIsUserCheckable
            )

            item.setCheckState(
                Qt.Unchecked
            )


            self.console_list.addItem(
                item
            )


        layout.addWidget(
            self.console_list
        )



        self.initialize_button = QPushButton(
            "INITIALIZE SIMULATION"
        )


        self.initialize_button.clicked.connect(
            self.initialize
        )


        layout.addWidget(
            self.initialize_button
        )

        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings)

        buttons = QHBoxLayout()
        buttons.addWidget(self.settings_button)
        buttons.addWidget(self.initialize_button)

        layout.addLayout(buttons)

        self.setLayout(
            layout
        )



    def scan_missions(self):

        self.mission_list.clear()

        if not self.missions_path.exists():

            QMessageBox.critical(
                self,
                "Mission Folder Missing",
                f"Could not find:\n{self.missions_path}"
            )

            return

        missions = sorted(self.missions_path.glob("*.mission"))

        for mission in missions:
            self.mission_list.addItem(mission.name)

        if self.mission_list.count() == 0:

            QMessageBox.warning(
                self,
                "No Missions",
                "No .mission files were found."
            )



    def initialize(self):

        name = self.operator_name.text()

        operator_id = self.operator_id.text()


        if not name:

            QMessageBox.warning(
                self,
                "Error",
                "Operator name required"
            )

            return


        if not operator_id.isdigit():

            QMessageBox.warning(
                self,
                "Error",
                "Operator ID must be numeric"
            )

            return



        stations = []


        for i in range(
            self.console_list.count()
        ):

            item = self.console_list.item(i)


            if item.checkState() == Qt.Checked:

                stations.append(
                    item.data(
                        Qt.UserRole
                    )
                )


        if not stations:

            QMessageBox.warning(
                self,
                "Error",
                "Assign at least one station"
            )

            return



        mission_file = self.mission_list.currentText()

        mission_path = self.missions_path / mission_file

        mission = Mission(mission_path)


        self.configuration = {


            "operator": {

                "name": name,

                "id": int(operator_id)

            },


            "mission": mission.data,


            "stations": stations

        }



        self.close()



    def get_configuration(self):

        return self.configuration