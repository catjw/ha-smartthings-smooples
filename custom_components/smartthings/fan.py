"""Support for fans through the SmartThings cloud API."""

from __future__ import annotations

import math
from typing import Any

from pysmartthings import Attribute, Capability, Command, SmartThings

from homeassistant.components.fan import FanEntity, FanEntityFeature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util.percentage import (
    percentage_to_ranged_value,
    ranged_value_to_percentage,
)
from homeassistant.util.scaling import int_states_in_range

from homeassistant.components.smartthings import FullDevice, SmartThingsConfigEntry, fan
from homeassistant.components.smartthings.const import MAIN
from homeassistant.components.smartthings.entity import SmartThingsEntity

SPEED_RANGE = (1, 3)  # off is not included


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add fans for a config entry."""
    await fan.async_setup_entry(hass, entry, async_add_entities)
