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
        self.show_settings = False
        self.settings_options = ["Continue", "Help", "Save Game", "Load Game", "Quit Game"]
        self.hovered_option = None  
        self.option_rects = []

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
        if self.show_settings:
            self.draw_settings()
        pg.display.flip()

    def draw_popup(self):
        screen_width, screen_height = self.screen.get_size()
        popup_width, popup_height = int(screen_width * 0.6), int(screen_height * 0.6)
        popup_x, popup_y = (screen_width - popup_width) // 2, (screen_height - popup_height) // 2
        popup_rect = pg.Rect(popup_x, popup_y, popup_width, popup_height)
        
        pg.draw.rect(self.screen, (139, 69, 19), popup_rect)
        pg.draw.rect(self.screen, (100, 50, 10), popup_rect, 3)
        font = pg.font.Font(None, 48)
        rivet_radius = 6
        rivet_color = (160, 140, 100)
        for x in [popup_x + 10, popup_x + popup_width - 10]:
            for y in [popup_y + 10, popup_y + popup_height - 10]:
                pg.draw.circle(self.screen, rivet_color, (x, y), rivet_radius)
        self.font = pg.font.Font("assets/PressStart2P-Regular.ttf", 16)
        text = font.render("Inventory", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, popup_y + 50))
        self.screen.blit(text, text_rect)

    def draw_settings(self):
        screen_width, screen_height = self.screen.get_size()
        popup_width, popup_height = int(screen_width * 0.6), int(screen_height * 0.6)
        popup_x, popup_y = (screen_width - popup_width) // 2, (screen_height - popup_height) // 2
        popup_rect = pg.Rect(popup_x, popup_y, popup_width, popup_height)
        
        pg.draw.rect(self.screen, (139, 69, 19), popup_rect)
        pg.draw.rect(self.screen, (100, 50, 10), popup_rect, 3)
        font = pg.font.Font(None, 48)
        rivet_radius = 6
        rivet_color = (160, 140, 100)
        for x in [popup_x + 10, popup_x + popup_width - 10]:
            for y in [popup_y + 10, popup_y + popup_height - 10]:
                pg.draw.circle(self.screen, rivet_color, (x, y), rivet_radius)
        self.font = pg.font.Font("assets/PressStart2P-Regular.ttf", 16)
        text = font.render("Settings", True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_width // 2, popup_y + 50))
        self.screen.blit(text, text_rect)
        
        self.option_rects = []
        for i, option in enumerate(self.settings_options):
            mouse_pos = pg.mouse.get_pos()
            option_rect = pg.Rect(0, 0, popup_width * 0.8, 40)
            option_rect.center = (screen_width // 2, popup_y + 120 + i * 50)
            self.option_rects.append(option_rect)
            
            is_hovered = option_rect.collidepoint(mouse_pos)
            if is_hovered:
                self.hovered_option = i
            
            color = (255, 255, 0) if is_hovered else (255, 255, 255)
            
            option_text = font.render(option, True, color)
            option_rect = option_text.get_rect(center=(screen_width // 2, popup_y + 120 + i * 50))
            self.screen.blit(option_text, option_rect)


    def check_events(self):
        self.anim_trigger = False
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif e.type == self.anim_event:
                self.anim_trigger = True
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_TAB and not self.show_settings:
                    self.show_popup = not self.show_popup
                elif e.key == pg.K_ESCAPE:
                    if self.show_settings:
                        self.show_settings = False
                    elif not self.show_popup:
                        self.show_settings = True
                
                if not (self.show_settings or self.show_popup) and self.player:
                    self.player.single_fire(event=e)
            elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1: 
                if self.show_settings and self.hovered_option is not None:
                    self.handle_settings_selection(self.hovered_option)

    def handle_settings_selection(self, option_index):
        if self.settings_options[option_index] == "Quit Game":
            pg.quit()
            sys.exit()
        elif self.settings_options[option_index] == "Continue":
            self.show_settings = False
        elif self.settings_options[option_index] == "Help":
            pass  # kasnije dodati - kontrole...
        elif self.settings_options[option_index] == "Load Game":
            pass  # kasnije dodati
        elif self.settings_options[option_index] == "Save Game":
            pass  # kasnije dodati

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
