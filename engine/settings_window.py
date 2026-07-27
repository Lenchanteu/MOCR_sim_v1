from PySide6.QtCore import Qt, QSettings
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QFileDialog
)


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = QSettings("MOCR", "Simulator")

        self.setWindowTitle("Settings")
        self.setMinimumSize(600, 500)

        self.build_ui()
        self.load_settings()

    def build_ui(self):

        main_layout = QVBoxLayout(self)

        #
        # Appearance
        #
        appearance_group = QGroupBox("Appearance")
        appearance_layout = QFormLayout()

        self.theme = QComboBox()
        self.theme.addItems([
            "Dark",
            "Light",
            "System"
        ])

        appearance_layout.addRow("Theme", self.theme)
        appearance_group.setLayout(appearance_layout)

        #
        # Startup
        #
        startup_group = QGroupBox("Startup")
        startup_layout = QVBoxLayout()

        self.remember_name = QCheckBox("Remember operator name")
        self.remember_id = QCheckBox("Remember operator ID")
        self.remember_stations = QCheckBox("Remember selected stations")
        self.remember_mission = QCheckBox("Remember last mission")

        startup_layout.addWidget(self.remember_name)
        startup_layout.addWidget(self.remember_id)
        startup_layout.addWidget(self.remember_stations)
        startup_layout.addWidget(self.remember_mission)

        startup_group.setLayout(startup_layout)

        #
        # Simulation
        #
        simulation_group = QGroupBox("Simulation")
        simulation_layout = QFormLayout()

        self.time_scale = QComboBox()
        self.time_scale.addItems([
            "0.25x",
            "0.5x",
            "1x",
            "2x",
            "5x",
            "10x"
        ])

        self.refresh_rate = QSpinBox()
        self.refresh_rate.setRange(1, 240)
        self.refresh_rate.setSuffix(" FPS")

        self.failure_system = QCheckBox("Enable failures")

        simulation_layout.addRow("Default time scale", self.time_scale)
        simulation_layout.addRow("Refresh rate", self.refresh_rate)
        simulation_layout.addRow("", self.failure_system)

        simulation_group.setLayout(simulation_layout)

        #
        # Network
        #
        network_group = QGroupBox("Network")
        network_layout = QFormLayout()

        self.enable_network = QCheckBox("Enable multiplayer")

        self.hostname = QLineEdit()

        self.port = QSpinBox()
        self.port.setRange(1, 65535)

        network_layout.addRow("", self.enable_network)
        network_layout.addRow("Host", self.hostname)
        network_layout.addRow("Port", self.port)

        network_group.setLayout(network_layout)

        #
        # Mission Folder
        #
        folder_group = QGroupBox("Mission Folder")
        folder_layout = QHBoxLayout()

        self.mission_folder = QLineEdit()

        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self.select_folder)

        folder_layout.addWidget(self.mission_folder)
        folder_layout.addWidget(browse_button)

        folder_group.setLayout(folder_layout)

        #
        # Buttons
        #
        button_layout = QHBoxLayout()

        button_layout.addStretch()

        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")

        save_button.clicked.connect(self.save_settings)
        cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(cancel_button)
        button_layout.addWidget(save_button)

        #
        # Assemble
        #
        main_layout.addWidget(appearance_group)
        main_layout.addWidget(startup_group)
        main_layout.addWidget(simulation_group)
        main_layout.addWidget(network_group)
        main_layout.addWidget(folder_group)
        main_layout.addStretch()
        main_layout.addLayout(button_layout)

    def select_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Mission Folder",
            self.mission_folder.text()
        )

        if folder:
            self.mission_folder.setText(folder)

    def load_settings(self):

        self.theme.setCurrentText(
            self.settings.value("theme", "Dark")
        )

        self.remember_name.setChecked(
            self.settings.value("remember_name", True, bool)
        )

        self.remember_id.setChecked(
            self.settings.value("remember_id", True, bool)
        )

        self.remember_stations.setChecked(
            self.settings.value("remember_stations", True, bool)
        )

        self.remember_mission.setChecked(
            self.settings.value("remember_mission", True, bool)
        )

        self.time_scale.setCurrentText(
            self.settings.value("time_scale", "1x")
        )

        self.refresh_rate.setValue(
            self.settings.value("refresh_rate", 30, int)
        )

        self.failure_system.setChecked(
            self.settings.value("failure_system", True, bool)
        )

        self.enable_network.setChecked(
            self.settings.value("network_enabled", False, bool)
        )

        self.hostname.setText(
            self.settings.value("hostname", "localhost")
        )

        self.port.setValue(
            self.settings.value("port", 5500, int)
        )

        self.mission_folder.setText(
            self.settings.value("mission_folder", "data/missions")
        )

    def save_settings(self):

        self.settings.setValue("theme", self.theme.currentText())

        self.settings.setValue(
            "remember_name",
            self.remember_name.isChecked()
        )

        self.settings.setValue(
            "remember_id",
            self.remember_id.isChecked()
        )

        self.settings.setValue(
            "remember_stations",
            self.remember_stations.isChecked()
        )

        self.settings.setValue(
            "remember_mission",
            self.remember_mission.isChecked()
        )

        self.settings.setValue(
            "time_scale",
            self.time_scale.currentText()
        )

        self.settings.setValue(
            "refresh_rate",
            self.refresh_rate.value()
        )

        self.settings.setValue(
            "failure_system",
            self.failure_system.isChecked()
        )

        self.settings.setValue(
            "network_enabled",
            self.enable_network.isChecked()
        )

        self.settings.setValue(
            "hostname",
            self.hostname.text()
        )

        self.settings.setValue(
            "port",
            self.port.value()
        )

        self.settings.setValue(
            "mission_folder",
            self.mission_folder.text()
        )

        self.accept()