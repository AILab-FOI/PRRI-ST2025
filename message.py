
from settings import *
import textwrap
from itertools import chain

class Message:
    def __init__(self, app, alpha=156, border_radius=10, border_color=(150, 150, 150)):
        self.app = app
        self.alpha = alpha
        self.x, self.y = self.app.screen.get_size()
        self.y //= 2
        self.border = 10
        self.border_radius = border_radius
        self.border_color = border_color
        self.overlay_surface = pg.Surface((self.x - 2 * self.border, self.y - 2 * self.border), pg.SRCALPHA)
        self.overlay_surface.fill((0, 0, 0, self.alpha))
        self.inner_border = 20  
        self.inner_surface = self.empty_surface()
        #self.overlay_surface.fill((0, 0, 0, 255))
        self.active = False
        self.shown = False
        self.font = pg.font.Font("assets/PressStart2P-Regular.ttf", 39)
        
        self.set_message( self.message )
        self.text_index = 0
        self.max_lines = 0
        self.line_height = self.font.get_height()
        self.max_lines = self.inner_surface.get_height() // self.line_height

    def empty_surface( self ):
        s = pg.Surface(
            (
                self.overlay_surface.get_width() - 2 * self.inner_border,
                self.overlay_surface.get_height() - 2 * self.inner_border
            ),
            pg.SRCALPHA
        )
        s.fill((0, 0, 0, 0))  
        return s
        
    def draw_border(self):
        border_rect = pg.Rect(0, 0, self.x - 2 * self.border, self.y - 2 * self.border)
        pg.draw.rect(self.overlay_surface, self.border_color, border_rect, border_radius=self.border_radius, width=10)

    def set_message( self, msg ):
        self.message = msg
        t = [ textwrap.wrap( m, width=39 ) for m in self.message.split( '\n' ) ]
        self.wrapped_text = list( chain( *t ) )  
        
    def draw_message(self):
        self.show_text = self.wrapped_text[self.text_index:self.text_index + self.max_lines]

        if not self.show_text:
            self.active = False
            self.text_index = 0
            return

        self.shown = True
        
        self.overlay_surface.fill((0, 0, 0, self.alpha))
        self.inner_surface = self.empty_surface()

        for i, line in enumerate(self.show_text):
            text = self.font.render(line, True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.top = i * self.line_height
            self.inner_surface.blit(text, text_rect)

        self.overlay_surface.blit(self.inner_surface, (self.inner_border, self.inner_border))

    def draw(self):
        if self.active:
            self.draw_border()
            self.draw_message()
            self.app.screen.blit(self.overlay_surface, (self.border, self.y + self.border))
        else:
            if 'CREDITS' in ''.join( self.wrapped_text ) and self.shown:
                if __import__("sys").platform != "emscripten":
                    print( CREDITS )
                    pg.quit()
                    sys.exit()

    def handle_input(self):
        if self.text_index < len(self.wrapped_text):
            self.text_index += self.max_lines
        else:
            self.text_index = 0
            self.active = False
