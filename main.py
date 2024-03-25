import pygame,sys
import time
pygame.init()



# Inicialize os dispositivos de joystick
pygame.joystick.init()

# Verifique se há pelo menos um joystick conectado
if pygame.joystick.get_count() == 0:
    print("Nenhum joystick encontrado. Certifique-se de que um controle de PS4 está conectado.")
else:

    # Configure o primeiro joystick (controle de PS4)
    controle_ps4 = pygame.joystick.Joystick(0)
    controle_ps4.init()





largura_janela, altura_janela = 1280,720
janela = pygame.display.set_mode((largura_janela,altura_janela))
fonte = pygame.font.Font("ThaleahFat.ttf", 50) 
fonte_nome = pygame.font.Font("ThaleahFat.ttf",100)

fonte_outros = pygame.font.Font("ThaleahFat.ttf",45)

fundo = pygame.image.load("tela_pico8_preta.png")
fundo = pygame.transform.scale(fundo, (largura_janela, altura_janela))


menu_selection = pygame.mixer.Sound('audios/menu_selection.wav')
cursor_select = pygame.mixer.Sound("audios/cursor_select.wav")
cursor_back = pygame.mixer.Sound("audios/cursor_back.wav")
mudar = pygame.mixer.Sound("audios/open_001.ogg")
coletou = pygame.mixer.Sound("audios/coletado.ogg")
click = pygame.mixer.Sound("audios/click.2.ogg")

player = pygame.image.load("imagens/robo1.png").convert_alpha()




botao_up = pygame.image.load("imagens/botao_up.png").convert_alpha()
botao_up_rect = botao_up.get_rect(center=(200,400))

botao_down = pygame.image.load("imagens/botao_down.png").convert_alpha()
botao_down_rect = botao_up.get_rect(center=(200,400))


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

    

    pygame.Rect(0, 615, 800, 20),
    pygame.Rect(780, 40, 20, 600),


]

paredes_fase3 = [

    pygame.Rect(10, 40, 20, 600),
    pygame.Rect(10, 40, 800, 20),

    pygame.Rect(400,80,40,500),

    pygame.Rect(0, 615, 800, 20),
    pygame.Rect(780, 40, 20, 600),



]

def desenhar_paredes(paredes):
        
        for parede in paredes:
            pygame.draw.rect(janela, (255,255,255), parede)







def menu():
        # Carregue a música
    pygame.mixer.music.load('musica/menu.mp3')

    # Defina o volume (opcional)
    pygame.mixer.music.set_volume(0.5)  # Valor varia de 0.0 a 1.0

    # Reproduza a música em loop infinito (-1 significa loop infinito)
    pygame.mixer.music.play(-1)


    opcoes = [0,1,2]
    indice = 0
    azul = (0,0,255)
    preto = (255,255,255)
    while True:
        janela.fill((255,255,255))
        janela.blit(fundo,(0,0))

        if pygame.joystick.get_count() == 0:
            pass
        else:

            botao_x = controle_ps4.get_button(0)  # Verifica se o botão X (índice 2) está pressionado
            eixo_direcional_x = controle_ps4.get_axis(0)  # Eixo esquerdo horizontal
            eixo_direcional_y = controle_ps4.get_axis(1)  # Eixo esquerdo vertical
            up = controle_ps4.get_button(11)
            # print(up)

            if botao_x and indice == 0:
                fase1()

            if up:
                menu_selection.play()
                indice-=1
                if indice <0:
                    indice = len(opcoes)-1
            


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
        config = fonte.render("conquistas",True,preto)
        sair = fonte.render("Sair",True,preto)

        nome = fonte_nome.render("Game OOP",True,preto)
        nome_rect = nome.get_rect(center=(largura_janela/2,altura_janela/2 - 200))
        janela.blit(nome,nome_rect)

                    
        if indice == 0:
            start = fonte.render("Start",True,azul)
        if indice == 1:
            config = fonte.render("conquistas",True,azul)
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
    preto = (255,255,255)
    while True:
        janela.fill((255,255,255))
        janela.blit(fundo,(0,0))

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
        nao = fonte.render("Nao",True,preto)
        

        nome = fonte_outros.render("Tem certeza que quer sair?",True,preto)
        nome_rect = nome.get_rect(center=(largura_janela/2,altura_janela/2 - 100))
        janela.blit(nome,nome_rect)

                    
        if indice == 0:
            sim = fonte.render("Sim",True,azul)
        if indice == 1:
            nao = fonte.render("Nao",True,azul)
        



        sim_rect = sim.get_rect(center= (largura_janela/2,(altura_janela/2)+40) )
        nao_rect = nao.get_rect(center=(largura_janela/2,altura_janela/2))
        
      
        janela.blit(sim,sim_rect)
        janela.blit(nao,nao_rect)
        

        

        pygame.display.update()

def pause(fase):
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
                    fase()
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



def colidiu(bloco,paredes):
    for i in paredes:
        if bloco.place().colliderect(i):
            return True
    return False
    

def fase1():
    bloco = Bloco(60,100, id=1)
    bloco.colisao = False
    x_textos = largura_janela-300
    qt_coletados = 0
    player_rect = player.get_rect(center = (50,50))
    while True:
        janela.fill((255,255,255))
        janela.blit(fundo,(0,0))

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
        if teclas[pygame.K_b]:
            pause(fase1)


        if bloco.place().colliderect(botao_up_rect) and bloco.colisao == False:
            bloco.colisao = True
            click.play()
            
        


        q = Bloco(500,200,cor="green")
        q.place()

        # bloco.dx = dx
        # bloco.dy = dy

        
        

        
        

        if bloco.colisao == False:
            janela.blit(botao_up,botao_up_rect)
            if colidiu(bloco,paredes_fase1):
                pass
            else:
                # bloco.x +=dx
                # bloco.y +=dy

                player_rect.x +=dx
                player_rect.y +=dy

            if bloco.place().colliderect(q.place()):
                pass
        else:
            janela.blit(botao_down,botao_down_rect)
            if colidiu(bloco,paredes_fase1):
                pass
            else:
                bloco.x +=dx
                bloco.y +=dy

            if bloco.place().colliderect(q.place()):
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

        janela.blit(player,player_rect)

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

        if bloco.place().colliderect(botao_up_rect) and bloco.colisao == True:
            bloco.colisao = False
            click.play()


        

        bloco.dx = dx
        bloco.dy = dy
        
    

        if bloco.colisao == True:
            janela.blit(botao_up,botao_up_rect)

            if colidiu(bloco,paredes_fase2) or bloco.place().colliderect(f):
                pass
            else:
                bloco.x +=dx
                bloco.y +=dy
        else:
            janela.blit(botao_down,botao_down_rect)
            if colidiu(bloco,paredes_fase2):
                pass
            else:
                bloco.x +=dx
                bloco.y +=dy

          
            
    
        for item in range(len(itens)):
            if bloco.place().colliderect(itens[item].place()):
                coletou.play()
                itens.pop()
                qt_coletados+=1

        
        if qt_coletados == 2:
            fase3()
            

        colisao_texto = fonte.render(f"Colisao:{bloco.colisao} ",True,(0,0,0))
        tamanho_texto = fonte.render(f"Tamanho:{bloco.tamanho} ",True,(0,0,0))
        id_texto = fonte.render(f"Id:{bloco.id} ",True,(0,0,0))
        coletados = fonte.render(f"coletados:{qt_coletados}/{2}",True,(0,0,0))

        janela.blit(colisao_texto,(largura_janela-200,60))
        janela.blit(tamanho_texto,(largura_janela-200,100))
        janela.blit(id_texto,(largura_janela-200,140))
        janela.blit(coletados,(largura_janela-200,180))

        pygame.display.update()

    
def fase3():
    
    bloco = Bloco(50,200, id=1)
    bloco.colisao = True
    qt_coletados =0

    item1 = Bloco(500,200,cor="green")
    item2 = Bloco(50,400,cor="green")
    

    itens = [item1,item2]

    bloco2 = Bloco(500,400,id=2,cor=(0,0,0),colisao=True)

    while True:
        janela.fill((255,255,255))

        desenhar_paredes(paredes_fase3)

        for item in itens:
            item.place()


        clock.tick(60)
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        
        bloco.place()
        bloco2.place()

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

        if bloco.place().colliderect(botao_up_rect) and bloco.id == 1:
            bloco.id =2
            bloco.cor = (0,0,0)
            bloco2.cor = (0,0,255)

            
            mudar.play()
              
        if bloco.id == 1:
            bloco.dx = dx
            bloco.dy = dy
        else:
            bloco2.dx = dx
            bloco2.dy = dy
        
    
        if bloco.id == 1:
            janela.blit(botao_up,botao_up_rect)
            if bloco.colisao == True:
                if colidiu(bloco,paredes_fase3):
                    pass
                else:
                    bloco.x +=dx
                    bloco.y +=dy
                    
            for item in range(len(itens)):
                if bloco.place().colliderect(itens[item].place()):
                    coletou.play()
                    itens.pop()
                    qt_coletados+=1

        else:
            janela.blit(botao_down,botao_down_rect)
            if bloco2.colisao == True:
                if colidiu(bloco2,paredes_fase3):
                    pass
                else:
                    bloco2.x +=dx
                    bloco2.y +=dy
                    
            for item in range(len(itens)):
                if bloco2.place().colliderect(itens[item].place()):
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
