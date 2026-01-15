"""Constants for the Energy Generation Report integration."""

DOMAIN = "energy_generation_report"

# Storage
STORAGE_KEY = "energy_generation_report_billing_data"
STORAGE_KEY_SOLAR = "energy_generation_report_solar_data"
STORAGE_VERSION = 1

# Services
SERVICE_ADD_BILLING_DATA = "add_billing_data"
SERVICE_UPDATE_BILLING_DATA = "update_billing_data"
SERVICE_DELETE_BILLING_DATA = "delete_billing_data"
SERVICE_ADD_SOLAR_DATA = "add_solar_data"
SERVICE_UPDATE_SOLAR_DATA = "update_solar_data"
SERVICE_DELETE_SOLAR_DATA = "delete_solar_data"
SERVICE_ADD_SOLAR_PERIOD_DATA = "add_solar_period_data"

# Configuration keys
CONF_SOLAR_SENSOR = "solar_sensor"
CONF_INITIAL_GRID_CONSUMPTION = "initial_grid_consumption"
CONF_INITIAL_GRID_INJECTION = "initial_grid_injection"
CONF_MINIMUM_BILLING_KWH = "minimum_billing_kwh"
CONF_INITIAL_BALANCE = "initial_balance"
CONF_BILLING_PERIOD_DAYS = "billing_period_days"

# Defaults
DEFAULT_MINIMUM_BILLING_KWH = 100.0
DEFAULT_INITIAL_BALANCE = 0.0
DEFAULT_BILLING_PERIOD_DAYS = 30

# Sensor types
SENSOR_TYPES = {
    "monthly_solar_generation": {
        "name": "Monthly Solar Generation",
        "unit": "kWh",
        "icon": "mdi:solar-power",
    },
    "monthly_grid_consumption": {
        "name": "Monthly Grid Consumption",
        "unit": "kWh", 
        "icon": "mdi:transmission-tower",
    },
    "monthly_grid_injection": {
        "name": "Monthly Grid Injection",
        "unit": "kWh",
        "icon": "mdi:transmission-tower-export", 
    },
    "monthly_total_consumption": {
        "name": "Monthly Total Consumption",
        "unit": "kWh",
        "icon": "mdi:flash",
    },
    "monthly_solar_consumption": {
        "name": "Monthly Solar Consumption",
        "unit": "kWh",
        "icon": "mdi:home-lightning-bolt",
    },
    "cumulative_balance": {
        "name": "Cumulative Energy Balance",
        "unit": "kWh",
        "icon": "mdi:scale-balance",
    },
}