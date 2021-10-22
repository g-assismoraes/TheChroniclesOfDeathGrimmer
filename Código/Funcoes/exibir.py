from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
import pygame
from Funcoes.funcoes1 import *
import os
import sys

#funcao relacionada a criaçao de um unico arquivo .exe
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def inicializa_fundo(janela):
    background = [0,0,0,0,0]
    background2 = [0,0,0,0,0]
    background3 = [0,0,0,0,0]
    for x in range(len(background)):
        background[x] = GameImage(resource_path("Images/Outras/Menu/bg" + str(5-x) + ".png"))
        background[x].set_position(-background[x].width, janela.height - background[x].height)
        background2[x] = GameImage(resource_path("Images/Outras/Menu/bg" + str(5-x) + ".png"))
        background2[x].set_position(janela.width - background[x].width, janela.height - background[x].height)
        background3[x] = GameImage(resource_path("Images/Outras/Menu/bg" + str(5-x) + ".png"))
        background3[x].set_position(background[x].width, janela.height - background[x].height)
        
    return background, background2, background3

def draw_fundo(background, background2, background3):
    for x in range(len(background)):
        background[x].draw()
        background2[x].draw()
        background3[x].draw()

def atualiza_fundo(janela, background, background2, background3):
    for x in range(1,len(background)):
        if background[x].x >= 0:
            background[x].x -= background[x].width
            background2[x].x -= background2[x].width
            background3[x].x -= background3[x].width
        elif background3[x].x <= janela.width-background3[x].width:
            background[x].x += background[x].width
            background2[x].x += background2[x].width
            background3[x].x += background3[x].width

def movimenta_fundo(background, background2, background3, valor):
    for x in range(1, len(background)):
        background[x].x -= valor
        background2[x].x -= valor
        background3[x].x -= valor
        valor += valor

def fade(width, height, janela): 
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    for alpha in range(0, 255):
        fade.set_alpha(alpha)
        janela.screen.blit(fade, (0, 0))
        janela.update()
        if alpha == 254: pygame.time.delay(3)
        else: pygame.time.delay(10)
    return

def cronometro(tempo, janela):
    lock = 0
    while lock < tempo:
        lock += janela.delta_time()
        janela.update()

def exibe_ensinaControles(janela, teclado):
    imagem = GameImage(resource_path("Images/Outras/placa1.png"))
    imagem.set_position(janela.width/2 - imagem.width/2, janela.height - imagem.height + 20)

    while not teclado.key_pressed("ESC"):

        imagem.draw()
        janela.update()

    return

def exibe_pos(janela, teclado, arquivo):
    imagem = GameImage(resource_path(arquivo))
    imagem.set_position(janela.width/2 - imagem.width/2, janela.height - imagem.height - 50)

    while not teclado.key_pressed("ESC"):

        imagem.draw()
        janela.update()

    return

class Botao():
    def __init__(self, original, pressionada, x, y):
        self.imagens = [GameImage(resource_path(original)), GameImage(resource_path(pressionada))]
        [botao.set_position(x - botao.width/2, y) for botao in self.imagens]
        self.curr_img = self.imagens[0]
    
    def draw(self, mouse):
        if mouse.is_over_object(self.curr_img):
            self.curr_img = self.imagens[1]
        else: self.curr_img = self.imagens[0]

        self.curr_img.draw()

def menu_ajustes(botoes, funcoes, teclado, janela, flag=True):
    mouse = Window.get_mouse()

    fundo = GameImage(resource_path("Images/Outras/fundo2.png"))
    controle = Botao(resource_path("Images/Outras/Botoes/controle.png"), resource_path("Images/Outras/Botoes/controle_press.png"), janela.width/2, janela.height/2)
    audio = Botao(resource_path("Images/Outras/Botoes/audio.png"), resource_path("Images/Outras/Botoes/audio_press.png"), controle.curr_img.x + controle.curr_img.width/2,\
        controle.curr_img.y + controle.curr_img.height + 10)

    while not teclado.key_pressed("ESC"):
        fundo.draw()
        controle.draw(mouse)
        audio.draw(mouse)
        if flag: janela.draw_text2("Jogo Pausado", 400, 200, resource_path("Fontes/ROCC.ttf"), 100, (209, 209, 209))
        else: janela.draw_text2("Configurações", 380, 200, resource_path("Fontes/ROCC.ttf"), 100, (209, 209, 209))

        if mouse.is_over_object(controle.curr_img) and mouse.is_button_pressed(1):
            botoes = escolhe_controles(botoes, teclado, janela)
            cronometro(0.3, janela)
        
        elif mouse.is_over_object(audio.curr_img) and mouse.is_button_pressed(1):
            escolhe_volume(0, mouse, funcoes, teclado, janela)
            cronometro(0.3, janela)

        janela.update()
    
    return botoes

def escolhe_volume(volume, mouse, funcoes, teclado, janela):

    cor_original = (209, 209, 209)
    cor_selecionado = (200, 200, 200)
    esc_cor = cor_original

    fundo = GameImage(resource_path("Images/Outras/fundo_volume.png"))
    selec_mus = GameImage(resource_path("Images/Outras/Botoes/selecionador_volume.png"))
    selec_mus.set_position(4.68 * funcoes.musica_vol + 472, 294 - selec_mus.height/2)

    selec_ef = GameImage(resource_path("Images/Outras/Botoes/selecionador_volume.png"))
    selec_ef.set_position(4.68 * funcoes.efeito_vol + 472, 407 - selec_mus.height/2)

    while not teclado.key_pressed("ESC"):

        fundo.draw()
        selec_mus.draw()
        selec_ef.draw()
        mouse_pos = mouse.get_position()

        if mouse.is_over_area([470, 265], [950, 323]) and mouse.is_button_pressed(1):
            if 472 <= selec_mus.x <= 940 and 472 <= mouse_pos[0] <= 940:
                selec_mus.x = mouse_pos[0]

                funcoes.atualiza_musicas((selec_mus.x - 472)/4.68)
        
        elif mouse.is_over_area([470, 380], [950, 430]) and mouse.is_button_pressed(1):
            if 472 <= selec_ef.x <= 940 and 472 <= mouse_pos[0] <= 940:
                selec_ef.x = mouse_pos[0]

                funcoes.atualiza_efeitos((selec_ef.x - 472)/4.68)
                funcoes.sons[1].play()
                cronometro(0.3, janela)

        janela.update()
    
def escolhe_controles(botoes, teclado, janela):

    index = 0
    pos_texto = 160
    somador = 80

    selecionador = GameImage(resource_path("Images/Outras/selecionador.png"))
    selecionador.set_position(janela.width/2 - selecionador.width/2, 137)
    altera_selecionador = [137, 215, 297, 378, 456, 534]

    fundo = GameImage(resource_path("Images/Outras/fundo2.png"))

    cronometro(0.2, janela)
    
    while not teclado.key_pressed("ESC"):

        if teclado.key_pressed("down") and index < 5:
            index += 1
            selecionador.y = altera_selecionador[index]
            cronometro(0.2, janela)
        elif teclado.key_pressed("up") and index > 0:
            index -= 1
            selecionador.y = altera_selecionador[index]
            cronometro(0.2, janela)

        fundo.draw()

        selecionador.draw()

        janela.draw_text2("Use as setas para navegar neste MENU || Pressione ESC para sair", 150, 90, resource_path("Fontes/ROCC.ttf"),\
             40, (200, 200, 200))
        [janela.draw_text2("Pressione o controle para "+ botoes[i][1] + ":  " + botoes[i][0], 340, pos_texto + i*somador, resource_path("Fontes/ROCC.ttf"),\
             40, (255, 255, 255)) for i in range(len(botoes))]

        for letra in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S",
                    "T", "U", "V", "W", "X", "Y", "space"]:
            if (teclado.key_pressed(letra)) and letra not in [botoes[0][0],botoes[1][0],botoes[2][0],botoes[3][0],botoes[4][0],botoes[5][0]]:
                botoes[index][0] = letra
                cronometro(0.2, janela)

        janela.update()
    
    return botoes

class Sons_Menu():
    def __init__(self, volumes):
        self.efeito_vol = volumes[0]
        self.musica_vol = volumes[1]
        self.sons = [Sound(resource_path("Sounds/grito.ogg")), Sound(resource_path("Sounds/corte.ogg"))]
        self.musica = Sound(resource_path("Sounds/mus_menu.ogg"))
        self.musica.set_repeat(True)
        self.atualiza_efeitos(self.efeito_vol)
        self.atualiza_musicas(self.musica_vol)

    def atualiza_efeitos(self, volume):
        self.efeito_vol = volume
        [som.set_volume(self.efeito_vol) for som in self.sons]
    
    def atualiza_musicas(self, volume):
        self.musica_vol = volume
        self.musica.set_volume(self.musica_vol)
    
    def toca_musica(self):
        self.musica.play()
    
    def para_musica(self):
        self.musica.stop()

        return [self.efeito_vol, self.musica_vol]


def menu(botoes, volumes, janela):
    b1, b2, b3 = inicializa_fundo(janela)
    titulo = GameImage(resource_path("Images/Outras/Menu/titulo2.png"))
    som = Sons_Menu(volumes)
    som.toca_musica()

    teclado = Window.get_keyboard()
    mouse = Window.get_mouse()

    cor_original = (209, 209, 209)
    cor_selecionado = (185, 159, 159)
    nj_cor = cor_selecionado
    conf_cor = cor_original

    index = 0


    while True:

        atualiza_fundo(janela, b1, b2, b3)
        draw_fundo(b1, b2, b3)
        movimenta_fundo(b1, b2, b3, 5 * janela.delta_time())

        janela.draw_text2("Jogar", 900, 530, resource_path("Fontes/BITCBLKAD.ttf"), 50, nj_cor)
        janela.draw_text2("Configurações", 810, 590, resource_path("Fontes/BITCBLKAD.ttf"), 50, conf_cor)

        if teclado.key_pressed("down") and index == 0 or mouse.is_over_area([813, 604], [1052, 645]):
            index = 1
            conf_cor, nj_cor = cor_selecionado, cor_original
            
        elif teclado.key_pressed("up") and index == 1 or mouse.is_over_area([906, 534], [1086, 585]):
            index = 0
            nj_cor, conf_cor = cor_selecionado, cor_original

        if index == 0 and (teclado.key_pressed("enter") or (mouse.is_button_pressed(1) and mouse.is_over_area([906, 534], [1086, 585]))):
            volumes =  som.para_musica()
            fade(1200, 700, janela)
            break
        elif index == 1 and (teclado.key_pressed("enter") or (mouse.is_button_pressed(1) and mouse.is_over_area([813, 604], [1052, 645]))):
            botoes = menu_ajustes(botoes, som, teclado, janela, False)

        titulo.draw()


        janela.update()
    
    return 0, botoes, volumes, janela
