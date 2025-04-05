"""Support for sensors through the SmartThings cloud API."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any, cast

from pysmartthings import Attribute, Capability, ComponentStatus, SmartThings, Status

from homeassistant.components.sensor import (
    DOMAIN as SENSOR_DOMAIN,
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
    CONCENTRATION_PARTS_PER_MILLION,
    LIGHT_LUX,
    PERCENTAGE,
    EntityCategory,
    UnitOfArea,
    UnitOfEnergy,
    UnitOfMass,
    UnitOfPower,
    UnitOfTemperature,
    UnitOfVolume,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.util import dt as dt_util

from homeassistant.components.smartthings import FullDevice, SmartThingsConfigEntry, sensor
from homeassistant.components.smartthings.const import MAIN
from homeassistant.components.smartthings.entity import SmartThingsEntity
from homeassistant.components.smartthings.util import deprecate_entity

THERMOSTAT_CAPABILITIES = {
    Capability.TEMPERATURE_MEASUREMENT,
    Capability.THERMOSTAT_HEATING_SETPOINT,
    Capability.THERMOSTAT_MODE,
}

JOB_STATE_MAP = {
    "airWash": "air_wash",
    "airwash": "air_wash",
    "aIRinse": "ai_rinse",
    "aISpin": "ai_spin",
    "aIWash": "ai_wash",
    "aIDrying": "ai_drying",
    "internalCare": "internal_care",
    "continuousDehumidifying": "continuous_dehumidifying",
    "thawingFrozenInside": "thawing_frozen_inside",
    "delayWash": "delay_wash",
    "weightSensing": "weight_sensing",
    "freezeProtection": "freeze_protection",
    "preDrain": "pre_drain",
    "preWash": "pre_wash",
    "prewash": "pre_wash",
    "wrinklePrevent": "wrinkle_prevent",
    "unknown": None,
}

OVEN_JOB_STATE_MAP = {
    "scheduledStart": "scheduled_start",
    "fastPreheat": "fast_preheat",
    "scheduledEnd": "scheduled_end",
    "stone_heating": "stone_heating",
    "timeHoldPreheat": "time_hold_preheat",
}

MEDIA_PLAYBACK_STATE_MAP = {
    "fast forwarding": "fast_forwarding",
}

ROBOT_CLEANER_TURBO_MODE_STATE_MAP = {
    "extraSilence": "extra_silence",
}

ROBOT_CLEANER_MOVEMENT_MAP = {
    "powerOff": "off",
}

OVEN_MODE = {
    "Conventional": "conventional",
    "Bake": "bake",
    "BottomHeat": "bottom_heat",
    "ConvectionBake": "convection_bake",
    "ConvectionRoast": "convection_roast",
    "Broil": "broil",
    "ConvectionBroil": "convection_broil",
    "SteamCook": "steam_cook",
    "SteamBake": "steam_bake",
    "SteamRoast": "steam_roast",
    "SteamBottomHeatplusConvection": "steam_bottom_heat_plus_convection",
    "Microwave": "microwave",
    "MWplusGrill": "microwave_plus_grill",
    "MWplusConvection": "microwave_plus_convection",
    "MWplusHotBlast": "microwave_plus_hot_blast",
    "MWplusHotBlast2": "microwave_plus_hot_blast_2",
    "SlimMiddle": "slim_middle",
    "SlimStrong": "slim_strong",
    "SlowCook": "slow_cook",
    "Proof": "proof",
    "Dehydrate": "dehydrate",
    "Others": "others",
    "StrongSteam": "strong_steam",
    "Descale": "descale",
    "Rinse": "rinse",
}

WASHER_OPTIONS = ["pause", "run", "stop"]

async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add sensors for a config entry."""
    await sensor.async_setup_entry(hass, entry, async_add_entities)
