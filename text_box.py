import pygame 


class TextBox:
    def __init__(self, rect, style={}, center=None, filter=None):
        self.style = {"colour": "white",
                      "border colour": "black",
                      "border size": 0,
                      "font": "arial",
                      "font size": 30,
                      "font colour": "black",
                      "cursor colour": "black",
                      "cursor speed":0.05,
                      "cursor width":3,
                      "backspace timer":40,
                      "click unselect":True}

        self.style.update(style)
                
        self.rect = pygame.Rect(rect)
        if not center is None:
            self.rect.center = pygame.Rect(*center).center
        
        self.text = ""
        
        self.selected = False

        self.cursor_timer = 0
        self.backspace_timer = 0

        self.filter = filter

    def update(self, events):
        if self.rect.collidepoint(events.mouse):
            if events.click:
                self.selected = not self.selected
                self.cursor_timer = 0
        elif self.style["click unselect"] and events.mouse_pressed[0]:
            self.selected = False

        if self.selected:
            if events.keys_pressed[pygame.K_BACKSPACE]:
                if self.backspace_timer == self.style["backspace timer"]:
                    self.text = self.text[:-1]
                else:
                    self.backspace_timer += 1
            else:
                self.backspace_timer = 0

            if events.input is not None:
                if events.input_name == "backspace":
                    self.text = self.text[:-1]
                elif events.input_name == "return":
                    self.selected = False
                else:
                    if self.filter is None:
                        self.text += events.input
                    else:
                        self.text += self.filter(events)

        self.cursor_timer += self.style["cursor speed"]
        
    def draw(self, graphics):
        pygame.draw.rect(graphics.surface, self.style["colour"], self.rect)
        if self.style["border size"] > 0:
            pygame.draw.rect(graphics.surface, self.style["border colour"], self.rect, self.style["border size"])
            
        rect = graphics.write(self.text, (0, 0), font=self.style["font"], size=self.style["font size"], colour=self.style["font colour"], center=self.rect)

        if self.selected and int(self.cursor_timer) % 2 == 0:
            pygame.draw.rect(graphics.surface, self.style["cursor colour"], (rect[0] + rect[2], rect[1], self.style["cursor width"], rect[3]))