import pygame
# import sys

# # Inicialize o Pygame
# pygame.init()

# # Defina o tamanho da janela
# largura_janela = 800
# altura_janela = 600

# # Crie a janela
# janela = pygame.display.set_mode((largura_janela, altura_janela))

# # Defina o título da janela
# pygame.display.set_caption("Janela Vazia")


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
        

        

# moving_sprites = pygame.sprite.Group()
# boss = Boss(100,100)

# moving_sprites.add(boss)


# clock = pygame.time.Clock()
# while True:
#     clock.tick(60)
#     janela.fill((255,255,255))
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

   


#     # Atualize a 
#     moving_sprites.draw(janela)
#     moving_sprites.update()
#     pygame.display.update()
