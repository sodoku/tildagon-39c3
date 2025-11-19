import app
import os
import sys

from machine import I2C

from app_components import clear_background
from events.input import Buttons, BUTTON_TYPES
from system.eventbus import eventbus
from system.patterndisplay.events import PatternDisable, PatternEnable
from tildagonos import tildagonos

if sys.implementation.name == "micropython":
    apps = os.listdir("/apps")
    path = ""
    for a in apps:
        if a == "sodoku_tildagon_39c3":
            path = "/apps/" + a
    ASSET_PATH = path + "/assets/"
else:
    ASSET_PATH = "apps/tildagon-39c3/assets/"


class App39c3(app.App):
    def __init__(self):
        self.button_states = Buttons(self)
        self.turn_off()

    def update(self, delta):
        if self.button_states.get(BUTTON_TYPES["CANCEL"]):
            self.button_states.clear()
            self.minimise()
        elif self.button_states.get(BUTTON_TYPES["DOWN"]):
            self.turn_on()
        elif self.button_states.get(BUTTON_TYPES["UP"]):
            self.turn_off()

    def draw(self, ctx):
        clear_background(ctx)
        if self.on:
            ctx.save()
            ctx.rgb(0, 255, 0).rectangle(-120, -120, 240, 240).fill()
            ctx.image(ASSET_PATH + "logo_black.png", -110, -26, 220, 52)
            ctx.restore()
        else:
            ctx.save()
            ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()
            ctx.image(ASSET_PATH + "logo_green.png", -110, -26, 220, 52)
            ctx.restore()

    def turn_on(self):
        eventbus.emit(PatternEnable())
        self.on = True

    def turn_off(self):
        eventbus.emit(PatternDisable())
        for i in range(0, 12):
            tildagonos.leds[i + 1] = (0, 0, 0)
        tildagonos.leds.write()
        self.on = False


__app_export__ = App39c3
