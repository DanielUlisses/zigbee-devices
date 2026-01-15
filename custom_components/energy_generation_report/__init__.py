"""The Energy Generation Report integration."""

from __future__ import annotations

import logging
from datetime import timedelta

import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.storage import Store
from homeassistant.helpers.typing import ConfigType
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    SERVICE_ADD_BILLING_DATA,
    SERVICE_ADD_SOLAR_DATA,
    SERVICE_ADD_SOLAR_PERIOD_DATA,
    SERVICE_DELETE_BILLING_DATA,
    SERVICE_DELETE_SOLAR_DATA,
    SERVICE_UPDATE_BILLING_DATA,
    SERVICE_UPDATE_SOLAR_DATA,
    STORAGE_KEY,
    STORAGE_KEY_SOLAR,
    STORAGE_VERSION,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

SERVICE_ADD_BILLING_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("config_entry_id"): cv.string,
        vol.Required("end_date"): cv.date,
        vol.Required("grid_consumption_reading"): vol.Coerce(float),
        vol.Required("grid_injection_reading"): vol.Coerce(float),
    }
)

SERVICE_UPDATE_BILLING_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("config_entry_id"): cv.string,
        vol.Required("end_date"): cv.date,
        vol.Required("grid_consumption_reading"): vol.Coerce(float),
        vol.Required("grid_injection_reading"): vol.Coerce(float),
    }
)

SERVICE_DELETE_BILLING_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("config_entry_id"): cv.string,
        vol.Required("end_date"): cv.date,
    }
)

SERVICE_ADD_SOLAR_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("config_entry_id"): cv.string,
        vol.Required("date"): cv.date,
        vol.Required("solar_generation_kwh"): vol.Coerce(float),
    }
)

SERVICE_UPDATE_SOLAR_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("config_entry_id"): cv.string,
        vol.Required("date"): cv.date,
        vol.Required("solar_generation_kwh"): vol.Coerce(float),
    }
)

SERVICE_DELETE_SOLAR_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("config_entry_id"): cv.string,
        vol.Required("date"): cv.date,
    }
)

SERVICE_ADD_SOLAR_PERIOD_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("config_entry_id"): cv.string,
        vol.Required("start_date"): cv.date,
        vol.Required("end_date"): cv.date,
        vol.Required("total_solar_generation_kwh"): vol.Coerce(float),
    }
)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Energy Generation Report component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Energy Generation Report from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    # Create storage for billing data
    store = Store(hass, STORAGE_VERSION, f"{STORAGE_KEY}_{entry.entry_id}")
    solar_store = Store(hass, STORAGE_VERSION, f"{STORAGE_KEY_SOLAR}_{entry.entry_id}")
    hass.data[DOMAIN][entry.entry_id] = {
        "store": store,
        "billing_data": await store.async_load() or {},
        "solar_store": solar_store,
        "manual_solar_data": await solar_store.async_load() or {},
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def add_billing_data(call: ServiceCall) -> None:
        """Add billing data for a period."""
        config_entry_id = call.data["config_entry_id"]
        end_date = call.data["end_date"].isoformat()
        grid_consumption = call.data["grid_consumption_reading"]
        grid_injection = call.data["grid_injection_reading"]

        if config_entry_id not in hass.data[DOMAIN]:
            _LOGGER.error("Config entry not found: %s", config_entry_id)
            return

        billing_data = hass.data[DOMAIN][config_entry_id]["billing_data"]
        store = hass.data[DOMAIN][config_entry_id]["store"]

        billing_data[end_date] = {
            "grid_consumption_reading": grid_consumption,
            "grid_injection_reading": grid_injection,
            "timestamp": dt_util.utcnow().isoformat(),
        }

        await store.async_save(billing_data)

        # Trigger sensor update
        hass.bus.async_fire(
            f"{DOMAIN}_data_updated", {"config_entry_id": config_entry_id}
        )

    async def update_billing_data(call: ServiceCall) -> None:
        """Update billing data for a period."""
        await add_billing_data(call)  # Same logic for now

    async def delete_billing_data(call: ServiceCall) -> None:
        """Delete billing data for a period."""
        config_entry_id = call.data["config_entry_id"]
        end_date = call.data["end_date"].isoformat()

        if config_entry_id not in hass.data[DOMAIN]:
            _LOGGER.error("Config entry not found: %s", config_entry_id)
            return

        billing_data = hass.data[DOMAIN][config_entry_id]["billing_data"]
        store = hass.data[DOMAIN][config_entry_id]["store"]

        if end_date in billing_data:
            del billing_data[end_date]
            await store.async_save(billing_data)
            hass.bus.async_fire(
                f"{DOMAIN}_data_updated", {"config_entry_id": config_entry_id}
            )

    async def add_solar_data(call: ServiceCall) -> None:
        """Add manual solar generation data for a specific date."""
        config_entry_id = call.data["config_entry_id"]
        date_str = call.data["date"].isoformat()
        solar_kwh = call.data["solar_generation_kwh"]

        if config_entry_id not in hass.data[DOMAIN]:
            _LOGGER.error("Config entry not found: %s", config_entry_id)
            return

        manual_solar_data = hass.data[DOMAIN][config_entry_id]["manual_solar_data"]
        solar_store = hass.data[DOMAIN][config_entry_id]["solar_store"]

        manual_solar_data[date_str] = {
            "solar_generation_kwh": solar_kwh,
            "timestamp": dt_util.utcnow().isoformat(),
        }

        await solar_store.async_save(manual_solar_data)
        hass.bus.async_fire(
            f"{DOMAIN}_data_updated", {"config_entry_id": config_entry_id}
        )

    async def update_solar_data(call: ServiceCall) -> None:
        """Update manual solar generation data for a specific date."""
        await add_solar_data(call)  # Same logic for now

    async def delete_solar_data(call: ServiceCall) -> None:
        """Delete manual solar generation data for a specific date."""
        config_entry_id = call.data["config_entry_id"]
        date_str = call.data["date"].isoformat()

        if config_entry_id not in hass.data[DOMAIN]:
            _LOGGER.error("Config entry not found: %s", config_entry_id)
            return

        manual_solar_data = hass.data[DOMAIN][config_entry_id]["manual_solar_data"]
        solar_store = hass.data[DOMAIN][config_entry_id]["solar_store"]

        if date_str in manual_solar_data:
            del manual_solar_data[date_str]
            await solar_store.async_save(manual_solar_data)
            hass.bus.async_fire(
                f"{DOMAIN}_data_updated", {"config_entry_id": config_entry_id}
            )

    async def add_solar_period_data(call: ServiceCall) -> None:
        """Add solar generation data for a period, distributed evenly across days."""
        config_entry_id = call.data["config_entry_id"]
        start_date = call.data["start_date"]
        end_date = call.data["end_date"]
        total_kwh = call.data["total_solar_generation_kwh"]

        if config_entry_id not in hass.data[DOMAIN]:
            _LOGGER.error("Config entry not found: %s", config_entry_id)
            return

        if start_date > end_date:
            _LOGGER.error("Start date must be before or equal to end date")
            return

        # Calculate number of days and daily average
        days_diff = (end_date - start_date).days + 1
        daily_kwh = total_kwh / days_diff

        manual_solar_data = hass.data[DOMAIN][config_entry_id]["manual_solar_data"]
        solar_store = hass.data[DOMAIN][config_entry_id]["solar_store"]

        # Add data for each day in the period
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.isoformat()
            manual_solar_data[date_str] = {
                "solar_generation_kwh": daily_kwh,
                "timestamp": dt_util.utcnow().isoformat(),
                "period_entry": True,  # Mark as period entry
                "period_total": total_kwh,
                "period_days": days_diff,
            }
            current_date += timedelta(days=1)

        await solar_store.async_save(manual_solar_data)
        hass.bus.async_fire(
            f"{DOMAIN}_data_updated", {"config_entry_id": config_entry_id}
        )

        _LOGGER.info(
            "Added solar data for period %s to %s: %.1f kWh total (%.2f kWh/day)",
            start_date,
            end_date,
            total_kwh,
            daily_kwh,
        )

    # Register services
    hass.services.async_register(
        DOMAIN,
        SERVICE_ADD_BILLING_DATA,
        add_billing_data,
        schema=SERVICE_ADD_BILLING_DATA_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_UPDATE_BILLING_DATA,
        update_billing_data,
        schema=SERVICE_UPDATE_BILLING_DATA_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_DELETE_BILLING_DATA,
        delete_billing_data,
        schema=SERVICE_DELETE_BILLING_DATA_SCHEMA,
    )

    # Register solar data services
    hass.services.async_register(
        DOMAIN,
        SERVICE_ADD_SOLAR_DATA,
        add_solar_data,
        schema=SERVICE_ADD_SOLAR_DATA_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_UPDATE_SOLAR_DATA,
        update_solar_data,
        schema=SERVICE_UPDATE_SOLAR_DATA_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_DELETE_SOLAR_DATA,
        delete_solar_data,
        schema=SERVICE_DELETE_SOLAR_DATA_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_ADD_SOLAR_PERIOD_DATA,
        add_solar_period_data,
        schema=SERVICE_ADD_SOLAR_PERIOD_DATA_SCHEMA,
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
