import pygame


class Events:
    def __init__(self):
        self.update()
        
    def update(self):
        self.quit = False
        self.click = False
        self.input = None
        self.input_name = None
        self.right_click = False
        self.resize = False 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True
                elif event.button == 3:
                    self.right_click = True
            elif event.type == pygame.KEYDOWN:
                self.input = event.unicode
                self.input_name = pygame.key.name(event.key)
            elif event.type == pygame.VIDEORESIZE:
                self.resize = True
                
        self.keys_pressed = pygame.key.get_pressed()
        self.mouse_pressed = pygame.mouse.get_pressed()
        self.mouse = self.x, self.y = pygame.mouse.get_pos()