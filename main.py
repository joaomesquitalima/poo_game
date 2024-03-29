import pygame,sys
import time
import random
from game import Boss
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

#fontes
fonte = pygame.font.Font("fontes/ThaleahFat.ttf", 50) #fonte media
fonte_pequena = pygame.font.Font("fontes/ThaleahFat.ttf",40)
fonte_nome = pygame.font.Font("fontes/ThaleahFat.ttf",100)
fonte_outros = pygame.font.Font("fontes/ThaleahFat.ttf",45)


#fundo
fundo = pygame.image.load("imagens/tela_pico8_preta.png")
fundo = pygame.transform.scale(fundo, (largura_janela, altura_janela))

fundo_desligado = pygame.image.load("imagens/tela_pico8_desligado.png")
fundo_desligado = pygame.transform.scale(fundo_desligado, (largura_janela, altura_janela))


#sons
menu_selection = pygame.mixer.Sound('audios/menu_selection.wav')
cursor_select = pygame.mixer.Sound("audios/cursor_select.wav")
cursor_back = pygame.mixer.Sound("audios/cursor_back.wav")
mudar = pygame.mixer.Sound("audios/open_001.ogg")
coletou = pygame.mixer.Sound("audios/coletado.ogg")
click = pygame.mixer.Sound("audios/click.2.ogg")
fire = pygame.mixer.Sound("audios/Shoot_01.mp3")
esplosao = pygame.mixer.Sound("audios/explosion.mp3")

#imagens
player = pygame.image.load("imagens/ship.png").convert_alpha()
player = pygame.transform.scale(player,(64,64))

vidas = pygame.image.load("imagens/ship.png").convert_alpha()
vidas = pygame.transform.scale(vidas,(32,32))

enemy = pygame.image.load("imagens/alien.png").convert_alpha()
enemy = pygame.transform.scale(enemy,(64,64))

laser = pygame.image.load("imagens/blasterbolt.png").convert_alpha()
laser_rect = laser.get_rect()



clock = pygame.time.Clock()





class Inimigo():
    def __init__(self,img,x,y,life,velocidade):
        self.x = x
        self.y = y
        self.life = life
        self.velocidade = velocidade
        self.img = pygame.image.load(img).convert_alpha()
        self.img = pygame.transform.scale(self.img,(64,64))
        self.img_rect = self.img.get_rect(center=(x,y))
        self.vel_inimigo = self.velocidade
    def atack(self):
        pass

    def move(self):
        #movimento alien
        
        
        if self.img_rect.x < parede_esquerda:
            self.vel_inimigo = self.velocidade
            self.img_rect.y +=10
            
            # pass
        if self.img_rect.x > parede_direita:
            self.vel_inimigo = -self.velocidade
            self.img_rect.y +=10

        self.img_rect.x += self.vel_inimigo

        janela.blit(self.img,self.img_rect)

        
            

class Player():
    def __init__(self,x,y,life=4):
        self.x = x
        self.y = y
        self.velocidade = 5
        self.laser_list = []
        self.life = life
        
        self.player_rect = player.get_rect(center = (self.x,self.y))
    def atacar(self):
        # print(len(self.laser_list))
        laser_rect = laser.get_rect(center=(self.player_rect.x+34,self.player_rect.y))
        self.laser_list.append(laser_rect)
        fire.play()

    def updata_life(self,lista_enemys):
        for i in range(1,self.life+1):
            janela.blit(vidas,(parede_esquerda + i*40 + 50,130))
            
            for enemy in lista_enemys:
                if enemy.img_rect.colliderect(self.player_rect):
                    self.life -= 1
        

    def move(self):
        # Movimento da nave principal
        teclas = pygame.key.get_pressed()
        dx= 0
        if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and self.player_rect.x > parede_esquerda:
            dx = -self.velocidade
        if (teclas[pygame.K_RIGHT] or teclas[pygame.K_d] ) and self.player_rect.x < parede_direita:
            dx = self.velocidade
        
        self.player_rect.x+=dx

    def draw(self):
            
        for rect in self.laser_list:
            rect.y -= 10

            if rect.y < 100:
                self.laser_list.remove(rect)
            
        
            janela.blit(laser,rect)
    def colidir(self,lista_enemys=False,boss=None):
        if lista_enemys == False:
            for rect in self.laser_list:
                if boss.colliderect(rect):
                    self.laser_list.remove(rect)
                    esplosao.play()
        else:
            for rect in self.laser_list:
                for enemy in lista_enemys:
                    if enemy.img_rect.colliderect(rect):
                        lista_enemys.remove(enemy)
                        self.laser_list.remove(rect)
                        esplosao.play()
                        return True

        



def off():
    while True:
        janela.fill((255,255,255))
        janela.blit(fundo_desligado,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                pygame.time.wait(500)
                menu()

        pygame.display.update()




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
    # pygame.time.set_timer(teste,200)
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

    



def final():
    jogador = Player(632,591)

    moving_sprites = pygame.sprite.Group()
    boss = Boss(550,120)
    moving_sprites.add(boss)
    while True:
        janela.fill((255,255,255))
        janela.blit(fundo,(0,0))

        jogador_rect = jogador.player_rect
        jogador.draw()

        jogador.colidir(lista_enemys=False,boss=boss.rect)

       
        clock.tick(60)
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jogador.atacar()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                jogador.atacar()

      
        jogador.move()
        moving_sprites.draw(janela)
        moving_sprites.update()
        janela.blit(player,jogador_rect)

        pygame.display.update()
        
        




def fase1():
    


    jogador = Player(632,591)
    enemy = Inimigo("imagens/alien.png",490,200,1,3)
    enemy2 = Inimigo("imagens/alien.png",600,250,1,3)
    enemy3 = Inimigo("imagens/alien.png",390,300,1,3)

    enemy4 = Inimigo("imagens/alien.png",490,200,1,3)
    enemy5 = Inimigo("imagens/alien.png",600,250,1,3)
    enemy6 = Inimigo("imagens/alien.png",390,300,1,3)

    enemy7 = Inimigo("imagens/alien.png",490,200,1,3)
    enemy8 = Inimigo("imagens/alien.png",600,250,1,3)
    enemy9 = Inimigo("imagens/alien.png",390,300,1,3)

    list_enemys = [enemy,enemy2,enemy3]

    lista2_enemys = [enemy4,enemy5,enemy6]

    lista3_enemys = [enemy7,enemy8,enemy9]


    
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jogador.atacar()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                jogador.atacar()

      
        jogador.move()
        jogador.draw()
        
        if jogador.colidir(list_enemys):
            pontos+=1
        
        

        for enemy in list_enemys:
            enemy.move()

        if len(list_enemys) == 0:
            final()

        



        score = fonte_pequena.render(f"Score: {pontos}",True,(255,255,255))
        vidas = fonte_pequena.render("Life:",True,(255,255,255))

        # for i in range(2):
          
        #     x = random.randint(parede_esquerda, parede_direita )  # Posição x aleatória
        #     y = random.randint(0, altura_janela )  # Posição y aleatória
        #     pygame.draw.rect(janela, (255,255,255), (x, y, 20, 20))

        
  
        janela.blit(player,jogador_rect)
        janela.blit(score,(parede_esquerda +4,90))
        janela.blit(vidas,(parede_esquerda +4,127))
        jogador.updata_life(list_enemys)

        pygame.display.update()







off()
