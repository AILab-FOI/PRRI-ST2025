from quest_handler import QuestHandler
from popup import InventoryPopup
import questRepository
from stacked_sprite import *
from random import uniform
from entity import Entity
from cache import Cache
from player import Player
import threading
import pygame as pg

P = 'player'
M = 'MajstorIvan' #NPC
MM = 'MajstorMarko'
MD = 'Karlo'
ML = 'Tomislav'
MJ = 'Zora'
S = 'SeljankaMara'
PD = 'poljoprivrednikDuro'
d1, d2, d3, t, c, a, b = 'blue_tree', 'drvo', 'breza', 'grass', 'chest', 'anvil', 'bunar', 
J1,J2,J3,J4 = 'jez', 'jez2', 'jez3', 'jez4'
ST = 'stol_majstor'
C = 'crafting'
RS = 'radni_stol'
GM, GJ, GB = 'grm_malina', 'grm_jagoda', 'grm_borovnica'

NPC_SPRITES = [M,MM,MD,ML,MJ,S,PD]

MAP = [
    [d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2],
    [d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3],
    [d2, t, c, t, t, d3, t, ML, t, d3, J3, t, t, J1, t, GB, t, GM, t, d3, d2],
    [d3, RS, t, t, t, t, t, t, t, MD, t, t, t, t, d2, t, t, t, t, d2, d3],
    [d2, C, t, P, M, d2, t, MM, t, t, d2, t, S, t, t, t, PD, t, t, d3, d2],
    [d3, a, t, t, t, t, t, t, t, t, t, t, t, t, t, d3, t, t, t, d3, d2],
    [d2, t, t, t, d3, t, MJ, t, d3, J2, t, t, t, J4, t, t, t, GJ, t, d2, d3],
    [d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3],
    [d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2, d3, d2]
]

MAP_SIZE = MAP_WIDTH, MAP_HEIGHT = vec2(len(MAP), len(MAP[0]))
MAP_CENTER = MAP_SIZE / 2


class Scene:
    def __init__(self, app):
        self.app = app
        self.transform_objects = []
        self.entity_repository = []
        self.load_scene()
        self.questHandler = QuestHandler(self.app, MAP, self.entity_repository)

        self.app.hint_popup.start_time = pg.time.get_ticks()  
        self.app.hint_popup.visible = True

        self.MaraJez = False
        self.cozy_tutorial = True
        self.npc_dialog_index = 0
        self.npc_dialog_active = False
        self.npc_dialog_last_space = 0
        self.npc_dialog_lines = [
            "Dobro došao! Prije nego posjetiš Seljanku Maru pokazat ću ti kako da popravljaš cipele. \n[Pritisni SPACE da nastaviš razgovor...]",
            "Prvo preuzmi cipele od mene kada stignu. Uvijek će ti doći podsjetnik da su cipele došle. Kao što sada vidiš.\n[Pritisni SPACE da nastaviš razgovor...]",
            "Zatim idi do stola za popravak i popravi cipele!\n[Pritisni SPACE da nastaviš razgovor...]",
            "Kad završiš, odneseš ih osobi kojoj su namijenjene. Vidjet ćeš u gornjem desnom uglu ekrana sliku osobe kojoj moraš donijeti cipele.\n[Pritisni SPACE da nastaviš razgovor...]",
            "Ja ću svako malo dobivati cipele za popravak, tako da navrati kada vidiš podsjetnik na vrhu ekrana. Sretno u popravku!\n[Pritisni SPACE da završiš razgovor...]"
        ]

    def load_scene(self):
        rand_rot = lambda: uniform(0, 360)
        rand_pos = lambda pos: pos + vec2(uniform(-0.25, 0.25))

        for j, row in enumerate(MAP):
            for i, name in enumerate(row):
                pos = vec2(i, j) + vec2(0.5)
                if name == 'player':
                    self.app.player.offset = pos * TILE_SIZE
                elif name in NPC_SPRITES:
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
                elif name == 'jez' or name == 'jez2' or name == 'jez3' or name == 'jez4':
                    entity = Entity(self.app, name=name, pos=pos)
                    entity.invisible = True
                    self.entity_repository.append(entity)
                elif name == 'stol_majstor':
                    TrnspStackedSprite(self.app, name=name, pos=pos)
                elif name == 'crafting':
                    TrnspStackedSprite(self.app, name=name, pos=pos)
                elif name == 'grm_borovnica':
                    TrnspStackedSprite(self.app, name=name, pos=pos)
                elif name == 'grm_jagoda':
                    TrnspStackedSprite(self.app, name=name, pos=pos)
                elif name == 'grm_malina':
                    TrnspStackedSprite(self.app, name=name, pos=pos)
                elif name == 'radni_stol':
                    TrnspStackedSprite(self.app, name=name, pos=pos)
                elif name == 'chest':
                    TrnspStackedSprite(self.app, name=name, pos=pos, rot=-90)
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
        self.check_npc_interaction3()
        self.questHandler.check_quests()
    
    #NPC KOJI POKAZUJE COZY MEHANIKU
    def check_npc_interaction3(self):
        player_pos = self.app.player.offset / TILE_SIZE
        majstorMarko_pos = None

        for j, row in enumerate(MAP):
            for i, name in enumerate(row):
                if name == 'MajstorMarko':
                    majstorMarko_pos = vec2(i, j) + vec2(0.5)
                    break

        if majstorMarko_pos and player_pos.distance_to(majstorMarko_pos) < 0.65 and self.cozy_tutorial == True:
            keys = pg.key.get_pressed()
            current_time = pg.time.get_ticks()
            self.app.popup.show_message(self.npc_dialog_lines[self.npc_dialog_index], 1)
            if keys[pg.K_SPACE] and current_time - self.npc_dialog_last_space > 300:
                self.npc_dialog_last_space = current_time
                self.npc_dialog_index += 1
                if self.npc_dialog_index == 5:
                    self.cozy_tutorial = False
                    self.npc_dialog_index = 0
                if self.npc_dialog_index == 1:
                    self.app.shoe_pickup.visible = True
                if self.npc_dialog_index == 2:
                    self.app.shoe_pickup.visible = False
                if self.npc_dialog_index == 3:
                    self.app.delivery_popup.visible = True
                if self.npc_dialog_index == 4:
                    self.app.delivery_popup.visible = False
                    self.app.cozy_mechanic_begin = True
                if self.npc_dialog_index < len(self.npc_dialog_lines):
                    self.app.popup.show_message(self.npc_dialog_lines[self.npc_dialog_index], 1)
        else:
            self.npc_dialog_index = 0

    def check_if_close_to_entity(self, npc_name, is_press_needed=False):
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

        current_message_index = min(int(self.progress), len(self.messages) - 1)
        msg = self.messages[current_message_index]
        text = self.font.render(msg, True, (255, 255, 255))
        text_rect = text.get_rect(center=(screen_center_x, screen_center_y + 80))
        self.app.screen.blit(text, text_rect)

        bar_bg_rect = pg.Rect(0, 0, self.bar_width, self.bar_height)
        bar_bg_rect.center = (screen_center_x, screen_center_y + 40)
        pg.draw.rect(self.app.screen, (204, 239, 253), bar_bg_rect)

        progress_width = int(self.progress / len(self.messages) * self.bar_width)
        bar_rect = pg.Rect(0, 0, progress_width, self.bar_height)
        bar_rect.midleft = bar_bg_rect.midleft
        pg.draw.rect(self.app.screen, (255, 0, 0), bar_rect)










