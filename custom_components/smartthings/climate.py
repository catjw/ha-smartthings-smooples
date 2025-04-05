"""Support for climate devices through the SmartThings cloud API."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from pysmartthings import Attribute, Capability, Command, SmartThings

from homeassistant.components.climate import (
    ATTR_HVAC_MODE,
    ATTR_TARGET_TEMP_HIGH,
    ATTR_TARGET_TEMP_LOW,
    SWING_BOTH,
    SWING_HORIZONTAL,
    SWING_OFF,
    SWING_VERTICAL,
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
)
from homeassistant.const import ATTR_TEMPERATURE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from homeassistant.components.smartthings import FullDevice, SmartThingsConfigEntry, climate
from homeassistant.components.smartthings.const import MAIN
from homeassistant.components.smartthings.entity import SmartThingsEntity

async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add climate entities for a config entry."""
    await climate.async_setup_entry(hass, entry, async_add_entities)
