import pygame




class Boss(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load("frames_output/frame_000.png"))
        self.sprites.append(pygame.image.load("frames_output/frame_001.png"))
        self.sprites.append(pygame.image.load("frames_output/frame_002.png"))
        self.sprites.append(pygame.image.load("frames_output/frame_003.png"))
        self.image_atual = 0
        self.image= self.sprites[self.image_atual]
        
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x,pos_y]

    def update(self):
        self.image_atual+=0.14

        if self.image_atual >= len(self.sprites):
            self.image_atual = 0

        self.image = self.sprites[int(self.image_atual)]
        

    

