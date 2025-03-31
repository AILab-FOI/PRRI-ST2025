import pygame as pg

class Popup:
    def __init__(self, screen, title, width_ratio=0.6, height_ratio=0.6):
        self.screen = screen
        self.title = title
        self.visible = False

        screen_width, screen_height = self.screen.get_size()
        self.width, self.height = int(screen_width * width_ratio), int(screen_height * height_ratio)
        self.x, self.y = (screen_width - self.width) // 2, (screen_height - self.height) // 2
        self.rect = pg.Rect(self.x, self.y, self.width, self.height)

        self.bg_color = (139, 69, 19)
        self.border_color = (100, 50, 10)
        self.text_color = (255, 255, 255)
        self.rivet_color = (160, 140, 100)
        self.rivet_radius = 6

        self.font = pg.font.Font("assets/PressStart2P-Regular.ttf", 20)
        self.title_font = pg.font.Font("assets/PressStart2P-Regular.ttf", 32)

    def toggle(self):
        self.visible = not self.visible

    def draw(self):
        if not self.visible:
            return
        
        pg.draw.rect(self.screen, self.bg_color, self.rect)
        pg.draw.rect(self.screen, self.border_color, self.rect, 3)
        
        title_surface = self.title_font.render(self.title, True, self.text_color)
        title_rect = title_surface.get_rect(center=(self.screen.get_width() // 2, self.y + 70))
        self.screen.blit(title_surface, title_rect)
        
        for cx in [self.x + 10, self.x + self.width - 10]:
            for cy in [self.y + 10, self.y + self.height - 10]:
                pg.draw.circle(self.screen, self.rivet_color, (cx, cy), self.rivet_radius)

class InventoryPopup(Popup):
    def __init__(self, screen):
        super().__init__(screen, "Inventory")

class SettingsPopup(Popup):
    def __init__(self, screen):
        super().__init__(screen, "Settings")
        self.options = ["Continue", "Help", "Save Game", "Load Game", "Quit Game"]
        self.option_rects = []
        self.hovered_option = None

    def draw(self):
        super().draw()
        
        self.option_rects = []
        for i, option in enumerate(self.options):
            mouse_pos = pg.mouse.get_pos()
            option_rect = pg.Rect(0, 0, self.width * 0.8, 40)
            option_rect.center = (self.screen.get_width() // 2, self.y + 180 + i * 50)
            self.option_rects.append(option_rect)

            is_hovered = option_rect.collidepoint(mouse_pos)
            if is_hovered:
                self.hovered_option = i

            color = (255, 255, 0) if is_hovered else self.text_color
            option_surface = self.font.render(option, True, color)
            option_text_rect = option_surface.get_rect(center=(self.screen.get_width() // 2, self.y + 180 + i * 50))
            self.screen.blit(option_surface, option_text_rect)
    
    def handle_mouse_click(self):
        if self.visible and self.hovered_option is not None:
            return self.options[self.hovered_option]
        return None
    
class MainMenu: 
    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.font = pg.font.Font("assets/PressStart2P-Regular.ttf", 32)
        self.options = ["Start New Game", "Load Game", "Quit"]
        self.selected_option = 0 
    
    def draw(self):
        self.screen.fill((0, 0, 0))  
        title_text = self.font.render("Whispering Tales", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 100))
        self.screen.blit(title_text, title_rect)

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, 320 + i * 60))
            self.screen.blit(text, text_rect)
        pg.display.flip()

    def handle_events(self):
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                exit()
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif e.key == pg.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif e.key == pg.K_RETURN:
                    if self.selected_option == 0:
                        print("Starting new game...")
                        self.app.start_game()  
                    elif self.selected_option == 1:  
                        print("Loading game...")
                    elif self.selected_option == 2: 
                        pg.quit()
                        exit()
