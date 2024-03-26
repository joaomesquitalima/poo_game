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


parede_esquerda = 357
parede_direita = 860


largura_janela, altura_janela = 1280,720
janela = pygame.display.set_mode((largura_janela,altura_janela))
fonte = pygame.font.Font("ThaleahFat.ttf", 50) #fonte media
fonte_pequena = pygame.font.Font("ThaleahFat.ttf",40)
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

player = pygame.image.load("ship_teste.png").convert_alpha()

player = pygame.transform.scale(player,(64,64))

vidas = pygame.image.load("ship_teste.png").convert_alpha()
vidas = pygame.transform.scale(vidas,(32,32))

enemy = pygame.image.load("alien1.png").convert_alpha()
enemy = pygame.transform.scale(enemy,(64,64))
enemy_rect = enemy.get_rect(center = (413,151))

laser = pygame.image.load("blasterbolt.png").convert_alpha()
laser_rect = laser.get_rect()



clock = pygame.time.Clock()



velocidade = 5

class Inimigo():
    def __init__(self,img,x,y,life,velocidade):
        self.x = x
        self.y = y
        self.life = life
        self.velocidade = velocidade
        self.img = pygame.image.load(img).convert_alpha()
        self.img = pygame.transform.scale(self.img,(64,64))
        self.img_rect = self.img.get_rect(center=(x,y))
    def atack(self):
        pass
    

    

        

class Player():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
        self.player_rect = player.get_rect(center = (self.x,self.y))
    def atacar(self):
        pass


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
        # Obtenha a posição do mouse
        posicao_mouse = pygame.mouse.get_pos()
        print(posicao_mouse)
        janela.fill((255,255,255))
        janela.blit(fundo,(0,0))

        if pygame.joystick.get_count() == 0:
            pass
        else:

            botao_x = controle_ps4.get_button(0) 
            
            up = controle_ps4.get_button(11)
        

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

    

def fase1():
    


    jogador = Player(632,591)
    enemy = Inimigo("alien1.png",390,200,1,3)
    enemy_img = enemy.img
    enemy_rect = enemy.img_rect
    vel_inimigo = enemy.velocidade
    pontos = 0
    while True:
        janela.fill((255,255,255))
        janela.blit(fundo,(0,0))

        jogador_rect = jogador.player_rect

       
        clock.tick(60)
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

      
        # Movimento da nave principal
        teclas = pygame.key.get_pressed()
        dx= 0
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a] and jogador_rect.x > parede_esquerda:
            dx = -velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d] and jogador_rect.x < parede_direita:
            dx = velocidade
        
        jogador_rect.x+=dx


        #movimento alien
        if enemy_rect.x < parede_esquerda:
            vel_inimigo = enemy.velocidade
            enemy_rect.y +=10
            # pass
        if enemy_rect.x > parede_direita:
            vel_inimigo = -enemy.velocidade
            enemy_rect.y +=10

        enemy_rect.x += vel_inimigo

        score = fonte_pequena.render(f"Score: {pontos}",True,(255,255,255))
        vidas = fonte_pequena.render("Life:",True,(255,255,255))

        

      
  
        janela.blit(player,jogador_rect)
        janela.blit(enemy_img,enemy_rect)
        janela.blit(score,(parede_esquerda +4,90))
        janela.blit(vidas,(parede_esquerda +4,127))

        pygame.display.update()







menu()
