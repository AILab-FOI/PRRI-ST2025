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

        self.done_counter = 0
        # game objects

        self.player = None
        self.cache = None
        self.scene = LoadingScene( self )
        self.message = Message( self )

        self.show_popup = False
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
        
        if self.show_popup:
            self.draw_popup()
        pg.display.flip()

    def draw_popup(self):
        screen_width, screen_height = self.screen.get_size()
        popup_width, popup_height = int(screen_width * 0.6), int(screen_height * 0.6)
        popup_x, popup_y = (screen_width - popup_width) // 2, (screen_height - popup_height) // 2
        popup_rect = pg.Rect(popup_x, popup_y, popup_width, popup_height)
        
        pg.draw.rect(self.screen, (50, 50, 50), popup_rect)
        pg.draw.rect(self.screen, (200, 200, 200), popup_rect, 3)
        font = pg.font.Font(None, 48)
        text = font.render("Inventory", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, popup_y + 50))
        self.screen.blit(text, text_rect)

    def check_events(self):
        self.anim_trigger = False
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif e.type == self.anim_event:
                self.anim_trigger = True
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_TAB:
                    self.show_popup = not self.show_popup
                self.player.single_fire(event=e)

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
