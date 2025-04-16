import pygame as pg
import random
import time
import inventoryRepository
import threading
from stacked_sprite import *

class ShoeDelivery:
    def __init__(self, app):
        self.app = app
        self.last_generation_time = pg.time.get_ticks()
        self.generation_interval = 40000  
        self.unrepaired_shoes = 0
        self.repaired_shoes = 0
        self.max_unrepaired = 1
        self.pickup = False
        self.delivery_npcs = ['MajstorDalibor', 'MajstorLuka', 'MajstorJanko']  
        self.current_delivery_npc = None
        self.player_inventory = inventoryRepository.get_inventory_by_entity_name('player')
        self.npc_inventory = inventoryRepository.get_inventory_by_entity_name('MajstorMarko')

    def update(self):
        current_time = pg.time.get_ticks()

        if self.unrepaired_shoes == 0:
            if current_time - self.last_generation_time >= self.generation_interval:
                self.generate_shoes()
                self.last_generation_time = current_time
        if(self.pickup == True):
            self.check_shoe_pickup()
        self.check_repair()
        self.check_delivery()

    def generate_shoes(self):
        self.app.popup.show_message("Stigle su nove cipele za popravak kod Majstora Marka!", 3)
        self.pickup = True
        self.npc_inventory.add_item(inventoryRepository.create_item('unrepairedShoes'))

        
    def check_shoe_pickup(self):
        if self.app.scene.check_if_close_to_entity('MajstorMarko') and self.pickup:
            self.app.popup.show_message("Pritisni E da preuzmeš cipele za popravak.", 2)
            keys = pg.key.get_pressed()
            if keys[pg.K_e]:
                self.unrepaired_shoes += 1 
                self.app.popup.show_message("Preuzeo si cipele! Odnesi ih na popravak.", 3)
                self.pickup = False
                inventoryRepository.switch_items_from_inventories('MajstorMarko', 'player', 'unrepairedShoes')


    def check_repair(self):
        if self.unrepaired_shoes == 1 and self.app.scene.check_if_close_to_entity('crafting'):
            self.app.popup.show_message("Pritisni E kako bi popravio cipele!", 1)
            keys = pg.key.get_pressed()
            if keys[pg.K_e]:
                self.unrepaired_shoes -= 1
                self.repaired_shoes += 1
                delivery_npc = random.choice(self.delivery_npcs)
                self.current_delivery_npc = delivery_npc
                self.app.popup.show_message(f"Cipele popravljene! Dostavi ih NPC-u: {delivery_npc}.", 3)
                self.player_inventory.add_item(inventoryRepository.create_item('repairedShoes'))
                self.player_inventory.remove_item(self.player_inventory.get_item('unrepairedShoes'))

    def check_delivery(self):
        if self.repaired_shoes == 0 or not self.current_delivery_npc:
            return

        if self.app.scene.check_if_close_to_entity(self.current_delivery_npc):
            self.app.popup.show_message("Pritisni E kako bi predao cipele!", 1)
            keys = pg.key.get_pressed()
            if keys[pg.K_e]:
                self.repaired_shoes -= 1
                self.app.popup.show_message(f"Dostava cipela NPC-u {self.current_delivery_npc} obavljena! Bravo!", 3)
                inventoryRepository.switch_items_from_inventories('player', self.current_delivery_npc, 'repairedShoes')
                self.current_delivery_npc = None