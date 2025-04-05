
from homeassistant.core import HomeAssistant
from homeassistant.components import smartthings
from homeassistant.helpers import device_registry as dr, entity_registry as er

from pysmartthings import (
    Capability,
    ComponentStatus,
)
from homeassistant.config_entries import ConfigEntry

DOMAIN = smartthings.const.DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: smartthings.SmartThingsConfigEntry) -> bool:
    """Initialize config entry which represents an installed SmartApp."""
    # The oauth smartthings entry will have a token, older ones are version 3
    # after migration but still require reauthentication
    await smartthings.async_setup_entry(hass, entry)
    return True

async def async_unload_entry(
    hass: HomeAssistant, entry: smartthings.SmartThingsConfigEntry
) -> bool:
    """Unload a config entry."""
    return await smartthings.async_unload_entry(hass, entry)


async def async_migrate_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle config entry migration."""
    return await smartthings.async_migrate_entry(hass, entry)

def determine_machine_type(
    hass: HomeAssistant,
    entry_id: str,
    device_id: str,
) -> Capability | None:
    """Determine the machine type for a device."""
    return smartthings.determine_machine_type(
        hass,
        entry_id,
        device_id,
    )

def create_devices(
    device_registry: dr.DeviceRegistry,
    devices: dict[str, smartthings.FullDevice],
    entry: smartthings.SmartThingsConfigEntry,
    rooms: dict[str, str],
) -> None:
    """Create devices in the device registry."""
    smartthings.create_devices(
        device_registry,
        devices,
        entry,
        rooms,
    )

# KEEP_CAPABILITY_QUIRK: dict[
#     Capability | str, Callable[[dict[Attribute | str, Status]], bool]
# ] = {
#     Capability.DRYER_OPERATING_STATE: (
#         lambda status: status[Attribute.SUPPORTED_MACHINE_STATES].value is not None
#     ),
#     Capability.WASHER_OPERATING_STATE: (
#         lambda status: status[Attribute.SUPPORTED_MACHINE_STATES].value is not None
#     ),
#     Capability.DEMAND_RESPONSE_LOAD_CONTROL: lambda _: True,
# }


def process_status(status: dict[str, ComponentStatus]) -> dict[str, ComponentStatus]:
    """Remove disabled capabilities from status."""
    return smartthings.process_status(status)


def process_component_status(status: ComponentStatus) -> None:
    """Remove disabled capabilities from component status."""
    smartthings.process_component_status(ComponentStatus)