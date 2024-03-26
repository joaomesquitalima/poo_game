import pygame
import sys

# Defina as cores
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)


class Fase:
    def __init__(self, janela):
        self.janela = janela
        self.clock = pygame.time.Clock()

    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def atualizar(self):
        pass

    def desenhar(self):
        print("fase 1")

class Fase1(Fase):
    def __init__(self, janela):
        # super().__init__(janela)
        pass

    def processar_eventos(self):
        # super().processar_eventos()
        # Lógica específica da Fase 1
        pass

    def atualizar(self):
        # Lógica de atualização específica da Fase 1
        pass

    def desenhar(self):
        # Desenhar elementos específicos da Fase 1 na tela
        print("fase 2")

class Menu:
    def __init__(self, janela):
        self.janela = janela
        self.clock = pygame.time.Clock()
        self.fundo = pygame.image.load("tela_pico8_preta.png")
        self.fundo = pygame.transform.scale(self.fundo, (1280, 720))
        pygame.mixer.music.load('musica/menu.mp3')
        self.largura_janela = 1280
        self.altura_janela = 720

        # Defina o volume (opcional)
        pygame.mixer.music.set_volume(0.5)  # Valor varia de 0.0 a 1.0

        # Reproduza a música em loop infinito (-1 significa loop infinito)
        pygame.mixer.music.play(-1)

        self.opcoes = [0,1,2]
        self.indice = 0
        self.azul = (0,0,255)
        self.preto = (255,255,255)

        self.fonte = pygame.font.Font("ThaleahFat.ttf", 50) 
        self.fonte_nome = pygame.font.Font("ThaleahFat.ttf",100)

        self.fonte_outros = pygame.font.Font("ThaleahFat.ttf",45)

      

    def processar_eventos(self):
        print(self.indice)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.indice == 0:
                    jogo.fase_atual = Fase(self.janela)
                if event.key == pygame.K_SPACE and self.indice == 2:
                    # cursor_select.play()
                    # tchau()
                    pass
                if event.key == pygame.K_s:
                    
                    self.indice = self.indice +1
                    if self.indice>=len(self.opcoes):
                        self.indice = 0
                if event.key == pygame.K_w:
                    
                    self.indice = self.indice - 1
                    if self.indice <0:
                        self.indice = len(self.opcoes)-1

    def atualizar(self):
        pygame.display.update()

    def desenhar(self):
        self.janela.fill((255,255,255))
        self.janela.blit(self.fundo,(0,0))

        nome = self.fonte_nome.render("Game OOP",True,self.preto)
        nome_rect = nome.get_rect(center=(1280/2,720/2 - 200))

        start = self.fonte.render("Start",True,self.preto)
        config = self.fonte.render("conquistas",True,self.preto)
        sair = self.fonte.render("Sair",True,self.preto)

        if self.indice == 0:
            start = self.fonte.render("Start",True,self.azul)
        elif self.indice == 1:
            config = self.fonte.render("conquistas",True,self.azul)
        elif self.indice == 2:
            sair = self.fonte.render("Sair",True,self.azul)

        
        self.janela.blit(nome,nome_rect)
        config_rect = config.get_rect(center= (self.largura_janela/2,(self.altura_janela/2)+40) )
        start_rect = start.get_rect(center=(self.largura_janela/2,self.altura_janela/2))
        
        sair_rect = sair.get_rect(center= (self.largura_janela/2,(self.altura_janela/2)+80))
        self.janela.blit(start,start_rect)
        self.janela.blit(config,config_rect)
        self.janela.blit(sair,sair_rect)

class Jogo:
    def __init__(self):
        pygame.init()
        self.largura_janela = 1280
        self.altura_janela = 720
        self.janela = pygame.display.set_mode((self.largura_janela, self.altura_janela))
        pygame.display.set_caption('Meu Jogo com Pygame')
        self.clock = pygame.time.Clock()
        self.menu = Menu(self.janela)
        self.fase_atual = None  # Começar sem fase

    def executar(self):
        rodando = True
        while rodando:
            if self.fase_atual is None:
                self.menu.processar_eventos()
                self.menu.atualizar()
                self.menu.desenhar()
            else:
                self.fase_atual.processar_eventos()
                self.fase_atual.atualizar()
                self.fase_atual.desenhar()
            pygame.display.flip()
            self.clock.tick(60)  # Limita a taxa de quadros a 60 FPS

if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()
