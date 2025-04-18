"""Test configuration and mocks for the SmartThings component."""

from collections.abc import Generator
import time
from unittest.mock import AsyncMock, patch

from pysmartthings import (
    DeviceResponse,
    DeviceStatus,
    LocationResponse,
    RoomResponse,
    SceneResponse,
    Subscription,
)
import pytest

from homeassistant.components.application_credentials import (
    ClientCredential,
    async_import_client_credential,
)

from homeassistant.const import CONF_ACCESS_TOKEN, CONF_CLIENT_ID, CONF_CLIENT_SECRET
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component

from pytest_homeassistant_custom_component.common import MockConfigEntry, load_fixture
from pytest_homeassistant_custom_component.syrupy import HomeAssistantSnapshotExtension
from syrupy.assertion import SnapshotAssertion

from custom_components.smartthings import smartthings


pytest_plugins = ["pytest_homeassistant_custom_component"]

@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):

    """Enable custom integrations defined in the test dir."""
    yield


@pytest.fixture
def snapshot(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Return snapshot assertion fixture with the Home Assistant extension."""
    return snapshot.use_extension(HomeAssistantSnapshotExtension)


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Override async_setup_entry."""
    with patch(
        "custom_components.smartthings.smartthings.async_setup_entry",
        return_value=True,
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture(name="expires_at")
def mock_expires_at() -> int:
    """Fixture to set the oauth token expiration time."""
    return time.time() + 3600


@pytest.fixture(autouse=True)
async def setup_credentials(hass: HomeAssistant) -> None:
    """Fixture to setup credentials."""
    assert await async_setup_component(hass, "application_credentials", {})
    await async_import_client_credential(
        hass,
        smartthings.const.DOMAIN,
        ClientCredential("CLIENT_ID", "CLIENT_SECRET"),
        smartthings.const.DOMAIN,
    )


@pytest.fixture
def mock_smartthings() -> Generator[AsyncMock]:
    """Mock a SmartThings client."""
    with (
        patch(
            "custom_components.smartthings.smartthings.SmartThings",
            autospec=True,
        ) as mock_client,
        patch(
            "homeassistant.components.smartthings.config_flow.SmartThings",
            # "custom_components.smartthings.config_flow.SmartThings",
            new=mock_client,
        ),
    ):
        client = mock_client.return_value
        client.get_scenes.return_value = SceneResponse.from_json(
            load_fixture("scenes.json", smartthings.const.DOMAIN)
        ).items
        client.get_locations.return_value = LocationResponse.from_json(
            load_fixture("locations.json", smartthings.const.DOMAIN)
        ).items
        client.get_rooms.return_value = RoomResponse.from_json(
            load_fixture("rooms.json", smartthings.const.DOMAIN)
        ).items
        client.create_subscription.return_value = Subscription.from_json(
            load_fixture("subscription.json", smartthings.const.DOMAIN)
        )
        yield client


@pytest.fixture(
    params=[
        "da_ac_airsensor_01001",
        "da_ac_rac_000001",
        "da_ac_rac_000003",
        "da_ac_rac_100001",
        "da_ac_rac_01001",
        "multipurpose_sensor",
        "contact_sensor",
        "base_electric_meter",
        "smart_plug",
        "vd_stv_2017_k",
        "c2c_arlo_pro_3_switch",
        "yale_push_button_deadbolt_lock",
        "ge_in_wall_smart_dimmer",
        "centralite",
        "da_ref_normal_000001",
        "da_ref_normal_01011",
        "vd_network_audio_002s",
        "vd_sensor_light_2023",
        "iphone",
        "da_sac_ehs_000001_sub",
        "da_wm_dw_000001",
        "da_wm_wd_000001",
        "da_wm_wd_000001_1",
        "da_wm_wm_000001",
        "da_wm_wm_000001_1",
        "da_wm_sc_000001",
        "da_rvc_normal_000001",
        "da_ks_microwave_0101x",
        "da_ks_cooktop_31001",
        "da_ks_range_0101x",
        "da_ks_oven_01061",
        "hue_color_temperature_bulb",
        "hue_rgbw_color_bulb",
        "c2c_shade",
        "sonos_player",
        "aeotec_home_energy_meter_gen5",
        "virtual_water_sensor",
        "virtual_thermostat",
        "virtual_valve",
        "sensibo_airconditioner_1",
        "ecobee_sensor",
        "ecobee_thermostat",
        "ecobee_thermostat_offline",
        "fake_fan",
        "generic_fan_3_speed",
        "heatit_ztrm3_thermostat",
        "heatit_zpushwall",
        "generic_ef00_v1",
        "bosch_radiator_thermostat_ii",
        "im_speaker_ai_0001",
        "abl_light_b_001",
        "tplink_p110",
        "ikea_kadrilj",
        "aux_ac",
        "hw_q80r_soundbar",
        "gas_meter",
    ]
)
def device_fixture(
    mock_smartthings: AsyncMock, request: pytest.FixtureRequest
) -> Generator[str]:
    """Return every device."""
    return request.param


@pytest.fixture
def devices(mock_smartthings: AsyncMock, device_fixture: str) -> Generator[AsyncMock]:
    """Return a specific device."""
    mock_smartthings.get_devices.return_value = DeviceResponse.from_json(
        load_fixture(f"devices/{device_fixture}.json", smartthings.const.DOMAIN)
    ).items
    mock_smartthings.get_device_status.return_value = DeviceStatus.from_json(
        load_fixture(f"device_status/{device_fixture}.json", smartthings.const.DOMAIN)
    ).components
    return mock_smartthings


@pytest.fixture
def mock_config_entry(expires_at: int) -> MockConfigEntry:
    """Mock a config entry."""
    return MockConfigEntry(
        domain=smartthings.const.DOMAIN,
        title="My home",
        unique_id="397678e5-9995-4a39-9d9f-ae6ba310236c",
        data={
            "auth_implementation": smartthings.const.DOMAIN,
            "token": {
                "access_token": "mock-access-token",
                "refresh_token": "mock-refresh-token",
                "expires_at": expires_at,
                "scope": " ".join(smartthings.const.SCOPES),
                "access_tier": 0,
                "installed_app_id": "5aaaa925-2be1-4e40-b257-e4ef59083324",
            },
            smartthings.const.CONF_LOCATION_ID: "397678e5-9995-4a39-9d9f-ae6ba310236c",
            smartthings.const.CONF_INSTALLED_APP_ID: "123",
        },
        version=3,
        minor_version=2,
    )


@pytest.fixture
def mock_old_config_entry() -> MockConfigEntry:
    """Mock the old config entry."""
    return MockConfigEntry(
        domain=smartthings.const.DOMAIN,
        title="My home",
        unique_id="appid123-2be1-4e40-b257-e4ef59083324_397678e5-9995-4a39-9d9f-ae6ba310236c",
        data={
            CONF_ACCESS_TOKEN: "mock-access-token",
            smartthings.const.CONF_REFRESH_TOKEN: "mock-refresh-token",
            CONF_CLIENT_ID: "CLIENT_ID",
            CONF_CLIENT_SECRET: "CLIENT_SECRET",
            smartthings.const.CONF_LOCATION_ID: "397678e5-9995-4a39-9d9f-ae6ba310236c",
            smartthings.const.CONF_INSTALLED_APP_ID: "123aa123-2be1-4e40-b257-e4ef59083324",
        },
        version=2,
    )