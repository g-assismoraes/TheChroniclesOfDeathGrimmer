from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from Geral import *
from Funcoes.exibir import *
from Funcoes.funcoes2_5 import *

def inicia(hp, mp, qtd_almas, botoes, volumes, janela):
    #inicializacao analoga a da primeira fase, entretando recebe os parametros atualizados pós passagem da fase 1

    teclado = Window.get_keyboard()

    funcoes = Funcoes2_5(janela, volumes)

    morte = Morte(hp, mp, qtd_almas)
    alma = Alma(153, 25)

    chao = GameImage(resource_path("Images/Mapas/recortes/chao_Rei.png"))
    chao.set_position(0, janela.height - chao.height)

    background = GameImage(resource_path("Images/Background/Fase 2/throne_room.png"))

    rei = [0 for _ in range (1)]
    posicaoRei = [[960, 405]]
    for i in range(len(rei)): rei[i] = Rei(posicaoRei[i][0], posicaoRei[i][1])

    inimigos = [rei]

    gravidade, normal = 0, 0

    flag_musica = 0

    while True:
        #inicializa musica da fase
        if flag_musica > 3:
            funcoes.toca_musica()
            flag_musica = -10

        #reinicia a fase a depender se o player morreu por queda ou dano
        if morte.current_sprite.y > janela.height or morte.hp <= 14:
            volumes = funcoes.para_musica()
            return inicia(100, 100, morte.almas_salvas, botoes, volumes, janela)

        #desenha fundo e chao
        background.draw()
        chao.draw()

        #atualiza parametros que devem ser atualizados a cada loop
        morte, gravidade, normal = funcoes.analisa_estimulos(morte, chao, botoes, teclado, \
            janela, inimigos, gravidade, normal)

        #checa se o boss foi derrotado para encerrar a fase
        if rei == []:
            if morte.qtd_almas > 13:
                volumes = funcoes.para_musica()
                exibe_pos(janela, teclado, "Images/Outras/carta final feliz.png")
                fade(1200, 700, janela)
                return 2, morte.hp, morte.mp, morte.qtd_almas, janela, botoes, volumes
            else:
                volumes = funcoes.para_musica()
                exibe_pos(janela, teclado, "Images/Outras/final1.png")
                fade(1200, 700, janela)
                return -1, 0, 0, 0, janela, botoes, volumes

        #verifica se foi solicitado a abertura do menu/pause
        if teclado.key_pressed('q'):
            botoes = menu_ajustes(botoes, funcoes, teclado, janela)

        #desenha e da update no boss
        for grupo in inimigos:
            funcoes.desenha_inimigos(grupo)
            funcoes.update_inimigos(grupo, janela.delta_time())

        #desenha o contador de almas
        alma.draw()
        alma.update()
        janela.draw_text2(str(morte.qtd_almas), 200, 52, resource_path("Fontes/ROCC.ttf"), 25, (255, 255, 255))

        #atualizacao de algumas flags relacionadas ao tempo
        tempo = janela.delta_time()
        if flag_musica >= 0: flag_musica += 1

        #desenho e update do player
        morte.draw()
        morte.update(tempo)
        
        #update da janela
        janela.update()