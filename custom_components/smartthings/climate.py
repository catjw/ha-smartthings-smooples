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
    
    @property
    def preset_mode(self) -> str | None:
        """Return the preset mode."""
        if self.supports_capability(Capability.CUSTOM_AIR_CONDITIONER_OPTIONAL_MODE):
            mode = self.get_attribute_value(
                Capability.CUSTOM_AIR_CONDITIONER_OPTIONAL_MODE,
                Attribute.AC_OPTIONAL_MODE,
            )
            return mode
        return None
    
    def _determine_preset_modes(self) -> list[str] | None:
        """Return a list of available preset modes."""
        
        """Return the list of available ac optional modes, in samsung case check that windfree cannot be selected when in heating."""
        restricted_values = ["windFree"]
        model = self.device.status[climate.MAIN][Capability.OCF][Attribute.MODEL_NUMBER].value.split("|")[0]

        supported_ac_optional_modes = [
            str(x)
            for x in self.device.status[climate.MAIN][Capability.CUSTOM_AIR_CONDITIONER_OPTIONAL_MODE]["supportedAcOptionalMode"].value
        ]
        if "quiet" not in supported_ac_optional_modes and model == "ARTIK051_PRAC_20K":
            supported_ac_optional_modes.append("quiet")
            self.is_faulty_quiet = True

        if self.device.status[climate.MAIN][Capability.AIR_CONDITIONER_MODE][Attribute.AIR_CONDITIONER_MODE] in ("auto", "heat"):
            if any(
                restrictedvalue in supported_ac_optional_modes
                for restrictedvalue in restricted_values
            ):
                reduced_supported_optional_modes = supported_ac_optional_modes
                reduced_supported_optional_modes.remove("windFree")
                return reduced_supported_optional_modes
        else:
            return supported_ac_optional_modes
        
        
        # if self.supports_capability(Capability.CUSTOM_AIR_CONDITIONER_OPTIONAL_MODE):
        #     supported_modes = self.get_attribute_value(
        #         Capability.CUSTOM_AIR_CONDITIONER_OPTIONAL_MODE,
        #         Attribute.SUPPORTED_AC_OPTIONAL_MODE,
        #     )
        #     if supported_modes :
        #         return supported_modes
        # return None