import pygame as pg
import random
import inventoryRepository

class Minigame:
    def __init__(self, app):
        self.app = app
        self.surface = pg.Surface((600, 350), pg.SRCALPHA)
        self.rect = self.surface.get_rect(center=(app.screen.get_width() // 2, app.screen.get_height() // 2))

        self.slider_width = 400
        self.slider_left = 100
        self.slider_top = 140
        self.slider_height = 50

        self.pointer_x = self.slider_left
        self.pointer_speed = 2.5
        self.direction = 1

        self.zone_left = self.slider_left + 180
        self.zone_width = 40
        self.hits = 0
        self.max_hits = 3
        self.active = True
        self.last_space = 0

        self.game_font = pg.font.Font("assets/PressStart2P-Regular.ttf", 20)
        self.instruction_font = pg.font.Font("assets/PressStart2P-Regular.ttf", 14)
        self.background_color = (224, 200, 160)
        self.border_color = (139, 93, 60)
        self.text_color = (50, 30, 10)
        self.target_color = (139, 69, 19)

    def update(self):
        if not self.active:
            return

        self.pointer_x += self.pointer_speed * self.direction
        if self.pointer_x <= self.slider_left or self.pointer_x >= self.slider_left + self.slider_width:
            self.direction *= -1

        keys = pg.key.get_pressed()
        if keys[pg.K_SPACE]:
            if self.zone_left <= self.pointer_x <= self.zone_left + self.zone_width:
                current_time = pg.time.get_ticks()
                if current_time - self.last_space > 500:
                    self.hits += 1
                    self.last_space = current_time

        if self.hits >= self.max_hits:
            self.finish_repair()

    def finish_repair(self):
        shoe_delivery = self.app.shoe_delivery
        shoe_delivery.unrepaired_shoes -= 1
        shoe_delivery.repaired_shoes += 1
        delivery_npc = random.choice(shoe_delivery.delivery_npcs)
        shoe_delivery.current_delivery_npc = delivery_npc
        shoe_delivery.spremno_za_predaju = True
        #shoe_delivery.minigame = None
        self.active = False

    def draw(self):
        if not self.active:
            return

        popup_bg_color = (139, 93, 60) 
        pg.draw.rect(self.surface, popup_bg_color, self.surface.get_rect(), border_radius=12)
        pg.draw.rect(self.surface, self.background_color, self.surface.get_rect().inflate(-12, -12), border_radius=8)
        
        pg.draw.rect(self.surface, self.target_color, (self.zone_left, self.slider_top, self.zone_width, self.slider_height))
        pg.draw.rect(self.surface, self.border_color, (self.slider_left, self.slider_top, self.slider_width, self.slider_height), 4)

        pg.draw.rect(self.surface, (255, 255, 0), (int(self.pointer_x), self.slider_top, 6, self.slider_height))
        progress = self.hits / self.max_hits
        pg.draw.rect(self.surface, (190, 170, 140), (100, 300, 400, 12))
        pg.draw.rect(self.surface, (0, 200, 0), (100, 300, int(400 * progress), 12))

        text = self.game_font.render(f"Pogodi još {self.max_hits - self.hits} puta", True, self.text_color)
        self.surface.blit(text, (100, 40))
        self.instruction_font = pg.font.Font("assets/PressStart2P-Regular.ttf", 13)
        instruction_text = self.instruction_font.render("Pritisni SPACE da popraviš cipelu!", True, self.text_color)
        self.surface.blit(instruction_text, (100, 270))
        self.app.screen.blit(self.surface, self.rect.topleft)

    def is_active(self):
        return self.active
