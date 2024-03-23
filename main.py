import pygame,sys

pygame.init()

largura_janela, altura_janela = 1280,720
janela = pygame.display.set_mode((largura_janela,altura_janela))
fonte = pygame.font.Font(None, 36) 



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


    if teclas[pygame.K_a]:
        bloco.colisao = True

    q = Bloco(500,10,cor="green")
    q.place()
    bloco.x +=dx
    bloco.y +=dy


    if bloco.colisao == False:
        pass
    else:
        if q.place().colliderect(bloco.place()):
            dy = 0
        else:
            bloco.x +=dx

    colisao_texto = fonte.render(f"Colisao:{bloco.colisao} ",True,(0,0,0))
    tamanho_texto = fonte.render(f"Tamanho:{bloco.tamanho} ",True,(0,0,0))

    janela.blit(colisao_texto,(largura_janela-200,60))
    janela.blit(tamanho_texto,(largura_janela-200,100))

    pygame.display.update()