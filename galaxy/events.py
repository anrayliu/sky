import pygame


class Events:
    def __init__(self, custom=None):
        self.custom = custom
        self.update()
        
    def update(self):
        self.quit = False
        self.click = False
        self.input = None
        if self.custom != None:
            self.custom.reset()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.click = True
            elif event.type == pygame.KEYDOWN:
                self.input = pygame.key.name(event.key)

            if self.custom != None:
                self.custom.update(event)
                
        self.keys_held = pygame.key.get_pressed()
        self.mouse_held = pygame.mouse.get_pressed()
        self.mouse = self.x, self.y = pygame.mouse.get_pos()