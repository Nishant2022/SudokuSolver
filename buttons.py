import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

class Button():
    def __init__(self, surface, color, hover, rect, font):
        self.surface = surface
        self.color = color
        self.hover_color = hover
        self.rect = rect
        self.is_hovering = False
        self.font = font
    
    def hover(self, val):
        x, y = val
        if self.rect[0] < x < self.rect[0] + self.rect[2]:
            if self.rect[1] < y < self.rect[1] + self.rect[3]:
                self.is_hovering = True
            else:
                self.is_hovering = False
        else:
            self.is_hovering = False        

    def draw(self):
        if self.is_hovering:
            pygame.draw.rect(self.surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(self.surface, self.color, self.rect)
        font_surface = self.font.render(self.value if self.value != '0' else ' ', True, (0,0,0))
        font_rect = font_surface.get_rect(center = (self.rect[0] + 41, self.rect[1] + 41))
        self.surface.blit(font_surface, font_rect)
    
    def update(self):
        val = pygame.mouse.get_pos()
        self.hover(val)
    
    def change_value(self, value):
        self.value = value

class ToggleButton(Button):
    def __init__(self, surface, color, hover, rect, font, pencil_font):
        super(ToggleButton, self).__init__(surface, color, hover, rect, font)
        self.clicked = False
        self.coords = (0,0)
        self.incorrect = False
        self.pencil_font = pencil_font
        self.pencil_values = set()
        self.constant = False
        
    def draw(self):
        if self.constant:
            pygame.draw.rect(self.surface, (220, 220, 220), self.rect)
        elif self.is_hovering:
            pygame.draw.rect(self.surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(self.surface, self.color, self.rect)
        if self.clicked:
            pygame.draw.rect(self.surface, (255, 255, 0), self.rect)
        if self.incorrect:
            pygame.draw.rect(self.surface, (255, 0, 0), self.rect)
        font_surface = self.font.render(self.value if self.value != '0' else ' ', True, (0,0,0))
        if len(self.pencil_values) != 0:
            self.draw_pencil()
        font_rect = font_surface.get_rect(center = (self.rect[0] + 41, self.rect[1] + 41))
        self.surface.blit(font_surface, font_rect)

    def draw_pencil(self):
        for i in range(3):
            output = ''
            for j in range(3):
                if i * 3 + j + 1 in self.pencil_values:
                    output += str(i * 3 + j + 1) + ' '
                else:
                    output += '  '
            output = output[:-1]
            font_surface = self.pencil_font.render(output, True, (100, 100, 100))
            font_rect = font_surface.get_rect(center = (self.rect[0] + 41, self.rect[1] + 10 + 30 * i))
            self.surface.blit(font_surface, font_rect)

    def update(self):
        val = pygame.mouse.get_pos()
        x,y = val
        if pygame.mouse.get_pressed()[0]:
            if self.rect[0] < x < self.rect[0] + self.rect[2]:
                if self.rect[1] < y < self.rect[1] + self.rect[3]:
                    self.clicked = True
                else:
                    self.clicked = False
            else:
                self.clicked = False
        self.hover(val)

    def change_value(self, value):
        super().change_value(value)
        if self.incorrect:
            self.incorrect = False
    
    def pencil_value(self, values):
        self.pencil_values = values