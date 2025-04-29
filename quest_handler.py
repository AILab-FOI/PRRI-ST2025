import random
import questRepository
import inventoryRepository
from settings import *

class QuestHandler:
    def __init__(self, app, MAP, entity_repository):
        self.app = app
        self.MAP = MAP
        self.entity_repository = entity_repository
        questRepository.load_quests_from_json()
        questRepository.get_quest_by_id(0).startQuest()

    def fix_backpack(self):
        quest = questRepository.get_quest_by_id(0)
        player_inventory = inventoryRepository.get_inventory_by_entity_name('player')

        if not hasattr(self, 'repair_in_progress'):
            self.repair_in_progress = False
            self.repair_start_time = 0
            self.repair_duration = 5000

        def start_repair():
            self.repair_in_progress = True
            self.repair_start_time = pg.time.get_ticks()

        def update_repair():
            if self.repair_in_progress:
                current_time = pg.time.get_ticks()
                elapsed_time = current_time - self.repair_start_time

                if elapsed_time >= self.repair_duration:
                    self.repair_in_progress = False
                    finish_repair()

        def finish_repair():
            self.app.popup.show_message("Torba je popravljena!", 1)
            player_inventory.remove_item('backpack')
            quest.setStage(2)

        update_repair()

        if self.__check_if_close_to_entity('chest'):
            self.app.chest_popup.visible = True
        else:
            self.app.chest_popup.visible = False
        
        if quest.current_stage == 0:
            if self.__check_if_close_to_entity('MajstorIvan'):
                self.app.popup.show_message(
                    "Dobro došao! Prije nego kreneš u pustolovinu, moraš popraviti svoju torbu. "
                    "Imaš u škrinji neke stvari koji će ti pomoći, zajedno s tvojom torbom. Sretno!",
                    0.5
                )

            if player_inventory.contains_item('backpack'):
                quest.setStage(1)

        elif quest.current_stage == 1:
            if self.__check_if_close_to_entity('anvil'):
                if not self.repair_in_progress:
                    self.app.popup.show_message("Pritisnite tipku E za popravak torbe.", 0.5)
                    keys = pg.key.get_pressed()
                    if keys[pg.K_e]:
                        self.app.popup.show_message("Popravljanje u tijeku...", 5)
                        start_repair()
                        backpack = player_inventory.get_item('backpack')
                        player_inventory.remove_item(backpack)

        elif quest.current_stage == 2:
            if self.__check_if_close_to_entity('MajstorIvan'):
                self.app.popup.show_message(
                    "Legendarni zlatni šav... Jedina nit koja može spojiti ono što je jednom bilo izgubljeno.\n"
                    "Kažu da se nalazi samo onima koji pokažu dovoljno strpljenja i hrabrosti.\n"
                    "Požuri do Majstora Marka da ti pokaže što ti je dalje činiti!",
                    3
                )

                quest.endQuest()
                questRepository.get_quest_by_id(1).startQuest()
                questRepository.get_quest_by_id(2).startQuest()

    def find_hedgehog(self):
        def find_hedgehog_location(random_hedgehog_index):
            return self.entity_repository[random_hedgehog_index]

        quest = questRepository.get_quest_by_id(1)
        player_inventory = inventoryRepository.get_inventory_by_entity_name('player')

        if(quest.current_stage == 0):
            if self.__check_if_close_to_entity('SeljankaMara'):
                self.app.popup.show_message("Ijao izgubila sam ježa !!!\n Možeš li mi pomoći pronaći ga? Trebao bi biti na jednom od puteljaka.", 2)

                self.random_index = random.randint(0, len(self.entity_repository) - 1)
                jez = find_hedgehog_location(self.random_index)
                jez.invisible = False

                quest.setStage(1)
                
        elif quest.current_stage == 1:
            if self.__check_if_close_to_entity(self.entity_repository[self.random_index].name):
                self.app.popup.show_message("Pritisnite tipku E za pokupiti ježa.", 0.5)
                keys = pg.key.get_pressed()

                if keys[pg.K_e]:
                    if not self.app.hedgehog_minigame.is_active():
                        self.app.popup.show_message("Pritisni tipku E kako bi uhvatio ježa.", 0.5)
                        keys = pg.key.get_pressed()
                        if keys[pg.K_e]:
                            def on_success():
                                hedgehog = inventoryRepository.create_item('hedgehog')
                                inventoryRepository.get_inventory_by_entity_name('player').add_item(hedgehog)

                                jez = find_hedgehog_location(self.random_index)
                                jez.invisible = True

                                if(player_inventory.contains_item('hedgehog')):
                                    quest.setStage(2)

                            self.app.hedgehog_minigame.on_success = on_success
                            self.app.hedgehog_minigame.start()

        elif quest.current_stage == 2:
            if self.__check_if_close_to_entity('SeljankaMara'):
                player_inventory.remove_item(player_inventory.get_item('hedgehog'))
                self.app.popup.show_message("Hvala ti puno, evo ti nagrada!", 1)
                quest.endQuest()
        elif quest.is_completed:
            if not hasattr(self, 'quest_start_time'):
                self.quest_start_time = pg.time.get_ticks()

            current_time = pg.time.get_ticks()
            elapsed_time = current_time - self.quest_start_time

            if elapsed_time >= 60000:
                questRepository.get_quest_by_id(1).startQuest()
                delattr(self, 'quest_start_time')
                self.app.popup.show_message("Seljanka Mara te ponovno traži", 2)
    
    def __check_if_close_to_entity(self, npc_name, is_press_needed=False):
        player_pos = self.app.player.offset / TILE_SIZE
        npc_pos = self.__find_entity_pos_in_map(npc_name)
        
        if npc_pos and player_pos.distance_to(npc_pos) < 1.0:
            if is_press_needed:
                keys = pg.key.get_pressed()
                if keys[pg.K_e]:
                    return True
            else:
                return True
        return False
    
    def __find_entity_pos_in_map(self, npc_name):
        for j, row in enumerate(self.MAP):
            for i, name in enumerate(row):
                if name == npc_name:
                    npc_pos = vec2(i, j) + vec2(0.5)
                    break
        return npc_pos