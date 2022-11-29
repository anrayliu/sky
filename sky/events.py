import pygame


class Events:
    def __init__(self):
        self.update()
        
    def update(self):
        self.quit = False
        self.click = False
        self.input = None
        self.input_name = None
        self.input_const = None
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.click = True
            elif event.type == pygame.KEYDOWN:
                self.input = event.unicode
                self.input_name = pygame.key.name(event.key)
                self.input_const = event.key
                
        self.keys_pressed = pygame.key.get_pressed()
        self.mouse_pressed = pygame.mouse.get_pressed()
        self.mouse = self.x, self.y = pygame.mouse.get_pos()