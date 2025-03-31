#!/usr/bin/env python3


import sys
import platform
from settings import *
from cache import Cache
from player import Player
from scene import Scene, LoadingScene
import asyncio
from itertools import cycle
from message import Message
from popup import InventoryPopup, SettingsPopup

class App:
    def __init__(self):
        self.screen = pg.display.set_mode(RES, pg.FULLSCREEN) #
        pg.font.init()
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0.01
        self.anim_trigger = False
        self.anim_event = pg.USEREVENT + 0
        pg.time.set_timer(self.anim_event, 100)
        # groups
        self.main_group = pg.sprite.LayeredUpdates()
        self.entity_group = pg.sprite.LayeredUpdates()
        self.collision_group = pg.sprite.Group()
        self.transparent_objects = []

        # game objects
        self.player = None
        self.cache = None
        self.scene = LoadingScene( self )
        self.message = Message( self )

        self.inventory_popup = InventoryPopup(self.screen)
        self.settings_popup = SettingsPopup(self.screen)
        self.show_settings = False

    def update(self):
        self.scene.update()
        self.entity_group.update()
        self.main_group.update()
        pg.display.set_caption(f'{self.clock.get_fps(): .1f}')
        self.delta_time = self.clock.tick()

    def draw(self):
        try:
            self.scene.draw()
        except:
            self.screen.fill(BG_COLOR)
            self.entity_group.draw(self.screen)
            self.main_group.draw(self.screen)
            self.message.draw()
        
        if self.inventory_popup.visible:
            self.inventory_popup.draw()
        if self.settings_popup.visible:
            self.settings_popup.draw()

        pg.display.flip()

    def check_events(self):
        self.anim_trigger = False
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif e.type == self.anim_event:
                self.anim_trigger = True
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_TAB:
                    self.inventory_popup.toggle()
                elif e.key == pg.K_ESCAPE:
                    self.settings_popup.toggle()
                if not (self.settings_popup.visible or self.inventory_popup.visible) and self.player is not None:
                    self.player.single_fire(event=e)
            elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                if self.settings_popup.visible:
                    action = self.settings_popup.handle_mouse_click()
                    if action == "Quit Game":
                        pg.quit()
                        sys.exit()
                    elif action == "Continue":
                        self.settings_popup.toggle()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

async def run( app ):
    while True:
        if app.player:
            app.check_events()
        app.get_time()
        app.update()
        app.draw()
        await asyncio.sleep( 0 )


if __name__ == '__main__':
    if __import__("sys").platform == "emscripten":
        from time import sleep
        try:
            platform.document.body.style.background = '#000000'
        except:
            pass
        #asyncio.run( flash_bcg() )

    app = App()
    asyncio.run( run( app ) )
