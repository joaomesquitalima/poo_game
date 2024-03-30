import pygame




class Boss(pygame.sprite.Sprite):
    def __init__(self,pos_x,pos_y,life):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load("frames_output/frame_000.png").convert_alpha())
        self.sprites.append(pygame.image.load("frames_output/frame_001.png").convert_alpha())
        self.sprites.append(pygame.image.load("frames_output/frame_002.png").convert_alpha())
        self.sprites.append(pygame.image.load("frames_output/frame_003.png").convert_alpha())
        self.image_atual = 0
        self.image= self.sprites[self.image_atual]
        self.life = life
        self.bullet = pygame.image.load("boss_bullet.png").convert_alpha()
        self.lista_bullet = []
        
        self.rect = self.image.get_rect(center = (pos_x,pos_y))
        

        self.opacidade = 0
        

    def update(self,janela,x):
        self.image_atual+=0.14
        
        if self.image_atual >= len(self.sprites):
            self.image_atual = 0

        self.image = self.sprites[int(self.image_atual)]
        self.imge = pygame.transform.scale(self.image,(64,64))
        # imagem_opaca = self.image.copy()
        # imagem_opaca.fill((255, 255, 255, 60), None, pygame.BLEND_RGBA_MULT)
        # self.image = imagem_opaca
        self.opacidade+=0.4
        # print(self.opacidade)
        print(self.life)

        for bala in self.lista_bullet:
            bala.y += 10
            


            if bala.y > 600:
                self.lista_bullet.remove(bala)
            janela.blit(self.bullet,bala)

        


    def ai(self):
        imagem_opaca = self.image.copy()
        if self.opacidade >= 220:
            self.opacidade = 220
        imagem_opaca.fill((255, 255, 255, self.opacidade), None, pygame.BLEND_RGBA_MULT)
        self.image = imagem_opaca

    def atack(self,x):
        if (x+65) >= 810:
            self.rect.x = x -70
            bullet = self.bullet.get_rect(center=(self.rect.x + 150 ,self.rect.y))
        elif (x+65) <= 400:
            self.rect.x = x + 70
            bullet = self.bullet.get_rect(center=(self.rect.x + 20,self.rect.y))
            

        else:
            self.rect.x = x
        
            bullet = self.bullet.get_rect(center=(self.rect.x + 100,self.rect.y))

        self.lista_bullet.append(bullet)

        



        

        

    

