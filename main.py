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


#fontes de texto
fonte_terraria = pygame.font.Font("fontes/ANDYB.TTF",40)
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


enemy_atack = pygame.USEREVENT + 3
pygame.time.set_timer(enemy_atack, 1000)



class Boss(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, life):
        # Inicialização da classe Boss, que herda de pygame.sprite.Sprite
        super().__init__()

        # Lista de sprites para animação do chefe
        self.sprites = [
            pygame.image.load("frames_output/frame_000.png").convert_alpha(),
            pygame.image.load("frames_output/frame_001.png").convert_alpha(),
            pygame.image.load("frames_output/frame_002.png").convert_alpha(),
            pygame.image.load("frames_output/frame_003.png").convert_alpha()
        ]
        
        # Índice do sprite atual da animação
        self.image_atual = 0
        self.image = self.sprites[self.image_atual]  # Imagem atual do chefe
        self.life = life  # Vida do chefe
        self.bullet = pygame.image.load("imagens/boss_bullet.png").convert_alpha()  # Imagem do projétil do chefe
        self.lista_bullet = []  # Lista de projéteis disparados pelo chefe
        
        # Definição da posição do chefe e seu retângulo de colisão
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        
        # Opacidade para efeitos visuais
        self.opacidade = 0

    def update(self, janela, x):
        # Método para atualizar a animação do chefe e movimentar seus projéteis
        self.image_atual += 0.14
        
        if self.image_atual >= len(self.sprites):
            self.image_atual = 0

        self.image = self.sprites[int(self.image_atual)]
        self.imge = pygame.transform.scale(self.image, (64, 64))
        
        self.opacidade += 0.4

        # Movimentação dos projéteis e remoção daqueles que saíram da tela
        for bala in self.lista_bullet:
            bala.y += 10
            
            if bala.y > 600:
                self.lista_bullet.remove(bala)
            janela.blit(self.bullet, bala)

    def ai(self):
        # Método que controla a inteligência artificial do chefe, como a variação de opacidade
        imagem_opaca = self.image.copy()
        if self.opacidade >= 220:
            self.opacidade = 220
        imagem_opaca.fill((255, 255, 255, self.opacidade), None, pygame.BLEND_RGBA_MULT)
        self.image = imagem_opaca

    def atack(self, x):
        # Método para o chefe disparar projéteis em direção ao jogador
        if (x + 65) >= 810:
            self.rect.x = x - 70
            bullet = self.bullet.get_rect(center=(self.rect.x + 150, self.rect.y))
        elif (x + 65) <= 400:
            self.rect.x = x + 70
            bullet = self.bullet.get_rect(center=(self.rect.x + 20, self.rect.y))
        else:
            self.rect.x = x
            bullet = self.bullet.get_rect(center=(self.rect.x + 100, self.rect.y))

        self.lista_bullet.append(bullet)

#interface enemy pra criar inimigos
class Enemy():
    def __init__(self,img,x,y,life,velocidade):
        self.x = x
        self.y = y
        self.life = life
        self.velocidade = velocidade
        self.img = pygame.image.load(img).convert_alpha()
        self.img = pygame.transform.scale(self.img,(64,64))
        self.img_rect = self.img.get_rect(center=(x,y))
        self.vel_enemy = self.velocidade
    def atack(self):
        pass
    def move(self):
        pass
        

class Alien(Enemy):
    def __init__(self,img, x, y,life,velocidade,atack_time= 1000):
        # Chama o construtor da classe pai para inicializar atributos comuns
        super().__init__(img, x, y, life, velocidade)
        self.lasers_list = []
        self.laser = pygame.image.load("alien_laser.png").convert_alpha()
        self.atack_time = atack_time
        self.last_attack_time = pygame.time.get_ticks() 
        
    def atack(self):
        bullet = self.laser.get_rect(center=(self.img_rect.x + 40, self.img_rect.y+10))
        self.lasers_list.append(bullet)

    
        

    def move(self):

        
        for bala in self.lasers_list:
            
            bala.y += 10
            if bala.y > altura_janela - 150:
                self.lasers_list.remove(bala)
                

            janela.blit(self.laser,bala)
      
        if self.img_rect.x < parede_esquerda:
            self.vel_enemy = self.velocidade
            self.img_rect.y +=10
            
            # pass
        if self.img_rect.x > parede_direita:
            self.vel_enemy = -self.velocidade
            self.img_rect.y +=5

        self.img_rect.x += self.vel_enemy

        janela.blit(self.img,self.img_rect)

        
            

class Player():
    def __init__(self, x, y, life=4):
        # Inicialização do jogador com posição, vida e velocidade padrão
        self.x = x
        self.y = y
        self.velocidade = 5
        self.laser_list = []  # Lista de tiros do jogador
        self.life = life  # Vida do jogador
        # Retângulo representando a posição e tamanho do jogador na tela
        self.player_rect = player.get_rect(center=(self.x, self.y))
    
    def atacar(self):
        # Método para o jogador atirar
        laser_rect = laser.get_rect(center=(self.player_rect.x + 34, self.player_rect.y))
        if len(self.laser_list) > 1:
            pass
        else:
            self.laser_list.append(laser_rect)  # Adiciona um novo tiro à lista
            fire.play()  # Reproduz o som de tiro

    def update_life(self, lista_enemys=None):
        # Método para atualizar a vida do jogador e exibir na tela
        for i in range(1, self.life + 1):
            janela.blit(vidas, (parede_esquerda + i * 40 + 50, 130))

            if lista_enemys is not None:
                # Verifica se o jogador colidiu com algum inimigo e reduz a vida
                for enemy in lista_enemys:
                    if enemy.img_rect.colliderect(self.player_rect):
                        self.life -= 1

    def move(self):
        # Método para mover o jogador na tela de acordo com as teclas pressionadas
        teclas = pygame.key.get_pressed()
        dx = 0
        if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and self.player_rect.x > parede_esquerda:
            dx = -self.velocidade
        if (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and self.player_rect.x < parede_direita:
            dx = self.velocidade
        self.player_rect.x += dx

    def draw(self):
        # Método para desenhar os tiros do jogador na tela
        for rect in self.laser_list:
            rect.y -= 10
            if rect.y < 100:
                self.laser_list.remove(rect)  # Remove tiros que saíram da tela
            janela.blit(laser, rect)  # Desenha os tiros na tela

    def colidir(self, lista_enemys=False, boss=None):
        # Método para verificar colisões do jogador com inimigos ou com o chefe
        if lista_enemys == False:
            # Verifica colisões com o chefe e seus projéteis
            for rect in self.laser_list:
                if (boss.rect.colliderect(rect) and boss.opacidade > 180):
                    boss.life -= 1
                    self.laser_list.remove(rect)
                    esplosao.play()

                for bullet in boss.lista_bullet:
                    if bullet.colliderect(rect):
                        boss.lista_bullet.remove(bullet)

            for bullet in boss.lista_bullet:
                if self.player_rect.colliderect(bullet):
                    boss.lista_bullet.remove(bullet)
                    self.life -= 1

        else:
            # Verifica colisões com os inimigos e remove-os da lista se a vida chegar a 0
            for rect in self.laser_list:
                for enemy in lista_enemys:
                    if enemy.img_rect.colliderect(rect):
                        enemy.life -= 1
                        
                        self.laser_list.remove(rect)
                        esplosao.play()
                        if enemy.life <= 0:
                            lista_enemys.remove(enemy)
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
                
                mudanca(menu,"ligando",0)

        pygame.display.update()



def mudanca(fase, texto,pontos):
    # Loop principal para exibir a mudança de fase
    while True:
        # Preenche a janela com uma cor sólida
        janela.fill((0, 0, 0))
        # Exibe o fundo
        janela.blit(fundo, (0, 0))

        # Verifica os eventos do pygame
        for event in pygame.event.get():
            # Se o evento for de fechar a janela, encerra o jogo
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Renderiza o texto na tela
        texto_renderizado = fonte.render(texto, True, (255, 255, 255))
        texto_rect = texto_renderizado.get_rect(center=(largura_janela / 2, altura_janela / 2))
        janela.blit(texto_renderizado, texto_rect)

        # Atualiza a janela
        pygame.display.update()
        
        # Aguarda 2 segundos antes de chamar a próxima fase
        pygame.time.wait(2000)
        fase(pontos)  # Chama a próxima fase após o tempo de espera



def menu(pontos):
    # Carregue a música
    pygame.mixer.music.load('musica/menu.mp3')
    
    

    # Defina o volume (opcional)
    pygame.mixer.music.set_volume(1.0)  # Valor varia de 0.0 a 1.0
    
    pygame.mixer.music.play(-1)


    opcoes = 3
    indice = 0
    azul = (0,0,255)
    branco = (255,255,255)
   
    while True:
        
        janela.fill((255,255,255))
        janela.blit(fundo,(0,0))

        if pygame.joystick.get_count() == 0:
            pass
        else:
            botao_x = controle_ps4.get_button(0) 
            up = controle_ps4.get_button(11)
        
            if botao_x and indice == 0:        
                fase1(pontos)

            if up:
                menu_selection.play()
                indice-=1
                if indice <0:
                    indice = opcoes
            


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and indice == 0:
                    pygame.mixer.music.stop()
                    mudanca(fase1,"Fase 1",pontos)
                    
                if event.key == pygame.K_SPACE and indice == 2:
                    cursor_select.play()
                    tchau()

                if event.key == pygame.K_s:
                    menu_selection.play()
                    indice = indice +1
                    if indice>=opcoes:
                        indice = 0
                if event.key == pygame.K_w:
                    menu_selection.play()
                    indice = indice - 1
                    if indice <0:
                        indice = opcoes-1

        start = fonte.render("Start",True,branco)
        config = fonte.render("conquistas",True,branco)
        sair = fonte.render("Sair",True,branco)

        nome = fonte_nome.render("Game OOP",True,branco)
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
    branco = (255,255,255)
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

        sim = fonte.render("Sim",True,branco)
        nao = fonte.render("Nao",True,branco)
        

        nome = fonte_outros.render("Tem certeza que quer sair?",True,branco)
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

    

def final(pontos):
    #instanciando um objeto player
    jogador = Player(632,591)
    jogador.laser_list = []
    
   
    pygame.mixer.music.load("audios/boss_music.mpeg")

    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1)

    boss_nascendo = pygame.mixer.Sound("audios/boss_nascendo.mp3")
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
        jogador.update_life(None)


        #atualiza janela
        pygame.display.update()


def fase4(pontos):
    jogador = Player(632,591)
    enemy = Alien("imagens/alien.png",parede_esquerda+20,200,5,3,atack_time=1000)
    enemy2 = Alien("imagens/alien.png",parede_direita-20,250,5,3,atack_time=2000)
    enemy3 = Alien("imagens/alien.png",490,300,5,3,atack_time=6000)

    list_enemys = [enemy,enemy2,enemy3]
    
 
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
            current_time = pygame.time.get_ticks()
            if current_time - enemy.last_attack_time >= enemy.atack_time:
                # Executar ataque somente se passou tempo suficiente desde o último ataque
                enemy.last_attack_time = current_time  # Atualiza o tempo do último ataque
                
                enemy.atack()

        if len(list_enemys) == 0:
            mudanca(final,"BOSS FINAL !",pontos)
            


        score = fonte_pequena.render(f"Score: {pontos}",True,(255,255,255))
        vidas = fonte_pequena.render("Life:",True,(255,255,255))

        
  
        janela.blit(player,jogador_rect)
        janela.blit(score,(parede_esquerda +4,90))
        janela.blit(vidas,(parede_esquerda +4,127))
        jogador.update_life(list_enemys)

        pygame.display.update()


def fase3(pontos):
    jogador = Player(632,591)
    enemy = Alien("imagens/alien.png",490,200,5,3,atack_time=4000)
    enemy2 = Alien("imagens/alien.png",600,250,5,3,atack_time=5000)
    enemy3 = Alien("imagens/alien.png",390,300,5,3,atack_time=2000)
    enemy4 = Alien("imagens/alien.png",490,310,5,3,atack_time=7000)
    enemy5 = Alien("imagens/alien.png",parede_esquerda+50,380,5,3)

    list_enemys = [enemy,enemy2,enemy3,enemy4,enemy5]
    
    
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
            current_time = pygame.time.get_ticks()
            if current_time - enemy.last_attack_time >= enemy.atack_time:
                # Executar ataque somente se passou tempo suficiente desde o último ataque
                enemy.last_attack_time = current_time  # Atualiza o tempo do último ataque
                
                enemy.atack()

        if len(list_enemys) == 0:
            
            mudanca(fase4,"Fase 4",pontos)


        score = fonte_pequena.render(f"Score: {pontos}",True,(255,255,255))
        vidas = fonte_pequena.render("Life:",True,(255,255,255))

        
  
        janela.blit(player,jogador_rect)
        janela.blit(score,(parede_esquerda +4,90))
        janela.blit(vidas,(parede_esquerda +4,127))
        jogador.update_life(list_enemys)

        pygame.display.update()
        

def fase2(pontos):
    jogador = Player(632,591)
    enemy = Alien("imagens/alien.png",490,200,5,3,atack_time=3000)
    enemy2 = Alien("imagens/alien.png",600,250,5,3,atack_time=5000)
    enemy3 = Alien("imagens/alien.png",390,300,5,3,atack_time=6000)
    enemy4 = Alien("imagens/red_alien.png",parede_esquerda+40,140,10,7,atack_time=1000)

    list_enemys = [enemy,enemy2,enemy3,enemy4]
    
    
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
        
        
       
        if len(list_enemys) == 0:
            
            mudanca(fase3,"Fase 3",pontos)

        for enemy in list_enemys:
            enemy.move()
            current_time = pygame.time.get_ticks()
            if current_time - enemy.last_attack_time >= enemy.atack_time:
                # Executar ataque somente se passou tempo suficiente desde o último ataque
                enemy.last_attack_time = current_time  # Atualiza o tempo do último ataque
                
                enemy.atack()


        score = fonte_pequena.render(f"Score: {pontos}",True,(255,255,255))
        vidas = fonte_pequena.render("Life:",True,(255,255,255))

        
  
        janela.blit(player,jogador_rect)
        janela.blit(score,(parede_esquerda +4,90))
        janela.blit(vidas,(parede_esquerda +4,127))
        jogador.update_life(list_enemys)

        pygame.display.update()

def fase1(pontos):
    
    jogador = Player(632,591)
    enemy = Alien("imagens/alien.png",490,200,5,3,atack_time=2000)
    enemy2 = Alien("imagens/alien.png",600,250,5,3,atack_time=8000)
    enemy3 = Alien("imagens/alien.png",390,300,5,3,atack_time=4000)

    list_enemys = [enemy,enemy2,enemy3]
    

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
            current_time = pygame.time.get_ticks()
            if current_time - enemy.last_attack_time >= enemy.atack_time:
                # Executar ataque somente se passou tempo suficiente desde o último ataque
                enemy.last_attack_time = current_time  # Atualiza o tempo do último ataque
                
                enemy.atack()
            
        

        if len(list_enemys) == 0:
         
            mudanca(fase2,"Fase 2",pontos)


        score = fonte_pequena.render(f"Score: {pontos}",True,(255,255,255))
        vidas = fonte_pequena.render("Life:",True,(255,255,255))

        
  
        janela.blit(player,jogador_rect)
        janela.blit(score,(parede_esquerda +4,90))
        janela.blit(vidas,(parede_esquerda +4,127))
        jogador.update_life(list_enemys)

        pygame.display.update()




off()
