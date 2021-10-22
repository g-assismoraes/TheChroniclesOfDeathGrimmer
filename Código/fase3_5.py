from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from Geral import *
from Funcoes.exibir import *
from Funcoes.funcoes3_5 import *

def inicia(hp, mp, qtd_almas, botoes, volumes, janela):
    #inicializacoes similares as das fases anteriores

    teclado = Window.get_keyboard()

    funcoes = Funcoes3_5(janela, volumes)

    morte = Morte(hp, mp, qtd_almas)
    alma = Alma(153, 25)

    chao = GameImage(resource_path("Images/Mapas/recortes/final_forest.png"))
    chao.set_position(-3, janela.height - chao.height)

    background = GameImage(resource_path("Images/Background/Fase 3/final_forest.png"))

    reiCalamidade = [0 for _ in range (1)]
    posicaoReiCalamidade = [[960, 375]]
    for i in range(len(reiCalamidade)): reiCalamidade[i] = Rei(posicaoReiCalamidade[i][0], posicaoReiCalamidade[i][1])
    pilares, bolas, caes = [], [], []

    ataques = [pilares, bolas, caes]

    inimigos = [reiCalamidade]

    gravidade, normal = 0, 0

    flag_musica = 0

    while True:
        #inicializa musica
        if flag_musica > 3:
            funcoes.toca_musica()
            flag_musica = -10

        #checa se o jogador morreu por queda ou dano para reinicar a fase
        if morte.current_sprite.y > janela.height or morte.hp <= 14:
            volumes = funcoes.para_musica()
            return inicia(100, 100, morte.almas_salvas, botoes, volumes, janela)

        #desenha o fundo e o chao
        background.draw()
        chao.draw()

        #atualiza parametros que devem ser atualizados a cada loop
        morte, gravidade, normal, ataques = funcoes.analisa_estimulos(morte, chao, botoes, teclado, \
            janela, inimigos, gravidade, normal, ataques)

        #checa se o boss morreu para encerrer a fase, nesse caso, o jogo.. o que implica voltar ao menu
        if reiCalamidade == []:
            volumes = funcoes.para_musica()
            exibe_pos(janela, teclado, "Images/Outras/pergaminho final .png")
            fade(1200, 700, janela)
            return -1, 0, 0, 0, janela, botoes, volumes

        #checa se foi solicitada a abertura do menu ou pause
        if teclado.key_pressed('q'):
            botoes = menu_ajustes(botoes, funcoes, teclado, janela)

        #desenha e atualiza inimgigos
        for grupo in inimigos:
            funcoes.desenha_inimigos(grupo)
            funcoes.update_inimigos(grupo, janela.delta_time())

        #desenha e atualiza o contador de almas
        alma.draw()
        alma.update()
        janela.draw_text2(str(morte.qtd_almas), 200, 52, resource_path("Fontes/ROCC.ttf"), 25, (255, 255, 255))

        #atualiza parametros relacionados ao tempo
        tempo = janela.delta_time()
        if flag_musica >= 0: flag_musica += 1

        #draw e update no player
        morte.draw()
        morte.update(tempo)

        #update na janela
        janela.update()
