import pygame
import random

# Inicialização
pygame.init()
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Exploração em Marte com Radar")

# Cores
COR_MARTE = (201, 81, 38)
COR_CRATERA = (120, 50, 20)
COR_JOGADOR = (200, 200, 255)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Mundo
LARGURA_MUNDO = 1600
ALTURA_MUNDO = 1200

# Jogador
jogador = pygame.Rect(100, 100, 40, 40)
velocidade = 5

# Crateras aleatórias
crateras = []
for _ in range(100):
    x = random.randint(0, LARGURA_MUNDO)
    y = random.randint(0, ALTURA_MUNDO)
    raio = random.randint(15, 30)
    crateras.append((x, y, raio))

# Minimapa
MINIMAPA_TAMANHO = 200
minimapa_surface = pygame.Surface((MINIMAPA_TAMANHO, MINIMAPA_TAMANHO))

# Mapa de exploração (inicialmente tudo escuro)
explorado = pygame.Surface((LARGURA_MUNDO, ALTURA_MUNDO))
explorado.fill(PRETO)

def atualizar_exploracao():
    # Revela uma área circular em torno do jogador no mapa de exploração
    pygame.draw.circle(explorado, BRANCO, (jogador.centerx, jogador.centery), 100)

def desenhar_minimapa():
    minimapa_surface.fill(PRETO)
    escala_x = MINIMAPA_TAMANHO / LARGURA_MUNDO
    escala_y = MINIMAPA_TAMANHO / ALTURA_MUNDO

    # Reduz a área explorada para caber no minimapa
    minimapa_explorado = pygame.transform.scale(explorado, (MINIMAPA_TAMANHO, MINIMAPA_TAMANHO))
    minimapa_surface.blit(minimapa_explorado, (0, 0))

    # Jogador no minimapa
    jogador_x = int(jogador.x * escala_x)
    jogador_y = int(jogador.y * escala_y)
    pygame.draw.rect(minimapa_surface, (0, 255, 255), (jogador_x - 2, jogador_y - 2, 4, 4))

    tela.blit(minimapa_surface, (LARGURA_TELA - MINIMAPA_TAMANHO - 10, 10))

# Loop principal
relogio = pygame.time.Clock()
rodando = True
camera_x = 0
camera_y = 0

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Movimento do jogador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        jogador.x -= velocidade
    if teclas[pygame.K_RIGHT]:
        jogador.x += velocidade
    if teclas[pygame.K_UP]:
        jogador.y -= velocidade
    if teclas[pygame.K_DOWN]:
        jogador.y += velocidade

    # Limites do mundo
    jogador.x = max(0, min(jogador.x, LARGURA_MUNDO - jogador.width))
    jogador.y = max(0, min(jogador.y, ALTURA_MUNDO - jogador.height))

    # Atualiza a câmera
    camera_x = jogador.x - LARGURA_TELA // 2
    camera_y = jogador.y - ALTURA_TELA // 2
    camera_x = max(0, min(camera_x, LARGURA_MUNDO - LARGURA_TELA))
    camera_y = max(0, min(camera_y, ALTURA_MUNDO - ALTURA_TELA))

    # Atualiza mapa de exploração
    atualizar_exploracao()

    # Desenha fundo marciano
    tela.fill(COR_MARTE)

    # Desenha crateras
    for x, y, raio in crateras:
        pygame.draw.circle(tela, COR_CRATERA, (x - camera_x, y - camera_y), raio)

    # Desenha jogador
    pygame.draw.rect(tela, COR_JOGADOR, (jogador.x - camera_x, jogador.y - camera_y, jogador.width, jogador.height))

    # Desenha minimapa
    desenhar_minimapa()

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()