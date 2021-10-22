from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from Funcoes.funcoes2 import *
from Funcoes.exibir import *
import fase2_5
from Geral import *

def inicia(hp, mp, qtd_almas, botoes, volumes, janela):
    #inicializacoes similares as anteriores

    teclado = Window.get_keyboard()
    funcoes = Funcoes2(janela, volumes)

    morte = Morte(hp, mp, qtd_almas)

    alma = Alma(153, 25)

    move_tela = 0.3

    chao_colisivo = [GameImage(resource_path("Images/Mapas/recortes/recorte_castelo_chao" + str(x + 1) + ".png")) for x in range(3)]
    pos_chao = [[0, janela.height - chao_colisivo[0].height], [967, janela.height - chao_colisivo[1].height],
                [2070, janela.height - chao_colisivo[2].height]]
    for x in range(3):
        chao_colisivo[x].set_position(pos_chao[x][0],pos_chao[x][1])
    
    chao = chao_colisivo

    background = funcoes.inicializa_fundo()

    cavaleiros = [0 for _ in range(3)]
    posicaoCavaleiros=[[350, 510, 0],[750, 510, 0], [2650,510, 2]]
    for i in range(len(cavaleiros)): cavaleiros[i] = Cavaleiro(posicaoCavaleiros[i][0], posicaoCavaleiros[i][1], posicaoCavaleiros[i][2])

    lanceiras = [0 for _ in range(3)]
    posicaoLanceiras=[[1250, 405, 1],[1610, 405, 1], [3350, 440, 2]]
    for i in range(len(lanceiras)): lanceiras[i] = Lanceira(posicaoLanceiras[i][0], posicaoLanceiras[i][1], posicaoLanceiras[i][2])
    lancas = []

    inimigos = [cavaleiros, lanceiras, lancas]

    gravidade, normal = 0, 0

    flag_musica = 0

    while True:
        
        #inicializa a musica da fase
        if flag_musica > 3:
            funcoes.toca_musica()
            flag_musica = -10

        #checa se o inimigo morreu por queda ou dano para reiniciar a fase
        if morte.current_sprite.y > janela.height or morte.hp <= 14:
            volumes = funcoes.para_musica()
            return inicia(100, 100, morte.almas_salvas, botoes, volumes, janela)
        
        #desenha o fundo
        funcoes.draw_fundo(background)

        #desenha o chao, com a peculiaridade que para essa fase o chao e chao colisivo sao iguais, uma vez que nao ha adereços
        for x in range(3):
            chao_colisivo[x].draw()

        #corrige o fundo
        funcoes.atualiza_fundo(background, chao[0])

        #atualiza parametros que devem ser atualizados a cada loop
        morte, move_tela, gravidade, normal = funcoes.analisa_estimulos(morte, chao, chao_colisivo, botoes, teclado, \
            janela, background, inimigos, move_tela, gravidade, normal)

        #avalia se foi solicitado a abertura do menu/pause
        if teclado.key_pressed('q'):
            botoes = menu_ajustes(botoes, funcoes, teclado, janela)

        #draw e update nos inimigos
        for grupo in inimigos:
            funcoes.corrige_eixoInimigos(grupo, chao[0].x)
            funcoes.desenha_inimigos(grupo)
            funcoes.update_inimigos(grupo, janela.delta_time())

        #desenha o contador de almas
        alma.draw()
        alma.update()
        janela.draw_text2(str(morte.qtd_almas), 200, 52, resource_path("Fontes/ROCC.ttf"), 25, (255, 255, 255))

        #atualiza flags relacionadas ao tempo
        tempo = janela.delta_time()
        if flag_musica >= 0: flag_musica += 1

        #se o jogador cumpriu os requisitos para seguir em frente, inicializa a proxima fase
        if (morte.current_sprite.x > 1080 and chao[0].x < -2395) and inimigos[0] == [] and inimigos[1] == []:
            funcoes.para_musica()
            fade(1200, 700, janela)
            return fase2_5.inicia(morte.hp, morte.mp, morte.qtd_almas, botoes, volumes, janela)

        #desenha e update sobre o player
        morte.draw()
        morte.update(tempo)
        janela.update()