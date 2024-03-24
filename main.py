import pygame,sys
import time
pygame.init()

largura_janela, altura_janela = 1280,720
janela = pygame.display.set_mode((largura_janela,altura_janela))
fonte = pygame.font.Font(None, 36) 
fonte_nome = pygame.font.Font(None,100)

menu_selection = pygame.mixer.Sound('menu_selection.wav')
cursor_select = pygame.mixer.Sound("cursor_select.wav")
cursor_back = pygame.mixer.Sound("cursor_back.wav")

coletou = pygame.mixer.Sound("coletado.ogg")


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





velocidade = 10

paredes_fase1 = [
    pygame.Rect(10, 40, 20, 600),
    pygame.Rect(10, 40, 800, 20),

    pygame.Rect(0, 615, 800, 20),
    pygame.Rect(780, 40, 20, 600),


]

paredes_fase2 = [
    pygame.Rect(10, 40, 20, 600),
    pygame.Rect(10, 40, 800, 20),

    pygame.Rect(400,80,40,500),

    pygame.Rect(0, 615, 800, 20),
    pygame.Rect(780, 40, 20, 600),


]

def desenhar_paredes(paredes):
        
        for parede in paredes:
            pygame.draw.rect(janela, (0,0,0), parede)







def menu():

    opcoes = [0,1,2]
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
                if event.key == pygame.K_SPACE and indice == 2:
                    cursor_select.play()
                    tchau()
                if event.key == pygame.K_s:
                    menu_selection.play()
                    indice = indice +1
                    if indice>=len(opcoes):
                        indice = 0
                if event.key == pygame.K_w:
                    menu_selection.play()
                    indice = indice - 1
                    if indice <0:
                        indice = len(opcoes)-1

        start = fonte.render("Start",True,preto)
        config = fonte.render("configuraçoes",True,preto)
        sair = fonte.render("Sair",True,preto)

        nome = fonte_nome.render("Game OOP",True,preto)
        nome_rect = nome.get_rect(center=(largura_janela/2,altura_janela/2 - 200))
        janela.blit(nome,nome_rect)

                    
        if indice == 0:
            start = fonte.render("Start",True,azul)
        if indice == 1:
            config = fonte.render("configuraçoes",True,azul)
        if indice == 2:
            sair = fonte.render("Sair",True,azul)



        config_rect = config.get_rect(center= (largura_janela/2,(altura_janela/2)+40) )
        start_rect = start.get_rect(center=(largura_janela/2,altura_janela/2))
        
        sair_rect = sair.get_rect(center= (largura_janela/2,(altura_janela/2)+80))
        janela.blit(start,start_rect)
        janela.blit(config,config_rect)
        janela.blit(sair,sair_rect)

        

        pygame.display.update()



def tchau():
    
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
                if event.key == pygame.K_SPACE and indice == 1:
                    cursor_back.play()
                    menu()
                if event.key == pygame.K_SPACE and indice == 0:
                    cursor_select.play()
                    time.sleep(1)
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_s:
                    menu_selection.play()
                    indice = indice +1
                    if indice>=len(opcoes):
                        indice = 0
                if event.key == pygame.K_w:
                    menu_selection.play()
                    indice = indice - 1
                    if indice <0:
                        indice = len(opcoes)-1

        sim = fonte.render("Sim",True,preto)
        nao = fonte.render("Não",True,preto)
        

        nome = fonte_nome.render("Tem certeza que quer sair?",True,preto)
        nome_rect = nome.get_rect(center=(largura_janela/2,altura_janela/2 - 200))
        janela.blit(nome,nome_rect)

                    
        if indice == 0:
            sim = fonte.render("Sim",True,azul)
        if indice == 1:
            nao = fonte.render("Não",True,azul)
        



        sim_rect = sim.get_rect(center= (largura_janela/2,(altura_janela/2)+40) )
        nao_rect = nao.get_rect(center=(largura_janela/2,altura_janela/2))
        
      
        janela.blit(sim,sim_rect)
        janela.blit(nao,nao_rect)
        

        

        pygame.display.update()



def fase1():
    bloco = Bloco(60,100, id=1)
    bloco.colisao = False
    x_textos = largura_janela-300
    qt_coletados = 0
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
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx = -velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx = velocidade
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy = -velocidade
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy = velocidade


        if teclas[pygame.K_t]:
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
                qt_coletados+=1
                fase2()
                


        colisao_texto = fonte.render(f"Colisao:{bloco.colisao} ",True,(0,0,0))
        tamanho_texto = fonte.render(f"Tamanho:{bloco.tamanho} ",True,(0,0,0))
        coletados = fonte.render(f"coletados:{qt_coletados}/{1}",True,(0,0,0))
        id_texto = fonte.render(f"Id:{bloco.id} ",True,(0,0,0))

        janela.blit(colisao_texto,(x_textos,60))
        janela.blit(tamanho_texto,(x_textos,100))
        janela.blit(id_texto,(x_textos,140))
        janela.blit(coletados,(x_textos,180))

        pygame.display.update()





def fase2():
    bloco = Bloco(50,200, id=1)
    bloco.colisao = True
    qt_coletados =0

    item1 = Bloco(500,200,cor="green")
    item2 = Bloco(50,400,cor="green")
    

    itens = [item1,item2]

    while True:
        janela.fill((255,255,255))

        desenhar_paredes(paredes_fase2)

        t = pygame.Rect(400,80,40,500)
        f = pygame.draw.rect(janela,(0,0,0),t)

        for item in itens:
            item.place()

        
        


        clock.tick(60)
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        
        bloco.place()

        # Movimento do quadrado principal
        teclas = pygame.key.get_pressed()
        dx, dy = 0, 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            dx = -velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            dx = velocidade
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            dy = -velocidade
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            dy = velocidade
        

        

        bloco.dx = dx
        bloco.dy = dy
        
    

        if bloco.colisao == True:
          
            
            if bloco.place().colliderect(f):
                print("Oi")
            else:
                bloco.x +=dx
                bloco.y +=dy


        for item in range(len(itens)):
            if bloco.place().colliderect(itens[item].place()):
                coletou.play()
                itens.pop()
                qt_coletados+=1
            


   


        colisao_texto = fonte.render(f"Colisao:{bloco.colisao} ",True,(0,0,0))
        tamanho_texto = fonte.render(f"Tamanho:{bloco.tamanho} ",True,(0,0,0))
        id_texto = fonte.render(f"Id:{bloco.id} ",True,(0,0,0))
        coletados = fonte.render(f"coletados:{qt_coletados}/{2}",True,(0,0,0))

        janela.blit(colisao_texto,(largura_janela-200,60))
        janela.blit(tamanho_texto,(largura_janela-200,100))
        janela.blit(id_texto,(largura_janela-200,140))
        janela.blit(coletados,(largura_janela-200,180))

        pygame.display.update()

    


menu()
