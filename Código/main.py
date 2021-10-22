import fase1
import fase2
import fase3
from Geral import *
from Funcoes.exibir import*
from PPlay.window import *

# uma série de variáveis iniciais
flag, hp, mp, qtd_almas, volumes = -1, 0, 0, 0, [50, 50]
botoes = [["A","esquerda"],["D","direita"], ["J","atacar"], ["K","pular"], ["I", "especial"], ["L", "curar"]]
janela = Window(1200,700)
janela.set_title("The Chronicles of Death Grimmer")
pygame.display.set_icon(pygame.image.load(resource_path("Images/Outras/gameicon.png"))) #o icone exibido na barra superior

#loop que controla o fluxo lógico do jogo inteiro, sendo -1 menu, 0 fase 1, 1 fase 2, 2 fase 3
while True:

    if flag == -1: flag, botoes, volumes, janela = menu(botoes, volumes, janela)

    if flag == 0: flag, hp, mp, qtd_almas, janela, botoes, volumes = fase1.inicia(hp, mp, qtd_almas, botoes, volumes, janela)

    if flag == 1: flag, hp, mp, qtd_almas, janela, botoes, volumes = fase2.inicia(hp, mp, qtd_almas, botoes, volumes, janela)

    if flag == 2: flag, hp, mp, qtd_almas, janela, botoes, volumes = fase3.inicia(hp, mp, qtd_almas, botoes, volumes, janela)
