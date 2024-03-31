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


#fontes de texto
fonte_terraria = pygame.font.Font("Terraria-Font/ANDYB.TTF",40)
fonte = pygame.font.Font("fontes/ThaleahFat.ttf", 50) 
fonte_pequena = pygame.font.Font("fontes/ThaleahFat.ttf",40)
fonte_nome = pygame.font.Font("fontes/ThaleahFat.ttf",100)
fonte_outros = pygame.font.Font("fontes/ThaleahFat.ttf",45)


#fundo
fundo = pygame.image.load("imagens/tela_pico8_preta.png")
fundo = pygame.transform.scale(fundo, (largura_janela, altura_janela))

fundo_desligado = pygame.image.load("imagens/tela_pico8_desligado.png")
fundo_desligado = pygame.transform.scale(fundo_desligado, (largura_janela, altura_janela))


#sons de efeito
menu_selection = pygame.mixer.Sound('audios/menu_selection.wav')
cursor_select = pygame.mixer.Sound("audios/cursor_select.wav")
cursor_back = pygame.mixer.Sound("audios/cursor_back.wav")
mudar = pygame.mixer.Sound("audios/open_001.ogg")

fire = pygame.mixer.Sound("audios/Shoot_01.mp3")
fire.set_volume(0.7)
esplosao = pygame.mixer.Sound("audios/explosion.mp3")
esplosao.set_volume(0.7)

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

        
        if self.img_rect.x < parede_esquerda:
            self.vel_inimigo = self.velocidade
            self.img_rect.y +=10
            
            # pass
        if self.img_rect.x > parede_direita:
            self.vel_inimigo = -self.velocidade
            self.img_rect.y +=5

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
        if len(self.laser_list) > 1:
            pass
        else:
        
            self.laser_list.append(laser_rect)
        
            fire.play()

    def updata_life(self,lista_enemys=None):
        for i in range(1,self.life+1):
            janela.blit(vidas,(parede_esquerda + i*40 + 50,130))

            if lista_enemys != None:
            
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
            # se boss colidir com laser
                if (boss.rect.colliderect(rect) and boss.opacidade > 180):
                    boss.life-= 1
                    self.laser_list.remove(rect)
                    esplosao.play()

                for bullet in boss.lista_bullet:
                    
                    
                    if bullet.colliderect(rect):
                        # self.laser_list.remove(rect)
                        boss.lista_bullet.remove(bullet)
                        
                    

               
            for bullet in boss.lista_bullet:
                if self.player_rect.colliderect(bullet):
                    boss.lista_bullet.remove(bullet)
                    self.life -= 1
                        

        else:
            for rect in self.laser_list:
                for enemy in lista_enemys:
                    if enemy.img_rect.colliderect(rect):
                        enemy.life -=1
                       
                        
                        if enemy.life <=0:
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
                
                transicao(menu,"ligando")

        pygame.display.update()



def transicao(fase,texto):
    
    
    while True:
        janela.fill((0,0,0))
        janela.blit(fundo,(0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        

        texto = fonte.render(texto,True,(255,255,255))
        texto_rect = texto.get_rect(center=(largura_janela/2,altura_janela/2))
        janela.blit(texto,texto_rect)
        
        

        pygame.display.update()
        pygame.time.wait(2000)
        fase()



def menu():
    # Carregue a música
    pygame.mixer.music.load('musica/menu.mp3')
    
    

    # Defina o volume (opcional)
    pygame.mixer.music.set_volume(1.0)  # Valor varia de 0.0 a 1.0
    
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
                    pygame.mixer.music.stop()
                    transicao(fase1,"Fase 1")
                    
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
    #instanciando um objeto player
    jogador = Player(632,591)
    jogador.laser_list = []
    
   
    pygame.mixer.music.load("boss_music.mpeg")

    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1)

    boss_nascendo = pygame.mixer.Sound("boss_nascendo.mp3")
    boss_nascendo.play()


    moving_sprites = pygame.sprite.Group()
    boss = Boss(largura_janela/2,altura_janela/2 - 100,100)
    moving_sprites.add(boss)

    # Defina um evento personalizado
    inicio_ataque= pygame.USEREVENT + 1

    padrao1 = pygame.USEREVENT + 2

    pygame.time.set_timer(inicio_ataque, 5 * 1000)

    pygame.time.set_timer(padrao1, 500)

    ataque = False

    texto =  fonte_terraria.render("Cérebro de Cthulhu nasceu",True,(255,255,255))
    texto_rect = texto.get_rect(center = (largura_janela/2,altura_janela/2))

    while True:
        clock.tick(60)
        janela.fill((255,255,255))
        janela.blit(fundo,(0,0))
        boss.ai()

        jogador_rect = jogador.player_rect
        jogador.draw()
        

        jogador.colidir(lista_enemys=False,boss=boss)

        if ataque == False:
            janela.blit(texto,texto_rect)


        # percorre todos os eventos que ocorrem no jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == inicio_ataque:
                ataque = True

            if ataque and event.type == padrao1:
                boss.atack(jogador_rect.x - 65)
                

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jogador.atacar()
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                jogador.atacar()

        #faz com que o jogador se mova
        jogador.move()


        #desenha os sprites do boss
        moving_sprites.draw(janela)
        moving_sprites.update(janela,jogador_rect.x - 50)
        
        
        janela.blit(player,jogador_rect)

        

        
        vidas = fonte_pequena.render("Life:",True,(255,255,255))
        janela.blit(vidas,(parede_esquerda +4,127))
        jogador.updata_life(None)


        #atualiza janela
        pygame.display.update()


def fase4():
    jogador = Player(632,591)
    enemy = Inimigo("imagens/alien.png",parede_esquerda+20,200,5,3)
    enemy2 = Inimigo("imagens/alien.png",parede_direita-20,250,5,3)
    enemy3 = Inimigo("imagens/alien.png",490,300,5,3)

    list_enemys = [enemy,enemy2,enemy3]
    
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
            transicao(final,"BOSS FINAL !")
            # transicao(fase2,"Fase 2")


        score = fonte_pequena.render(f"Score: {pontos}",True,(255,255,255))
        vidas = fonte_pequena.render("Life:",True,(255,255,255))

        
  
        janela.blit(player,jogador_rect)
        janela.blit(score,(parede_esquerda +4,90))
        janela.blit(vidas,(parede_esquerda +4,127))
        jogador.updata_life(list_enemys)

        pygame.display.update()


def fase3():
    jogador = Player(632,591)
    enemy = Inimigo("imagens/alien.png",490,200,5,3)
    enemy2 = Inimigo("imagens/alien.png",600,250,5,3)
    enemy3 = Inimigo("imagens/alien.png",390,300,5,3)

    list_enemys = [enemy,enemy2,enemy3]
    
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
            # transicao(final,"BOSS FINAL !")
            transicao(fase4,"Fase 4")


        score = fonte_pequena.render(f"Score: {pontos}",True,(255,255,255))
        vidas = fonte_pequena.render("Life:",True,(255,255,255))

        
  
        janela.blit(player,jogador_rect)
        janela.blit(score,(parede_esquerda +4,90))
        janela.blit(vidas,(parede_esquerda +4,127))
        jogador.updata_life(list_enemys)

        pygame.display.update()
        

def fase2():
    jogador = Player(632,591)
    enemy = Inimigo("imagens/alien.png",490,200,5,3)
    enemy2 = Inimigo("imagens/alien.png",600,250,5,3)
    enemy3 = Inimigo("imagens/alien.png",390,300,5,3)

    list_enemys = [enemy,enemy2,enemy3]
    
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
            # transicao(final,"BOSS FINAL !")
            transicao(fase3,"Fase 3")


        score = fonte_pequena.render(f"Score: {pontos}",True,(255,255,255))
        vidas = fonte_pequena.render("Life:",True,(255,255,255))

        
  
        janela.blit(player,jogador_rect)
        janela.blit(score,(parede_esquerda +4,90))
        janela.blit(vidas,(parede_esquerda +4,127))
        jogador.updata_life(list_enemys)

        pygame.display.update()

def fase1():
    
    jogador = Player(632,591)
    enemy = Inimigo("imagens/alien.png",490,200,5,3)
    enemy2 = Inimigo("imagens/alien.png",600,250,5,3)
    enemy3 = Inimigo("imagens/alien.png",390,300,5,3)

    list_enemys = [enemy,enemy2,enemy3]
    
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
            # transicao(final,"BOSS FINAL !")
            transicao(fase2,"Fase 2")


        score = fonte_pequena.render(f"Score: {pontos}",True,(255,255,255))
        vidas = fonte_pequena.render("Life:",True,(255,255,255))

        
  
        janela.blit(player,jogador_rect)
        janela.blit(score,(parede_esquerda +4,90))
        janela.blit(vidas,(parede_esquerda +4,127))
        jogador.updata_life(list_enemys)

        pygame.display.update()




off()
