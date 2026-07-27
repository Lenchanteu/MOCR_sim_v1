from datetime import datetime, timezone, timedelta
from enum import Enum


# ==========================================================
# Enums
# ==========================================================

class AlertSeverity(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class AlertSystem(Enum):
    POWER = "POWER"
    COMMUNICATION = "COMMUNICATION"
    THERMAL = "THERMAL"
    COMPUTER = "COMPUTER"
    PROPULSION = "PROPULSION"


# ==========================================================
# Data Classes
# ==========================================================

class Mission:
    def __init__(self):
        self.phase = "PRE-LAUNCH"
        self.met = 0                     # seconds
        self.utc_time = datetime.now(timezone.utc)
        self.last_communication = None

    def tick(self, dt):
        self.met += dt
        self.utc_time += timedelta(seconds=dt)


class Navigation:
    def __init__(self):
        self.position = (0.0, 0.0, 0.0)  # x,y,z km
        self.orbit_number = 0
        self.altitude = 0.0              # km
        self.velocity = (0.0, 0.0, 0.0)              # x,y,z km/s
        self.attitude_mode = "SAFE"
        self.has_target = False
        self.distance_from_target = (0.0, 0.0, 0.0)

    def tick(self, dt):
        self.position = tuple(
            p + v * dt
            for p, v in zip(self.position, self.velocity)
        )
        if self.has_target:
            self.distance_from_target = tuple(
                p - v * dt
                for p, v in zip(self.distance_from_target, self.velocity)
            )
        self.altitude += self.velocity[1] * dt

class Communication:
    def __init__(self):
        self.state = "OFFLINE"
        self.current_ground_station = None
        self.signal_strength = 0.0       # %
        self.data_rate = 0.0             # kbps
        self.last_contact = None
        self.link_quality = "NONE"


class Power:
    def __init__(self):
        self.battery_percentage = 100.0
        self.battery_capacity = 5000.0
        self.battery_voltage = 28.0
        self.battery_energy = self.battery_capacity
        self.solar_array_status = "DEPLOYED"
        self.power_generation = 0.0      # W
        self.power_consumption = 0.0     # W
        self.power_mode = "NORMAL"

    def tick(self, dt):
        self.update_battery(dt)
    def update_battery(self, dt):

        # Net electrical power (W)
        net_power = (
            self.power_generation -
            self.power_consumption
        )

        # Update stored energy (Wh)
        self.battery_energy += (
            net_power * dt / 3600
        )

        # Clamp
        self.battery_energy = max(
            0,
            min(
                self.battery_capacity,
                self.battery_energy
            )
        )

        # Percentage
        self.battery_percentage = (
            self.battery_energy /
            self.battery_capacity
        ) * 100

        # Voltage
        self.battery_voltage = (
            24.0 +
            5.4 *
            (self.battery_percentage / 100) ** 0.35
        )


class Thermal:
    def __init__(self):
        self.main_bus_temperature = 20.0
        self.component_temperatures = {}
        self.thermal_state = "NOMINAL"

    def tick(self, dt, power):
        heat = power.power_consumption * 0.002

        self.main_bus_temperature += heat * dt

        if self.main_bus_temperature > 35:
            self.main_bus_temperature -= 0.05 * dt

class Propulsion:
    def __init__(self):
        self.available = True
        self.fuel_percentage = 100.0
        self.thruster_status = "READY"
        self.last_maneuver = None

    def tick(self, dt):
        if self.thruster_status == "FIRING":
            self.fuel_percentage -= 0.005 * dt

        self.fuel_percentage = max(0, self.fuel_percentage)


class Computer:
    def __init__(self):
        self.health = "GOOD"
        self.active_computer = "PRIMARY"
        self.software_version = "1.0.0"
        self.fault_status = None
        self.reset_count = 0


class Payload:
    def __init__(self):
        self.status = "OFF"
        self.instrument_mode = "IDLE"
        self.data_collection = False
        self.storage_used = 0.0          # %

    def tick(self, dt):
        if self.data_collection:
            self.storage_used += 0.001 * dt
            self.storage_used = min(100, self.storage_used)
        


# ==========================================================
# Alert
# ==========================================================

class Alert:
    def __init__(self, severity, system, message):
        self.severity = severity
        self.system = system
        self.message = message
        self.timestamp = datetime.now(timezone.utc)

    def __str__(self):
        return f"[{self.timestamp}] {self.severity.value} {self.system.value}: {self.message}"


class Alerts:
    def __init__(self):
        self.alerts = []
    def check(self):
        pass

# ==========================================================
# Spacecraft
# ==========================================================

class Spacecraft:

    def __init__(self):
        self.name = ""
        self.id = ""
        self.type = ""

        self.mission = Mission()
        self.navigation = Navigation()
        self.communication = Communication()
        self.power = Power()
        self.thermal = Thermal()
        self.propulsion = Propulsion()
        self.computer = Computer()
        self.payload = Payload()

        self.alert = Alerts()
        self.alerts = self.alert.alerts

    def initialization(self, spacecraft_type, name, mission_id):

        if spacecraft_type not in ("sat", "crew", "probe"):
            raise ValueError(
                f"Spacecraft type '{spacecraft_type}' is not implemented."
            )

        self.type = spacecraft_type
        self.name = name
        self.id = mission_id

        # Type-specific defaults
        if spacecraft_type == "crew":
            self.communication.data_rate = 5000
            self.power.battery_capacity = 5000.0

        elif spacecraft_type == "probe":
            self.communication.data_rate = 256
            self.power.battery_capacity = 5000.0

        elif spacecraft_type == "sat":
            self.communication.data_rate = 1024
            self.power.battery_capacity = 5000.0

    def add_alert(self, severity, system, message):
        self.alerts.append(Alert(severity, system, message))


    def tick(self, dt):
        """
        Advance the simulation by dt seconds.
        """
        self.mission.tick(dt)
        self.power.tick(dt)
        self.navigation.tick(dt)
        self.thermal.tick(dt, self.power)
        self.propulsion.tick(dt)
        self.payload.tick(dt)
        self.alert.check()


# ==========================================================
# Simulator
# ==========================================================

class Simulator:

    def __init__(self):
        self.spacecraft = Spacecraft()

    def step(self, dt=1):
        self.spacecraft.tick(dt)