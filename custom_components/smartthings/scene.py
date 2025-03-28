"""Support for scenes through the SmartThings cloud API."""

from homeassistant.components.smartthings import scene


class SmartThingsScene(scene.SmartThingsScene):
    pass

for i in scene.__all__:
    setattr(SmartThingsScene, i, getattr(scene, i))