"""Sensor platform for Energy Generation Report."""

from __future__ import annotations

import logging
from datetime import date, datetime, timedelta
from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    CONF_BILLING_PERIOD_DAYS,
    CONF_INITIAL_BALANCE,
    CONF_INITIAL_GRID_CONSUMPTION,
    CONF_INITIAL_GRID_INJECTION,
    CONF_MINIMUM_BILLING_KWH,
    CONF_SOLAR_SENSOR,
    DEFAULT_BILLING_PERIOD_DAYS,
    DEFAULT_INITIAL_BALANCE,
    DEFAULT_MINIMUM_BILLING_KWH,
    DOMAIN,
    SENSOR_TYPES,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = EnergyReportCoordinator(hass, config_entry)

    sensors = []
    for sensor_type in SENSOR_TYPES:
        sensors.append(EnergyReportSensor(coordinator, sensor_type))

    async_add_entities(sensors)


class EnergyReportCoordinator:
    """Coordinator to manage energy report calculations."""

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize the coordinator."""
        self.hass = hass
        self.config_entry = config_entry
        self._listeners: list[callback] = []
        self._solar_data: dict[str, float] = {}  # date -> daily kwh
        self._periods: dict[str, dict] = {}  # end_date -> period_data

        # Listen for data updates
        self.hass.bus.async_listen(f"{DOMAIN}_data_updated", self._handle_data_update)

    @callback
    def async_add_listener(self, update_callback: callback) -> None:
        """Add a listener for updates."""
        self._listeners.append(update_callback)

    @callback
    def async_remove_listener(self, update_callback: callback) -> None:
        """Remove a listener."""
        if update_callback in self._listeners:
            self._listeners.remove(update_callback)

    @callback
    def _async_notify_listeners(self) -> None:
        """Notify all listeners of updates."""
        for listener in self._listeners:
            listener()

    async def _handle_data_update(self, event) -> None:
        """Handle billing data updates."""
        if event.data.get("config_entry_id") == self.config_entry.entry_id:
            await self._calculate_periods()
            self._async_notify_listeners()

    async def async_initialize(self) -> None:
        """Initialize the coordinator."""
        await self._load_solar_data()
        await self._calculate_periods()

    async def _load_solar_data(self) -> None:
        """Load and aggregate solar sensor data."""
        solar_sensor = self.config_entry.data[CONF_SOLAR_SENSOR]

        # Get all billing periods to determine date range needed
        billing_data = self.hass.data[DOMAIN][self.config_entry.entry_id][
            "billing_data"
        ]

        if not billing_data:
            return

        # Find earliest and latest dates
        dates = [
            datetime.fromisoformat(date_str).date() for date_str in billing_data.keys()
        ]
        if not dates:
            return

        start_date = min(dates) - timedelta(
            days=self.config_entry.data.get(
                CONF_BILLING_PERIOD_DAYS, DEFAULT_BILLING_PERIOD_DAYS
            )
        )
        end_date = max(dates)

        # Query solar data from recorder
        from homeassistant.components.recorder import get_instance
        from homeassistant.components.recorder.models import States
        from homeassistant.components.recorder.util import session_scope

        instance = get_instance(self.hass)
        if not instance:
            _LOGGER.warning("Recorder not available")
            return

        with session_scope(hass=self.hass) as session:
            # Get daily solar data
            query = (
                session.query(States)
                .filter(
                    States.entity_id == solar_sensor,
                    States.last_updated >= start_date,
                    States.last_updated <= end_date + timedelta(days=1),
                )
                .order_by(States.last_updated)
            )

            daily_totals = {}
            previous_value = None
            current_date = None

            for state in query:
                if state.state in ("unknown", "unavailable", None):
                    continue

                try:
                    value = float(state.state)
                except (ValueError, TypeError):
                    continue

                state_date = state.last_updated.date()

                # Handle daily reset sensors
                if current_date != state_date:
                    if current_date and previous_value is not None:
                        daily_totals[current_date.isoformat()] = previous_value
                    current_date = state_date
                    previous_value = value
                else:
                    previous_value = max(previous_value or 0, value)

            # Don't forget the last day
            if current_date and previous_value is not None:
                daily_totals[current_date.isoformat()] = previous_value

        self._solar_data = daily_totals

    async def _calculate_periods(self) -> None:
        """Calculate energy data for all billing periods."""
        billing_data = self.hass.data[DOMAIN][self.config_entry.entry_id][
            "billing_data"
        ]

        if not billing_data:
            self._periods = {}
            return

        # Sort periods by end date
        sorted_periods = sorted(billing_data.items(), key=lambda x: x[0])

        periods = {}
        cumulative_balance = self.config_entry.data.get(
            CONF_INITIAL_BALANCE, DEFAULT_INITIAL_BALANCE
        )

        prev_grid_consumption = self.config_entry.data.get(
            CONF_INITIAL_GRID_CONSUMPTION, 0.0
        )
        prev_grid_injection = self.config_entry.data.get(
            CONF_INITIAL_GRID_INJECTION, 0.0
        )
        prev_end_date = None

        for end_date_str, data in sorted_periods:
            end_date = datetime.fromisoformat(end_date_str).date()

            # Calculate start date
            if prev_end_date:
                start_date = prev_end_date + timedelta(days=1)
            else:
                billing_period_days = self.config_entry.data.get(
                    CONF_BILLING_PERIOD_DAYS, DEFAULT_BILLING_PERIOD_DAYS
                )
                start_date = end_date - timedelta(days=billing_period_days - 1)

            # Calculate grid consumption and injection for this period
            grid_consumption_period = (
                data["grid_consumption_reading"] - prev_grid_consumption
            )
            grid_injection_period = data["grid_injection_reading"] - prev_grid_injection

            # Calculate solar generation for this period
            solar_generation_period = self._calculate_solar_for_period(
                start_date, end_date
            )

            # Calculate derived metrics
            total_consumption = grid_consumption_period + (
                solar_generation_period - grid_injection_period
            )
            solar_consumption = solar_generation_period - grid_injection_period

            # Calculate balance change (injection - consumption,
            # but respect minimum billing)
            minimum_kwh = self.config_entry.data.get(
                CONF_MINIMUM_BILLING_KWH, DEFAULT_MINIMUM_BILLING_KWH
            )
            billing_consumption = max(grid_consumption_period - minimum_kwh, 0)
            balance_change = grid_injection_period - billing_consumption
            cumulative_balance += balance_change

            periods[end_date_str] = {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "solar_generation": solar_generation_period,
                "grid_consumption": grid_consumption_period,
                "grid_injection": grid_injection_period,
                "total_consumption": total_consumption,
                "solar_consumption": solar_consumption,
                "balance_change": balance_change,
                "cumulative_balance": cumulative_balance,
            }

            prev_grid_consumption = data["grid_consumption_reading"]
            prev_grid_injection = data["grid_injection_reading"]
            prev_end_date = end_date

        self._periods = periods

    def _calculate_solar_for_period(self, start_date: date, end_date: date) -> float:
        """Calculate total solar generation for a period."""
        total = 0.0
        current_date = start_date
        manual_solar_data = self.hass.data[DOMAIN][self.config_entry.entry_id][
            "manual_solar_data"
        ]

        while current_date <= end_date:
            date_str = current_date.isoformat()

            # Check if there's manual data for this date first
            if date_str in manual_solar_data:
                total += manual_solar_data[date_str]["solar_generation_kwh"]
            # Otherwise use sensor data
            elif date_str in self._solar_data:
                total += self._solar_data[date_str]

            current_date += timedelta(days=1)

        return total

    def get_current_period_value(self, sensor_type: str) -> float | None:
        """Get the current period value for a sensor type."""
        if not self._periods:
            return None

        # Get the latest period
        latest_period = max(self._periods.values(), key=lambda x: x["end_date"])

        if sensor_type == "monthly_solar_generation":
            return latest_period["solar_generation"]
        elif sensor_type == "monthly_grid_consumption":
            return latest_period["grid_consumption"]
        elif sensor_type == "monthly_grid_injection":
            return latest_period["grid_injection"]
        elif sensor_type == "monthly_total_consumption":
            return latest_period["total_consumption"]
        elif sensor_type == "monthly_solar_consumption":
            return latest_period["solar_consumption"]
        elif sensor_type == "cumulative_balance":
            return latest_period["cumulative_balance"]

        return None

    def get_all_periods_data(self) -> dict:
        """Get all periods data for charts."""
        return self._periods


class EnergyReportSensor(SensorEntity, RestoreEntity):
    """Representation of an Energy Report sensor."""

    def __init__(
        self,
        coordinator: EnergyReportCoordinator,
        sensor_type: str,
    ) -> None:
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._sensor_type = sensor_type
        # Format the sensor name
        name_prefix = coordinator.config_entry.data[CONF_NAME]
        sensor_name = SENSOR_TYPES[sensor_type]["name"]
        self._attr_name = f"{name_prefix} {sensor_name}"
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{sensor_type}"
        self._attr_native_unit_of_measurement = SENSOR_TYPES[sensor_type]["unit"]
        self._attr_icon = SENSOR_TYPES[sensor_type]["icon"]
        self._attr_state_class = SensorStateClass.TOTAL
        self._attr_native_value = None

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()

        # Restore previous state
        if (restored := await self.async_get_last_state()) is not None:
            if restored.state not in ("unknown", "unavailable"):
                try:
                    self._attr_native_value = float(restored.state)
                except (ValueError, TypeError):
                    pass

        # Initialize coordinator and add listener
        await self._coordinator.async_initialize()
        self._coordinator.async_add_listener(self._handle_coordinator_update)

        # Initial update
        self._handle_coordinator_update()

    async def async_will_remove_from_hass(self) -> None:
        """When entity is removed."""
        self._coordinator.async_remove_listener(self._handle_coordinator_update)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self._coordinator.get_current_period_value(
            self._sensor_type
        )
        self.async_write_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        attributes = {
            "periods_data": self._coordinator.get_all_periods_data(),
            "sensor_type": self._sensor_type,
            "config_entry_id": self._coordinator.config_entry.entry_id,
        }
        return attributes
