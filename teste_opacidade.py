import pygame
import sys

# Inicialize o Pygame
pygame.init()

# Defina o tamanho da janela
largura_janela = 800
altura_janela = 600
janela = pygame.display.set_mode((largura_janela, altura_janela))
pygame.display.set_caption("Janela Vazia")

# Carregue a imagem com transparência
imagem = pygame.image.load("frames_output/frame_000.png").convert_alpha()

# Defina a opacidade desejada (0 a 255)
opacidade = 220  # Por exemplo, defina a opacidade para 50%

# Crie uma cópia da imagem com transparência e opacidade ajustada
imagem_opaca = imagem.copy()
imagem_opaca.fill((255, 255, 255, opacidade), None, pygame.BLEND_RGBA_MULT)

# Loop principal do programa
rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    # Desenhe a imagem opaca na tela
    janela.fill((0, 0, 0))  # Preencha a tela com preto para melhor visualização da opacidade
    janela.blit(imagem_opaca, (0, 0))

    # Atualize a janela
    pygame.display.update()

pygame.quit()
sys.exit()
