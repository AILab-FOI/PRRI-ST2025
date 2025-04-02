import pygame as pg
import inventoryRepository
import questRepository

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
    def __init__(self, screen, entity_name):
        super().__init__(screen, "Inventory")
        self.inventory = None
        self.entity_name = entity_name
        # todo when save game is implemented, load inventory from save file

    def draw(self):
        if self.inventory is None:
            self.inventory = inventoryRepository.get_inventory_by_entity_name(self.entity_name)

        super().draw()
        item_size = self.width // 6
        padding = 10
        items_per_row = (self.width - 2 * padding) // (item_size + padding)
        start_x = self.x + padding
        start_y = self.y + 120

        self.item_rects = []

        for i, item in enumerate(self.inventory.items):
            row = i // items_per_row
            col = i % items_per_row
            item_x = start_x + col * (item_size + padding)
            item_y = start_y + row * (item_size + padding)

            item_rect = pg.Rect(item_x, item_y, item_size, item_size)
            self.item_rects.append((item_rect, item))
            pg.draw.rect(self.screen, self.bg_color, item_rect)
            pg.draw.rect(self.screen, self.border_color, item_rect, 2)

            if item.icon:
                icon_surface = pg.image.load(item.icon)
                icon_surface = pg.transform.scale(icon_surface, (item_size, item_size))
                self.screen.blit(icon_surface, (item_x, item_y))
            else:
                item_text = self.font.render(item.name[:2], True, (0, 0, 0))
                text_rect = item_text.get_rect(center=item_rect.center)
                self.screen.blit(item_text, text_rect)

    def handle_item_click(self, mouse_pos):
        if self.inventory is None:
            print("Error: Inventory is not loaded.")
            return

        for item_rect, item in self.item_rects:
            if item_rect.collidepoint(mouse_pos) and self.visible == True:
                try:
                    if self.entity_name != "player":
                        inventoryRepository.switch_items_from_inventories(self.entity_name, "player", item.name)
                        self.inventory = inventoryRepository.get_inventory_by_entity_name(self.entity_name)
                except Exception as e:
                    print(e)
                break

class MessagePopup:
    def __init__(self, app):
        self.app = app
        self.message = ""
        self.show_until = 0
        self.visible = False
        self.font = pg.font.Font(None, 36)
        
        screen_width, screen_height = self.app.screen.get_size()
        self.rect = pg.Rect(
            (screen_width - 600) // 2,  
            screen_height - 150,  
            600,  
            100   
        )
        self.background_color = (50, 50, 50)
        self.border_color = (200, 200, 200)
        self.text_color = (255, 255, 255)

    def show_message(self, text, duration):
        self.message = text
        self.show_until = pg.time.get_ticks() + (duration * 1000)
        self.visible = True  
    
    def hide_message(self):
        self.message = ""
        self.visible = False  
    
    def draw(self):
        if self.visible and pg.time.get_ticks() < self.show_until:
            # Pozadina prozora
            pg.draw.rect(self.app.screen, self.background_color, self.rect, border_radius=10)
            pg.draw.rect(self.app.screen, self.border_color, self.rect, 2, border_radius=10)

            # Prikazivanje poruke
            wrapped_text = self.wrap_text(self.message, self.font, self.rect.width - 20)
            start_y = self.rect.top + 20
            line_height = 30

            for i, line in enumerate(wrapped_text):
                text_surface = self.font.render(line, True, self.text_color)
                text_x = self.rect.left + 10
                y_position = start_y + i * line_height
                self.app.screen.blit(text_surface, (text_x, y_position))

        elif pg.time.get_ticks() >= self.show_until:
            self.hide_message()

    def wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)
        return lines

class SettingsPopup(Popup):
    def __init__(self, screen, help_popup=None):
        super().__init__(screen, "Settings")
        self.options = ["Continue", "Quests", "Help", "Save Game", "Load Game", "Quit Game"]
        self.option_rects = []
        self.hovered_option = None
        self.help_popup = help_popup

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
            selected_option = self.options[self.hovered_option]
            if selected_option == "Help":
                self.help_popup.visible = True  
            return selected_option
        return None

class QuestPopup(Popup):
    def __init__(self, screen):
        super().__init__(screen, "Quests")
        self.quests = questRepository.get_all_quests()
        self.scroll_offset = 0
        self.scroll_step = 30
        self.max_display = 6
        self.text_wrap_width = self.width - 40

        self.close_button_size = 50
        self.close_button_rect = pg.Rect(
            self.x + self.width - self.close_button_size - 15, 
            self.y + 15, 
            self.close_button_size, 
            self.close_button_size)

    def wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            test_width, _ = font.size(test_line)
            
            if test_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines

    def draw(self):
        super().draw()
        if not self.visible:
            return

        start_y = self.y + 120
        line_spacing = 10
        text_height = 0
        
        for i, quest in enumerate(self.quests[self.scroll_offset:self.scroll_offset + self.max_display]):
            quest_name_surface = self.font.render(quest.name, True, self.text_color)
            quest_name_rect = quest_name_surface.get_rect(midtop=(self.screen.get_width() // 2, start_y + text_height))
            self.screen.blit(quest_name_surface, quest_name_rect)
            text_height += self.font.get_height() + line_spacing
            
            wrapped_description = self.wrap_text(quest.description, self.font, self.text_wrap_width)
            
            for line in wrapped_description:
                quest_surface = self.font.render(line, True, self.text_color)
                quest_rect = quest_surface.get_rect(midtop=(self.screen.get_width() // 2, start_y + text_height))
                self.screen.blit(quest_surface, quest_rect)
                text_height += self.font.get_height() + line_spacing
            
            text_height += self.font.get_height()

        pg.draw.rect(self.screen, (139, 69, 19), self.close_button_rect)
        close_text = self.font.render("X", True, (255,255,255))
        close_text_rect = close_text.get_rect(center=self.close_button_rect.center)
        self.screen.blit(close_text, close_text_rect)

    def scroll_up(self):
        if self.scroll_offset > 0:
            self.scroll_offset -= 1

    def scroll_down(self):
        if self.scroll_offset + self.max_display < len(self.quests):
            self.scroll_offset += 1

    def handle_mouse_wheel(self, event):
        if event.y > 0:
            self.scroll_up()
        elif event.y < 0:
            self.scroll_down()

    def handle_mouse_click(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.visible and self.close_button_rect.collidepoint(event.pos):
                self.visible = False
    
#popup hint kako bi igrač znao otvoriti postavke na početku igre
class HintPopup(Popup):
    def __init__(self, screen):
        super().__init__(screen, "", 0.4, 0.1)
        self.text = "Ako želite vidjeti postavke i kontrole pritisnite Esc!"
        self.visible = True
        self.start_time = pg.time.get_ticks()
        self.duration = 5000

    def draw(self):
        if not self.visible:
            return

        if pg.time.get_ticks() - self.start_time > self.duration:
            self.visible = False
            return

        
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_width = text_surface.get_width() + 100  
        text_height = text_surface.get_height() + 20

       
        self.rect.width = text_width
        self.rect.height = text_height
        self.rect.topleft = (20, self.screen.get_height() // 10)

        
        pg.draw.rect(self.screen, (50, 50, 50), self.rect, border_radius=10)
        pg.draw.rect(self.screen, (200, 200, 200), self.rect, 2, border_radius=10)
        text_rect = text_surface.get_rect(midleft=(self.rect.left + 10, self.rect.centery))
        self.screen.blit(text_surface, text_rect)

class HelpPopup(Popup):
    def __init__(self, screen):
        super().__init__(screen, "Help", 0.6, 0.6)
        
        self.text = [
            ("Esc", "Zatvaranje Help popupa"),
            ("W", "Kretanje naprijed"),
            ("A", "Kretanje lijevo"),
            ("S", "Kretanje natrag"),
            ("D", "Kretanje desno"),
            ("E", "Interakcija s objektima"),
            ("Tab", "Otvaranje inventorija"),
            ("↑", "Bacanje blata"),
            ("←", "Okretanje kamere lijevo"),
            ("→", "Okretanje kamere desno")
        ]
        self.visible = False  

    def draw(self):
        if not self.visible:
            return
        super().draw()

        
        start_y = self.rect.top + 120  
        line_height = 40  

        for i, (key, action) in enumerate(self.text):
            key_text = f"Tipka '{key}'"
            key_surface = self.font.render(key_text, True, (255, 255, 255))
            action_surface = self.font.render(f" - {action}", True, (255, 255, 255))

            key_x = self.rect.left + 50  
            action_x = self.rect.left + 250  
            y_position = start_y + i * line_height  

            self.screen.blit(key_surface, (key_x, y_position))
            self.screen.blit(action_surface, (action_x, y_position))

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

class IvanNPC(Popup):
    def __init__(self, screen):
        super().__init__(screen, "Majstor Ivan", 0.6, 0.2)  
        
        self.text = (
            "Dobro došao! Prije nego kreneš u pustolovinu, "
            "moraš popraviti svoju torbu. Imaš u chestu "
            "neke iteme koji će ti pomoći. Sretno!"
        )
        self.rect.bottom = self.screen.get_height() - 50
        self.rect.left = (self.screen.get_width() - self.rect.width) // 2

    def draw(self):
        if not self.visible:
            return
        pg.draw.rect(self.screen, (50, 50, 50), self.rect, border_radius=10)
        pg.draw.rect(self.screen, (200, 200, 200), self.rect, 2, border_radius=10)

        title_surface = self.font.render("Majstor Ivan", True, (255, 255, 255))
        title_x = self.rect.left + 10
        title_y = self.rect.top + 10
        self.screen.blit(title_surface, (title_x, title_y))
        
        wrapped_text = self.wrap_text(self.text, self.font, self.rect.width - 20)
        start_y = self.rect.top + 40
        line_height = 25  

        for i, line in enumerate(wrapped_text):
            text_surface = self.font.render(line, True, (255, 255, 255))
            text_x = self.rect.left + 10  
            y_position = start_y + i * line_height  
            self.screen.blit(text_surface, (text_x, y_position))

    def wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""
        
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        return lines
