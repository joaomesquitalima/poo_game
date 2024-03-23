import pygame,sys

pygame.init()

largura_janela, altura_janela = 1280,720
janela = pygame.display.set_mode((largura_janela,altura_janela))


class Bloco():
    def __init__(self,x,y,colisao=False,tamanho= 50,cor = "blue"):
        self.colisao = colisao
        self.tamanho = tamanho
        self.cor = cor
        self.x = x
        self.y = y

    def place(self):
        
        return pygame.draw.rect(janela, self.cor, (self.x, self.y, self.tamanho, self.tamanho))



clock = pygame.time.Clock()


x = 10
y = 10
bloco = Bloco(x,y)

velocidade = 2

while True:

    clock.tick(60)
    janela.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    
    
    bloco.place()

    # Movimento do quadrado principal
    teclas = pygame.key.get_pressed()
    dx, dy = 0, 0
    if teclas[pygame.K_LEFT]:
        dx = -velocidade
    if teclas[pygame.K_RIGHT]:
        dx = velocidade
    if teclas[pygame.K_UP]:
        dy = -velocidade
    if teclas[pygame.K_DOWN]:
        dy = velocidade

    q = Bloco(500,10,cor="green")
    if q.place().colliderect(bloco.place()):
        bloco.x -=2
    else:
        bloco.x +=dx




    




    # # Verificar teclas pressionadas
    # teclas = pygame.key.get_pressed()
    # if teclas[pygame.K_LEFT]:
    #     x_personagem -= velocidade
    # if teclas[pygame.K_RIGHT]:
    #     x_personagem += velocidade
    # if teclas[pygame.K_UP]:
    #     y_personagem -= velocidade
    # if teclas[pygame.K_DOWN]:
    #     y_personagem += velocidade


    


    pygame.display.update()