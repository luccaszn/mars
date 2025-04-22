import pygame
import random
import math
import os

pygame.init()
pygame.mixer.init()
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Toupeira - Missão de Mapeamento")

# Sons (caminhos corrigidos)
som_recarga = pygame.mixer.Sound("recarga.wav")
som_andar = pygame.mixer.Sound("andar.wav")
som_tempestade = pygame.mixer.Sound("tempestade.wav")
som_alerta = pygame.mixer.Sound("alerta.wav")
som_vitoria = pygame.mixer.Sound("vitoria.wav")
som_derrota = pygame.mixer.Sound("derrota.wav")

# Cores
COR_TOUPEIRA = (255, 255, 255)
COR_TOUPEIRA_SUBTERRANEA = (100, 100, 100)
COR_PSEUDOLITE = (50, 150, 255)
COR_BARRA = (0, 255, 0)
COR_CONTORNO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Mundo
LARGURA_MUNDO = 1600
ALTURA_MUNDO = 1200
AREA_EXPLORAR_OBJETIVO = 1.0

# Jogador
jogador = pygame.Rect(100, 100, 40, 40)
velocidade = 7.5
energia_max = 200
energia = energia_max
subterraneo = False
tempo_subterraneo = 0
particulas = []

# Tempestade
tempestade_ativa = False
tempestade_x = 0
tempestade_y = 0
tempestade_raio = 200
tempestade_duracao = 300
contador_tempestade = 0
tempo_proxima_tempestade = 0

# Pseudolites
pseudolites = [
    pygame.Rect(300, 300, 60, 60),
    pygame.Rect(1300, 300, 60, 60),
    pygame.Rect(800, 1000, 60, 60)
]

# Exploração e minimapa
MINIMAPA_TAMANHO = 200
minimapa_surface = pygame.Surface((MINIMAPA_TAMANHO, MINIMAPA_TAMANHO))
explorado = pygame.Surface((LARGURA_MUNDO, ALTURA_MUNDO))
explorado.fill((0, 0, 0))

# Textura de fundo
textura_fundo = pygame.image.load("textura_marte.png").convert()
textura_fundo = pygame.transform.scale(textura_fundo, (100, 100))

def desenhar_fundo():
    for x in range(0, LARGURA_MUNDO, 100):
        for y in range(0, ALTURA_MUNDO, 100):
            tela.blit(textura_fundo, (x - camera_x, y - camera_y))

def atualizar_exploracao():
    if not subterraneo:
        pygame.draw.circle(explorado, (240, 240, 240), (jogador.centerx, jogador.centery), 100)

def desenhar_minimapa():
    minimapa_surface.fill((0, 0, 0))
    escala_x = MINIMAPA_TAMANHO / LARGURA_MUNDO
    escala_y = MINIMAPA_TAMANHO / ALTURA_MUNDO
    mini_explorado = pygame.transform.scale(explorado, (MINIMAPA_TAMANHO, MINIMAPA_TAMANHO))
    minimapa_surface.blit(mini_explorado, (0, 0))
    
    # Pseudolites
    for p in pseudolites:
        x = int(p.centerx * escala_x)
        y = int(p.centery * escala_y)
        pygame.draw.rect(minimapa_surface, COR_PSEUDOLITE, (x - 2, y - 2, 4, 4))

    # Tempestade
    if tempestade_ativa:
        tx = int(tempestade_x * escala_x)
        ty = int(tempestade_y * escala_y)
        tr = int(tempestade_raio * escala_x)
        pygame.draw.circle(minimapa_surface, (100, 30, 30), (tx, ty), tr)

    # Toupeira
    jx = int(jogador.centerx * escala_x)
    jy = int(jogador.centery * escala_y)
    pygame.draw.rect(minimapa_surface, (0, 255, 255), (jx - 2, jy - 2, 4, 4))

    tela.blit(minimapa_surface, (LARGURA_TELA - MINIMAPA_TAMANHO - 10, 10))


def desenhar_barra_energia():
    largura_barra = 200
    altura_barra = 15
    x, y = 10, 10
    proporcao = energia / energia_max
    pygame.draw.rect(tela, (100, 100, 100), (x, y, largura_barra, altura_barra))
    pygame.draw.rect(tela, COR_BARRA, (x, y, int(largura_barra * proporcao), altura_barra))
    pygame.draw.rect(tela, BRANCO, (x, y, largura_barra, altura_barra), 2)
    texto = fonte.render("Energia", True, BRANCO)
    tela.blit(texto, (x + largura_barra + 10, y - 2))

def toupeira_em_tempestade():
    if not tempestade_ativa:
        return False
    dist = math.hypot(jogador.centerx - tempestade_x, jogador.centery - tempestade_y)
    return dist <= tempestade_raio

def area_explorada_percentual():
    pixels = pygame.surfarray.array2d(explorado)
    total = pixels.size
    claros = (pixels != 0).sum()
    return claros / total

def gerar_particula():
    if subterraneo: return
    for _ in range(3):
        offset_x = random.randint(-10, 10)
        offset_y = random.randint(-10, 10)
        particulas.append([jogador.centerx + offset_x, jogador.centery + offset_y, random.randint(10, 20)])

# Tela inicial
def tela_inicial():
    tela.fill((20, 20, 20))
    titulo = grande.render("T.O.U.P.E.I.R.A.", True, BRANCO)
    subtitulo = fonte.render("Tecnologia de Orientação e Utilização Para Exploração Integrada de Recursos em Ambientes hostis", True, BRANCO)
    start = fonte.render("Pressione qualquer tecla para iniciar a missão", True, BRANCO)
    tela.blit(titulo, titulo.get_rect(center=(LARGURA_TELA//2, 200)))
    tela.blit(subtitulo, subtitulo.get_rect(center=(LARGURA_TELA//2, 260)))
    tela.blit(start, start.get_rect(center=(LARGURA_TELA//2, 340)))
    pygame.display.flip()
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN:
                esperando = False
# Loop principal
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 24)
grande = pygame.font.SysFont(None, 40)
camera_x = 0
camera_y = 0
venceu = False
tela_inicial()
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()
    dx = dy = 0
    if teclas[pygame.K_LEFT]: dx -= velocidade
    if teclas[pygame.K_RIGHT]: dx += velocidade
    if teclas[pygame.K_UP]: dy -= velocidade
    if teclas[pygame.K_DOWN]: dy += velocidade

    if dx != 0 or dy != 0:
        som_andar.play()
        gerar_particula()

    jogador.move_ip(dx, dy)
    jogador.clamp_ip(pygame.Rect(0, 0, LARGURA_MUNDO, ALTURA_MUNDO))

    colidiu = False
    for p in pseudolites:
        if jogador.colliderect(p):
            colidiu = True
            if energia < energia_max:
                energia += 0.7
                som_recarga.play()
            break

    if not colidiu:
        energia -= 0.15
        energia = max(0, energia)
        if energia < 30:
            som_alerta.play()

    camera_x = jogador.centerx - LARGURA_TELA // 2
    camera_y = jogador.centery - LARGURA_TELA // 2
    camera_x = max(0, min(camera_x, LARGURA_MUNDO - LARGURA_TELA))
    camera_y = max(0, min(camera_y, ALTURA_MUNDO - ALTURA_TELA))

    if not tempestade_ativa and pygame.time.get_ticks() > tempo_proxima_tempestade:
        tempestade_ativa = True
        tempestade_x = random.randint(0, LARGURA_MUNDO)
        tempestade_y = random.randint(0, ALTURA_MUNDO)
        contador_tempestade = tempestade_duracao
        som_tempestade.play()
    elif tempestade_ativa:
        contador_tempestade -= 1
        if contador_tempestade <= 0:
            tempestade_ativa = False
            tempo_proxima_tempestade = pygame.time.get_ticks() + random.randint(5000, 10000)

    if toupeira_em_tempestade():
        subterraneo = True
        tempo_subterraneo = pygame.time.get_ticks()
    if subterraneo and pygame.time.get_ticks() - tempo_subterraneo > 3000:
        subterraneo = False

    atualizar_exploracao()
    desenhar_fundo()

    # Mostrar tempestade
    if tempestade_ativa:
        pygame.draw.circle(tela, (60, 20, 20), (tempestade_x - camera_x, tempestade_y - camera_y), tempestade_raio)

    # Partículas
    for i in range(len(particulas) - 1, -1, -1):
        x, y, t = particulas[i]
        pygame.draw.circle(tela, (220, 220, 220), (int(x - camera_x), int(y - camera_y)), 2)
        particulas[i][2] -= 1
        if particulas[i][2] <= 0:
            particulas.pop(i)

    # Pseudolites
    for p in pseudolites:
        pygame.draw.rect(tela, COR_PSEUDOLITE, (p.x - camera_x, p.y - camera_y, p.width, p.height))

    # Toupeira
    cor_toupeira = COR_TOUPEIRA_SUBTERRANEA if subterraneo else COR_TOUPEIRA
    pygame.draw.rect(tela, cor_toupeira, (jogador.x - camera_x, jogador.y - camera_y, jogador.width, jogador.height), border_radius=6)
    pygame.draw.rect(tela, COR_CONTORNO, (jogador.x - camera_x, jogador.y - camera_y, jogador.width, jogador.height), 2, border_radius=6)

    desenhar_minimapa()
    desenhar_barra_energia()

    # Derrota
    if energia <= 0:
        tela.fill((0, 0, 0))
        linha1 = grande.render("Missão encerrada: Energia esgotada.", True, BRANCO)
        linha2 = grande.render("A Toupeira entrou em modo de espera.", True, BRANCO)
        tela.blit(linha1, linha1.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 25)))
        tela.blit(linha2, linha2.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 25)))
        som_derrota.play()
        pygame.display.flip()
        pygame.time.wait(5000)
        break

    # Vitória
    if not venceu and area_explorada_percentual() >= AREA_EXPLORAR_OBJETIVO:
        venceu = True
        texto = grande.render("Parabéns! Área 100% mapeada!", True, BRANCO)
        tela.blit(texto, texto.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2)))
        som_vitoria.play()
        pygame.display.flip()
        pygame.time.wait(5000)
        rodando = False  # Encerra o loop após vitória

    pygame.display.flip()
    relogio.tick(60)

pygame.quit()
