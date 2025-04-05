"""Support for valves through the SmartThings cloud API."""

from __future__ import annotations

from pysmartthings import Attribute, Capability, Category, Command, SmartThings

from homeassistant.components.valve import (
    ValveDeviceClass,
    ValveEntity,
    ValveEntityFeature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from homeassistant.components.smartthings import FullDevice, SmartThingsConfigEntry, valve
from homeassistant.components.smartthings.const import MAIN
from homeassistant.components.smartthings.entity import SmartThingsEntity

DEVICE_CLASS_MAP: dict[Category | str, ValveDeviceClass] = {
    Category.WATER_VALVE: ValveDeviceClass.WATER,
    Category.GAS_VALVE: ValveDeviceClass.GAS,
}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add valves for a config entry."""
    await valve.async_setup_entry(hass, entry, async_add_entities)
    