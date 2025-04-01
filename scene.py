from stacked_sprite import *
from random import uniform
from entity import Entity
from cache import Cache
from player import Player
import threading

P = 'player'
K = 'kitty'  # entity
A, B, C, D, E, F, G, H, CH, AN = 'van', 'tank', 'blue_tree', 'car', 'grass', 'crate', 'cup', 'pancake', 'chest', 'anvil'
S = 'sphere' # transform object

MAP = [
    [0, E, 0, E, B, 0, E, 0, 0, E, 0, E, 0, E],
    [E, C, C, C, 0, C, C, CH, E, 0, C, C, C, 0],
    [0, C, 0, 0, 0, 0, E, C, 0, C, 0, H, K, C],
    [C, 0, 0, E, AN, 0, 0, C, C, 0, 0, 0, 0, C],
    [C, E, 0, 0, P, CH, 0, E, 0, 0, F, E, 0, C],
    [C, 0, 0, A, E, D, E, S, 0, F, 0, 0, C, 0],
    [0, C, E, AN, 0, 0, E, 0, E, 0, 0, B, C, E],
    [0, C, C, 0, E, 0, C, C, 0, G, E, C, 0, 0],
    [E, 0, 0, C, C, C, C, 0, C, C, C, 0, E, 0],
]

MAP_SIZE = MAP_WIDTH, MAP_HEIGHT = vec2(len(MAP), len(MAP[0]))
MAP_CENTER = MAP_SIZE / 2


class Scene:
    def __init__(self, app):
        self.app = app
        self.transform_objects = []
        self.load_scene()
        self.app.message.set_message( self.app.player.message )
        self.app.message.active = True

    def load_scene(self):
        rand_rot = lambda: uniform(0, 360)
        rand_pos = lambda pos: pos + vec2(uniform(-0.25, 0.25))

        for j, row in enumerate(MAP):
            for i, name in enumerate(row):
                pos = vec2(i, j) + vec2(0.5)
                if name == 'player':
                    self.app.player.offset = pos * TILE_SIZE
                elif name == 'kitty':
                    Entity(self.app, name=name, pos=pos)
                elif name == 'blue_tree':
                    TrnspStackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
                elif name == 'grass':
                    StackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot(),
                                  collision=False)
                elif name == 'sphere':
                    obj = StackedSprite(self.app, name=name, pos=rand_pos(pos), rot=rand_rot())
                    self.transform_objects.append(obj)
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
        self.get_closest_object_to_player()
        self.transform()




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
        text = self.font.render(msg, True, (0, 0, 0))
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
        pg.draw.rect(self.app.screen, (221, 220, 79), bar_rect)










