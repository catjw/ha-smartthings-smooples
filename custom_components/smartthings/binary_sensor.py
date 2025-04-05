"""Support for binary sensors through the SmartThings cloud API."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from pysmartthings import Attribute, Capability, Category, SmartThings, Status

from homeassistant.components.binary_sensor import (
    DOMAIN as BINARY_SENSOR_DOMAIN,
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from homeassistant.components.smartthings import FullDevice, SmartThingsConfigEntry
from homeassistant.components.smartthings.const import INVALID_SWITCH_CATEGORIES, MAIN
from homeassistant.components.smartthings.entity import SmartThingsEntity
from homeassistant.components.smartthings.util import deprecate_entity

from homeassistant.components.smartthings import binary_sensor


def get_main_component_category(
    device: FullDevice,
) -> Category | str:
    """Get the main component of a device."""
    return binary_sensor.get_main_component_category(device)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add binary sensors for a config entry."""
    await binary_sensor.async_setup_entry(hass, entry, async_add_entities)
