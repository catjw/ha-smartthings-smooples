"""Support for scenes through the SmartThings cloud API."""

from homeassistant.components.smartthings import scene


class SmartThingsScene(scene.SmartThingsScene):
    """Representation of a SmartThings scene."""

# for i in scene.__all__:
#     setattr(SmartThingsScene, i, getattr(scene, i))