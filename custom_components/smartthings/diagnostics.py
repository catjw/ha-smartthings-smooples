"""Diagnostics support for SmartThings."""

from typing import Any
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntry

from homeassistant.components.smartthings import diagnostics

from . import SmartThingsConfigEntry


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    return await diagnostics.async_get_config_entry_diagnostics(
        hass,
        entry,
    )


async def async_get_device_diagnostics(
    hass: HomeAssistant, entry: SmartThingsConfigEntry, device: DeviceEntry
) -> dict[str, Any]:
    """Return diagnostics for a device entry."""
    return await diagnostics.async_get_device_diagnostics(
        hass,
        entry,
        device,
    )
