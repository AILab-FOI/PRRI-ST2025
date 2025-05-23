#!/usr/bin/env python3

import sys
import platform
import inventoryRepository
from settings import *
from cache import Cache
from player import Player
from scene import Scene, LoadingScene
import asyncio
from itertools import cycle
from message import Message
from popup import InventoryPopup, SettingsPopup, QuestPopup, MainMenu, HintPopup, HelpPopup, MessagePopup, ShoePickupPopUp, DeliveryNPCPopUp, BerryMiniGame
import questRepository 
from shoeDeliverySystem import ShoeDelivery
from popup import HedgehogMiniGame

class App:
    def __init__(self):
        self.screen = pg.display.set_mode(RES, pg.FULLSCREEN) #
        pg.font.init()
        pg.mixer.init()
        pg.mixer.music.load("assets/bgm/bgm.ogg")
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(-1)
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
        self.scene = None    #LoadingScene( self )
        self.popup = MessagePopup(self)
        self.menu = MainMenu(self)
        self.cozy_mechanic_begin = False
        self.show_chest_hint = True

        self.shoe_pickup = ShoePickupPopUp(self.screen, "assets/entities/bullet/cipele2.png")
        self.shoe_delivery = ShoeDelivery(self)
        self.hint_popup = HintPopup(self.screen) 
        self.hint_popup.visible = False
        self.inventory_popup = InventoryPopup(self.screen, 'player')
        self.chest_popup = InventoryPopup(self.screen, 'chest')
        self.help_popup = HelpPopup(self.screen) 
        self.settings_popup = SettingsPopup(self.screen, self.help_popup)  # Proslijedimo help popup
        self.quest_popup = QuestPopup(self.screen)
        self.npc_path = "assets/entities/npcs/npc1.png"
        self.delivery_popup = DeliveryNPCPopUp(self.screen, self.npc_path)
        self.show_settings = False
        self.hedgehog_minigame = HedgehogMiniGame(self)
        self.berry_minigame = BerryMiniGame(self)
        questRepository.load_quests_from_json()

    def update(self):
        self.hedgehog_minigame.update()
        self.shoe_delivery.update()
        self.scene.update()
        self.entity_group.update()
        self.main_group.update()
        pg.display.set_caption(f'{self.clock.get_fps(): .1f}')
        self.delta_time = self.clock.tick()
        self.berry_minigame.update()

    def draw(self):
        try:
            self.scene.draw()
        except:
            self.screen.fill(BG_COLOR)
            self.entity_group.draw(self.screen)
            self.main_group.draw(self.screen)
        
        if self.hint_popup.visible:
            self.hint_popup.draw()
        if self.settings_popup.visible:
            self.settings_popup.draw()
        if self.inventory_popup.visible:
            self.inventory_popup.draw()
        if self.chest_popup.visible:
            self.chest_popup.draw()
        if self.quest_popup.visible:
            self.quest_popup.draw()
        if self.help_popup.visible:
            self.help_popup.draw()  
        if self.popup.visible:
            self.popup.draw()
        if self.shoe_pickup.visible:
            self.shoe_pickup.draw()
        if self.delivery_popup.visible:
            self.delivery_popup.draw()
        if self.shoe_delivery.minigame and self.shoe_delivery.minigame.is_active():
            self.shoe_delivery.minigame.draw()
        if self.hedgehog_minigame.is_active():
            self.hedgehog_minigame.draw()
        if self.berry_minigame.active and self.berry_minigame.visible:
            self.berry_minigame.draw()
       
        pg.display.flip()

    def start_game(self):
        self.menu = None
        self.scene = LoadingScene(self)
        pg.time.set_timer(pg.USEREVENT + 1, 3000, loops=1)


    def check_events(self):
        self.anim_trigger = False
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif e.type == self.anim_event:
                self.anim_trigger = True
            elif e.type == pg.USEREVENT + 1:  
                self.hint_popup.visible = True
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_TAB:
                    self.inventory_popup.toggle()
                if e.key == pg.K_t:
                    self.quest_popup.toggle()
                if e.key == pg.K_e:
                    if self.scene and self.scene.questHandler.is_player_near_chest():
                        self.chest_popup.visible = True
                        self.show_chest_hint = False
                elif e.key == pg.K_ESCAPE:
                    if self.chest_popup.visible:
                        self.chest_popup.visible = False
                        return
                    if self.shoe_delivery.minigame and self.shoe_delivery.minigame.is_active():
                        self.shoe_delivery.minigame.active = False
                        self.popup.show_message("Izašao si iz miniigre za popravak.", 1.5)
                    elif self.hedgehog_minigame.is_active():
                        self.hedgehog_minigame.active = False
                        self.hedgehog_minigame.visible = False
                    else:
                        self.settings_popup.toggle()
                        self.help_popup.visible = False
                if self.hedgehog_minigame.is_active():
                    self.hedgehog_minigame.handle_input()
            elif e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
                if self.settings_popup.visible:
                    action = self.settings_popup.handle_mouse_click()
                    if action == "Quit Game":
                        pg.quit()
                        sys.exit()
                    elif action == "Continue":
                        self.settings_popup.toggle()
                    elif action == "Quests":
                        self.quest_popup.toggle()
                    elif action == "Help":
                        self.help_popup.visible = True 
                if self.quest_popup.visible:
                    self.quest_popup.handle_mouse_click(e)
                mouse_pos = e.pos
                self.inventory_popup.handle_item_click(mouse_pos)
                self.chest_popup.handle_item_click(mouse_pos)
            elif e.type == pg.MOUSEWHEEL:
                if self.quest_popup.visible:
                    self.quest_popup.handle_mouse_wheel(e)
            self.berry_minigame.handle_event(e)
                     

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

async def run( app ):
    while True:
        if app.menu is not None:
            app.menu.draw()
            app.menu.handle_events()
            
        else:    
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
