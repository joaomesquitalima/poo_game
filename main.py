import pygame,sys

pygame.init()

largura_janela, altura_janela = 1280,720
janela = pygame.display.set_mode((largura_janela,altura_janela))
fonte = pygame.font.Font(None, 36) 
fonte_nome = pygame.font.Font(None,100)



class Bloco():
    def __init__(self,x,y,colisao=False,tamanho= 50,cor = "blue",dx=0,dy=0,id=0):
        self.colisao = colisao
        self.tamanho = tamanho
        self.cor = cor
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.id = id

    def place(self):
        
        return pygame.draw.rect(janela, self.cor, (self.x +self.dx, self.y+self.dy, self.tamanho, self.tamanho))



clock = pygame.time.Clock()


x =50
y = 200
bloco = Bloco(x,y, id=1)

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


def menu():

    opcoes = [0,1]
    indice = 0
    azul = (0,0,255)
    preto = (0,0,0)
    while True:
        janela.fill((255,255,255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and indice == 0:
                    fase1()
                if event.key == pygame.K_s:
                    indice = indice +1
                    if indice>=len(opcoes):
                        indice = 0
                if event.key == pygame.K_w:
                    indice = indice - 1
                    if indice <0:
                        indice = len(opcoes)-1

        start = fonte.render("Start",True,preto)
        config = fonte.render("configuraçoes",True,preto)

        nome = fonte_nome.render("Game OOP",True,preto)
        nome_rect = nome.get_rect(center=(largura_janela/2,altura_janela/2 - 200))
        janela.blit(nome,nome_rect)

                    
        if indice == 0:
            start = fonte.render("Start",True,azul)
        if indice == 1:
            config = fonte.render("configuraçoes",True,azul)



        config_rect = config.get_rect(center=(largura_janela/2,(altura_janela/2)+40))
        start_rect = start.get_rect(center=(largura_janela/2,altura_janela/2))
        janela.blit(start,start_rect)
        janela.blit(config,config_rect)

        

        pygame.display.update()


def fase1():
    bloco.colisao = False
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
                fase2()
                


        colisao_texto = fonte.render(f"Colisao:{bloco.colisao} ",True,(0,0,0))
        tamanho_texto = fonte.render(f"Tamanho:{bloco.tamanho} ",True,(0,0,0))
        id_texto = fonte.render(f"Id:{bloco.id} ",True,(0,0,0))

        janela.blit(colisao_texto,(largura_janela-200,60))
        janela.blit(tamanho_texto,(largura_janela-200,100))
        janela.blit(id_texto,(largura_janela-200,140))

        pygame.display.update()





def fase2():
    bloco = Bloco(x,y, id=1)
    bloco.colisao = False
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
        id_texto = fonte.render(f"Id:{bloco.id} ",True,(0,0,0))

        janela.blit(colisao_texto,(largura_janela-200,60))
        janela.blit(tamanho_texto,(largura_janela-200,100))
        janela.blit(id_texto,(largura_janela-200,140))

        pygame.display.update()

    


menu()