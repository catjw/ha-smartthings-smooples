"""Support for climate devices through the SmartThings cloud API."""

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from homeassistant.components.smartthings import climate
from pysmartthings import Attribute, Capability

from . import SmartThingsConfigEntry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: SmartThingsConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Add climate entities for a config entry."""
    entry_data = entry.runtime_data
    entities: list[climate.ClimateEntity] = [
        SmartThingsRoomAirConditioner(entry_data.client, device)
        for device in entry_data.devices.values()
        if all(capability in device.status[climate.MAIN] for capability in climate.AC_CAPABILITIES)
    ]
    entities.extend(
        climate.SmartThingsThermostat(entry_data.client, device)
        for device in entry_data.devices.values()
        if all(
            capability in device.status[climate.MAIN] for capability in climate.THERMOSTAT_CAPABILITIES
        )
    )
    async_add_entities(entities)


class SmartThingsRoomAirConditioner(climate.SmartThingsAirConditioner):
    def _determine_preset_modes(self) -> list[str] | None:
        """Return a list of available preset modes."""
        if self.supports_capability(Capability.CUSTOM_AIR_CONDITIONER_OPTIONAL_MODE):
            supported_modes = self.get_attribute_value(
                Capability.CUSTOM_AIR_CONDITIONER_OPTIONAL_MODE,
                Attribute.SUPPORTED_AC_OPTIONAL_MODE,
            )
            if supported_modes :
                return supported_modes
        return None