"""Config flow for Energy Generation Report integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers import selector
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry

from .const import (
    DOMAIN,
    CONF_SOLAR_SENSOR,
    CONF_INITIAL_GRID_CONSUMPTION,
    CONF_INITIAL_GRID_INJECTION,
    CONF_MINIMUM_BILLING_KWH,
    CONF_INITIAL_BALANCE,
    CONF_BILLING_PERIOD_DAYS,
    DEFAULT_MINIMUM_BILLING_KWH,
    DEFAULT_INITIAL_BALANCE,
    DEFAULT_BILLING_PERIOD_DAYS,
)

_LOGGER = logging.getLogger(__name__)


async def get_energy_sensors(hass: HomeAssistant) -> list[str]:
    """Get list of energy sensors."""
    entity_registry = async_get_entity_registry(hass)
    sensors = []

    for entity_id, entry in entity_registry.entities.items():
        if (
            entry.domain == "sensor"
            and entry.device_class == "energy"
            and "solar" in entity_id.lower()
        ):
            sensors.append(entity_id)

    # If no solar sensors found, get all energy sensors
    if not sensors:
        for entity_id, entry in entity_registry.entities.items():
            if entry.domain == "sensor" and entry.device_class == "energy":
                sensors.append(entity_id)

    return sorted(sensors)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Energy Generation Report."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validate solar sensor exists
            if user_input[CONF_SOLAR_SENSOR] not in await get_energy_sensors(self.hass):
                errors[CONF_SOLAR_SENSOR] = "invalid_sensor"
            else:
                await self.async_set_unique_id(user_input[CONF_SOLAR_SENSOR])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=user_input[CONF_NAME],
                    data=user_input,
                )

        energy_sensors = await get_energy_sensors(self.hass)

        if not energy_sensors:
            return self.async_abort(reason="no_energy_sensors")

        data_schema = vol.Schema(
            {
                vol.Required(CONF_NAME, default="Energy Generation Report"): str,
                vol.Required(CONF_SOLAR_SENSOR): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                        device_class="energy",
                    )
                ),
                vol.Required(CONF_INITIAL_GRID_CONSUMPTION, default=0.0): vol.Coerce(
                    float
                ),
                vol.Required(CONF_INITIAL_GRID_INJECTION, default=0.0): vol.Coerce(
                    float
                ),
                vol.Optional(
                    CONF_MINIMUM_BILLING_KWH, default=DEFAULT_MINIMUM_BILLING_KWH
                ): vol.Coerce(float),
                vol.Optional(
                    CONF_INITIAL_BALANCE, default=DEFAULT_INITIAL_BALANCE
                ): vol.Coerce(float),
                vol.Optional(
                    CONF_BILLING_PERIOD_DAYS, default=DEFAULT_BILLING_PERIOD_DAYS
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=365)),
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle reconfiguration of the integration."""
        config_entry = self.hass.config_entries.async_get_entry(
            self.context["entry_id"]
        )

        if user_input is not None:
            return self.async_update_reload_and_abort(
                config_entry,
                data={**config_entry.data, **user_input},
            )

        data_schema = vol.Schema(
            {
                vol.Required(
                    CONF_NAME,
                    default=config_entry.data.get(
                        CONF_NAME, "Energy Generation Report"
                    ),
                ): str,
                vol.Required(
                    CONF_SOLAR_SENSOR, default=config_entry.data.get(CONF_SOLAR_SENSOR)
                ): selector.EntitySelector(
                    selector.EntitySelectorConfig(
                        domain="sensor",
                        device_class="energy",
                    )
                ),
                vol.Required(
                    CONF_INITIAL_GRID_CONSUMPTION,
                    default=config_entry.data.get(CONF_INITIAL_GRID_CONSUMPTION, 0.0),
                ): vol.Coerce(float),
                vol.Required(
                    CONF_INITIAL_GRID_INJECTION,
                    default=config_entry.data.get(CONF_INITIAL_GRID_INJECTION, 0.0),
                ): vol.Coerce(float),
                vol.Optional(
                    CONF_MINIMUM_BILLING_KWH,
                    default=config_entry.data.get(
                        CONF_MINIMUM_BILLING_KWH, DEFAULT_MINIMUM_BILLING_KWH
                    ),
                ): vol.Coerce(float),
                vol.Optional(
                    CONF_INITIAL_BALANCE,
                    default=config_entry.data.get(
                        CONF_INITIAL_BALANCE, DEFAULT_INITIAL_BALANCE
                    ),
                ): vol.Coerce(float),
                vol.Optional(
                    CONF_BILLING_PERIOD_DAYS,
                    default=config_entry.data.get(
                        CONF_BILLING_PERIOD_DAYS, DEFAULT_BILLING_PERIOD_DAYS
                    ),
                ): vol.All(vol.Coerce(int), vol.Range(min=1, max=365)),
            }
        )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=data_schema,
        )
