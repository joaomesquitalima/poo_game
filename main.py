import pygame,sys

pygame.init()

largura_janela, altura_janela = 1280,720
janela = pygame.display.set_mode((largura_janela,altura_janela))
fonte = pygame.font.Font(None, 36) 



class Bloco():
    def __init__(self,x,y,colisao=False,tamanho= 50,cor = "blue",dx=0,dy=0):
        self.colisao = colisao
        self.tamanho = tamanho
        self.cor = cor
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def place(self):
        
        return pygame.draw.rect(janela, self.cor, (self.x +self.dx, self.y+self.dy, self.tamanho, self.tamanho))



clock = pygame.time.Clock()


x = 10
y = 200
bloco = Bloco(x,y)

velocidade = 10

paredes_fase1 = [
    pygame.Rect(10, 40, 20, 600),
    pygame.Rect(10, 40, 800, 20),

    pygame.Rect(0, 615, 800, 20),
    pygame.Rect(780, 40, 20, 600),



    
]

def desenhar_paredes(paredes):
        
        for parede in paredes:
            pygame.draw.rect(janela, (0,0,0), parede)
def fase1():
    while True:
        janela.fill((255,255,255))

        desenhar_paredes(paredes_fase1)

        


        clock.tick(60)
       
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

        q = Bloco(500,200,cor="green")
        q.place()

        bloco.dx = dx
        bloco.dy = dy
        
    

        if bloco.colisao == False:
            bloco.x +=dx
            bloco.y +=dy

            if bloco.place().colliderect(q.place()):
                pass
        else:
            if not bloco.place().colliderect(q.place()):
                bloco.x +=dx
                bloco.y +=dy
            else:
                break
                


        colisao_texto = fonte.render(f"Colisao:{bloco.colisao} ",True,(0,0,0))
        tamanho_texto = fonte.render(f"Tamanho:{bloco.tamanho} ",True,(0,0,0))

        janela.blit(colisao_texto,(largura_janela-200,60))
        janela.blit(tamanho_texto,(largura_janela-200,100))

        pygame.display.update()


fase1()