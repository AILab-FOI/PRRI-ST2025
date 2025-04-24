import inventoryRepository
from popup import InventoryPopup
import questRepository
from stacked_sprite import *
from random import uniform
from entity import Entity
from cache import Cache
from player import Player
import threading

P = 'player'
M = 'MajstorIvan' #NPC
MM = 'MajstorMarko'
MD = 'Karlo'
ML = 'Tomislav'
MJ = 'Zora'
S = 'SeljankaMara'
d1, d2, d3, t, c, a, b = 'blue_tree', 'drvo', 'breza', 'grass', 'chest', 'anvil', 'bunar', 
J = 'jez'
ST = 'stol_majstor'
C = 'crafting'
RS = 'radni_stol'

MAP = [
    [d1, 0, d3, t, t, 0, d1, 0, t, 0, d1, 0, d3, t, d1],
    [t, 0, t, d2, 0, MD, 0, t, t, 0, d2, 0, d1, 0, d2],
    [0, RS, 0, C, 0, t, d3, 0, 0, d2, 0, b, d2, t, d3],
    [d2, t, t, 0, t, 0, t, 0, S, t, t, d1, J, t, 0],
    [0, M, 0, P, 0, a, t, 0, 0, d3, t, t, d3, d2, 0],
    [t, d3, 0, t, 0, t, 0, d2, 0, 0, d1, t, 0, t, d1],
    [c, 0, t, d1, MM, t, b, 0, 0, d3, 0, t, d3, 0, t],
    [0, ML, 0, 0, t, 0, MJ, 0, d1, t, d2, t, t, d1, d3],
    [d1, t, d3, t, 0, d3, 0, d2, 0, t, 0, d2, d2, t, d1],

]

MAP_SIZE = MAP_WIDTH, MAP_HEIGHT = vec2(len(MAP), len(MAP[0]))
MAP_CENTER = MAP_SIZE / 2


class Scene:
    def __init__(self, app):
        self.app = app
        self.transform_objects = []
        self.entity_repository = {}
        self.load_scene()

        self.app.hint_popup.start_time = pg.time.get_ticks()  
        self.app.hint_popup.visible = True  
        self.repairing = False
        self.repaired = False
        self.repairing_start_time = None
        self.success_message_time = None
        self.repair_duration = 7000
        questRepository.get_quest_by_id(0).startQuest()
        questRepository.get_quest_by_id(1).startQuest()

    def load_scene(self):
        rand_rot = lambda: uniform(0, 360)
        rand_pos = lambda pos: pos + vec2(uniform(-0.25, 0.25))

        for j, row in enumerate(MAP):
            for i, name in enumerate(row):
                pos = vec2(i, j) + vec2(0.5)
                if name == 'player':
                    self.app.player.offset = pos * TILE_SIZE
                elif name == 'MajstorIvan':
                    Entity(self.app, name=name, pos=pos)
                elif name == 'SeljankaMara':
                    Entity(self.app, name=name, pos=pos)
                elif name == 'MajstorMarko':
                    Entity(self.app, name=name, pos=pos)
                elif name == 'Karlo':
                    Entity(self.app, name=name, pos=pos)
                elif name == 'Zora':
                    Entity(self.app, name=name, pos=pos)
                elif name == 'Tomislav':
                    Entity(self.app, name=name, pos=pos)
                elif name == 'blue_tree':
                    TrnspStackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
                elif name == 'grass':
                    StackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot(),
                                  collision=False)
                elif name == 'drvo':
                    TrnspStackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
                elif name == 'breza':
                    TrnspStackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
                elif name == 'jez':
                    entity = Entity(self.app, name=name, pos=pos)
                    self.entity_repository.setdefault(name, []).append(entity)
                elif name == 'stol_majstor':
                    TrnspStackedSprite(self.app, name=name, pos=pos)
                elif name == 'crafting':
                    TrnspStackedSprite(self.app, name=name, pos=pos)
                elif name == 'radni_stol':
                    TrnspStackedSprite(self.app, name=name, pos=pos)
                elif name:
                    StackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())

    def get_closest_object_to_player(self):
        closest = sorted(self.app.transparent_objects, key=lambda e: e.dist_to_player)
        closest[0].alpha_trigger = True
        closest[1].alpha_trigger = True

    def transform(self):
        for obj in self.transform_objects:
            obj.rot = 30 * self.app.time

    def update(self):
        

        if self.check_anvil_interaction():
            if not self.repairing and not self.repaired:  
                self.app.popup.show_message("Pritisnite tipku E za popravak torbe.", 0.5)
                keys = pg.key.get_pressed()
                if keys[pg.K_e]:  
                    self.start_repair()  
            elif self.repaired:
                self.app.popup.show_message("Torba je uspješno popravljena! \n Vrati se do majstora Ivana, sigurno čuva neke tajne...", 0.5)  

        self.update_repair()
        self.check_if_close_to_chest()
        self.check_npc_interaction()
        self.check_first_quest()
        self.check_second_quest()

    def check_anvil_interaction(self):
        player_pos = self.app.player.offset / TILE_SIZE
        anvil_pos = None
        
        for j, row in enumerate(MAP):
            for i, name in enumerate(row):
                if name == 'anvil':
                    anvil_pos = vec2(i, j) + vec2(0.5)
                    break
        
        return anvil_pos and player_pos.distance_to(anvil_pos) < 0.35

    def start_repair(self):
        if not self.repairing and not self.repaired:  
            self.repairing = True
            self.repairing_start_time = pg.time.get_ticks()
            self.app.popup.show_message("Popravak torbe u tijeku... Pričekaj ovdje...", 5.5)

    def check_if_close_to_chest(self):
        player_pos = self.app.player.offset / TILE_SIZE
        chest_pos = None

        for j, row in enumerate(MAP):
            for i, name in enumerate(row):
                if name == 'chest':
                    chest_pos = vec2(i, j) + vec2(0.5)
                    break

        if chest_pos and player_pos.distance_to(chest_pos) < 0.65:
            self.app.chest_popup.visible = True
        else:
            self.app.chest_popup.visible = False

    def update_repair(self):
        if self.repairing:
            elapsed_time = pg.time.get_ticks() - self.repairing_start_time
            if elapsed_time >= self.repair_duration:  
                self.repairing = False
                self.repaired = True  
                self.repairing_start_time = None
                self.success_message_time = pg.time.get_ticks()  
    

    def check_npc_interaction(self):
        player_pos = self.app.player.offset / TILE_SIZE
        majstor_pos = None
        for j, row in enumerate(MAP):
            for i, name in enumerate(row):
                if name == 'MajstorIvan':
                    majstor_pos = vec2(i, j) + vec2(0.5)
                    break
        if majstor_pos and player_pos.distance_to(majstor_pos) < 0.65:
            self.app.popup.show_message("Dobro došao! Prije nego kreneš u pustolovinu, moraš popraviti svoju torbu. Imaš u chestu neke iteme koji će ti pomoći. Sretno!", 0.5)
            if self.repaired:  
                self.app.popup.show_message("Legendarni zlatni šav... Jedina nit koja može spojiti ono što je jednom bilo izgubljeno.\n"
                                            "Kažu da se nalazi samo onima koji pokažu dovoljno strpljenja i hrabrosti.\n"
                                            "Požuri do Seljanke Mare kako bi nastavio svoj put!", 0.5)
            return True
        return False     

    def check_npc_interaction2(self):
        player_pos = self.app.player.offset / TILE_SIZE
        mara_pos = None

        for j, row in enumerate(MAP):
            for i, name in enumerate(row):
                if name == 'SeljankaMara':
                    mara_pos = vec2(i, j) + vec2(0.5)
                    break
        if mara_pos and player_pos.distance_to(mara_pos) < 0.65:
            self.app.popup.show_message("Ijao izgubila sam ježa !!!\n Možeš li mi pomoći pronaći ga? Trebao bi biti na jednom od puteljaka. \n Pravi put je prekriven lišćem... ali ne svakakvim – onim što kao da šapće pod tvojim koracima.", 0.5)
            return True
        return False 
    
    def check_first_quest(self):
        quest = questRepository.get_quest_by_id(0)
        player_inventory = inventoryRepository.get_inventory_by_entity_name('player')
        
        if quest.current_stage == 0:
            if player_inventory.contains_item('backpack'):
                quest.setStage(1)
        elif quest.current_stage == 1:
            if self.check_anvil_interaction():
                self.app.popup.show_message("Pritisnite tipku E za popravak torbe.", 0.5)
                keys = pg.key.get_pressed()
                if keys[pg.K_e]:
                    self.start_repair()
                    player_inventory.remove_item('backpack')
                    quest.setStage(2)
        elif quest.current_stage == 2:
            quest.is_completed = True
            quest.is_active = False
            quest.setStage(-1)

    def check_second_quest(self):
        quest = questRepository.get_quest_by_id(1)
        player_inventory = inventoryRepository.get_inventory_by_entity_name('player')

        if(quest.current_stage == 0):
            if self.check_npc_interact('SeljankaMara'):
                self.app.popup.show_message("Ijao izgubila sam ježa !!!\n Možeš li mi pomoći pronaći ga? Trebao bi biti na jednom od puteljaka. \n Pravi put je prekriven lišćem... ali ne svakakvim – onim što kao da šapće pod tvojim koracima.", 3)
                quest.setStage(1)
        elif quest.current_stage == 1:
            if self.check_npc_interact('jez'):
                self.app.popup.show_message("Pritisnite tipku E za pokupiti ježa.", 0.5)
                keys = pg.key.get_pressed()

                if keys[pg.K_e]:
                    inventoryRepository.switch_items_from_inventories('jez', 'player', 'hedgehog')

                    for j, row in enumerate(MAP):
                        for i, name in enumerate(row):
                            if name == 'jez':
                                jez_list = self.entity_repository.get('jez', [])

                                if jez_list:
                                    jez = jez_list[0]
                                    jez.collision = False
                                    jez.invisible = True
                                    break

                    if(player_inventory.contains_item('hedgehog')):
                        quest.setStage(2)
        elif quest.current_stage == 2:
            if self.check_npc_interact('SeljankaMara'):
                self.app.popup.show_message("Hvala ti puno, evo ti nagrada!", 3)
                player_inventory.remove_item(player_inventory.get_item('hedgehog'))
                #todo make jez appear near mara
                quest.setStage(-1)
                quest.is_active = False
                quest.is_completed = True
    
    def check_npc_interact(self, npc_name, is_press_needed=False):
        player_pos = self.app.player.offset / TILE_SIZE
        npc_pos = None

        for j, row in enumerate(MAP):
            for i, name in enumerate(row):
                if name == npc_name:
                    npc_pos = vec2(i, j) + vec2(0.5)
                    break
        if npc_pos and player_pos.distance_to(npc_pos) < 1.0:
            if is_press_needed:
                keys = pg.key.get_pressed()
                if keys[pg.K_e]:
                    return True
            else:
                return True
        return False
    
    def check_if_close_to_entity(self, entity_name):
        player_pos = self.app.player.offset / TILE_SIZE
        entity_pos = None

        for j, row in enumerate(MAP):
            for i, name in enumerate(row):
                if name == entity_name:
                    entity_pos = vec2(i, j) + vec2(0.5)
                    break

        if entity_pos and player_pos.distance_to(entity_pos) < 0.65:
            return True
        return False

def run_in_thread(func, args=None, kwargs=None, callback=None):
    if args is None:
        args = ()
    if kwargs is None:
        kwargs = {}

    def wrapped_func():
        result = func(*args, **kwargs)
        if callback:
            callback()

    thread = threading.Thread(target=wrapped_func)
    thread.start()
    return thread
        
        

class LoadingScene:
    def __init__(self, app):
        self.app = app
        self.font = pg.font.Font("assets/PressStart2P-Regular.ttf", 16)
        self.progress = 0
        self.messages = [
            'Loading assets...',
            'Setting up player...',
            'Initializing game...',
            'Checking the weather...',
            'Thinking about the meaning of life...',
            'Resting...',
            'Contemplating life decisions...',
            'Talking to myself...',
            'Drinking coffee...',
            "Starring at my mobile...",
            "Doing nothing...",
            "A little bit more nothing...",
            'Almost done...',
            'Or not...',
            'Maybe...',
            "I have no idea what I'm doing...",
            
        ]
        self.bar_width = int( WIDTH / 3.0 )
        self.bar_height = int( HEIGHT / 56.33 )
        self.MAX = len( STACKED_SPRITE_ATTRS )
        self.done = False
        self.app.cache = Cache(self.app)
        self.app.cache.get_entity_sprite_cache()
        self.stacked_sprite_iterator = self.app.cache.get_stacked_sprite_cache()

    def done_cache( self ):
        self.done = True
        

    def update(self):
        counter = next(self.stacked_sprite_iterator, 'done')
        if counter == 'done':
            self.done_cache()
        if self.done:
            # Switch to the game scene after loading is complete
            self.app.player = Player(self.app)
            self.app.scene = Scene(self.app)
        else:
            # Simulate loading progress
            self.progress = self.app.done_counter / self.MAX * len( self.messages )



    def draw(self):
        #self.app.screen.fill(BG_COLOR)
        self.bg_img = pg.image.load('assets/images/splash.png')
        self.bg_img = pg.transform.smoothscale( self.bg_img, self.app.screen.get_size())
        self.app.screen.blit(self.bg_img, self.bg_img.get_rect())
        screen_center_x = self.app.screen.get_width() // 2
        screen_center_y = self.app.screen.get_height() // 100 * 85

        # Display the current message based on progress
        current_message_index = min(int(self.progress), len(self.messages) - 1)
        msg = self.messages[current_message_index]
        text = self.font.render(msg, True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_center_x, screen_center_y + 80))
        self.app.screen.blit(text, text_rect)

        # Draw the progress bar background
        bar_bg_rect = pg.Rect(0, 0, self.bar_width, self.bar_height)
        bar_bg_rect.center = (screen_center_x, screen_center_y + 40)
        pg.draw.rect(self.app.screen, (204, 239, 253), bar_bg_rect)

        # Draw the progress bar
        progress_width = int(self.progress / len(self.messages) * self.bar_width)
        bar_rect = pg.Rect(0, 0, progress_width, self.bar_height)
        bar_rect.midleft = bar_bg_rect.midleft
        pg.draw.rect(self.app.screen, (255, 0, 0), bar_rect)










