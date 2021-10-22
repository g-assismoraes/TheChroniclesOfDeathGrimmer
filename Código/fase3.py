from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from Funcoes.funcoes3 import *
from Funcoes.exibir import *
from Geral import *
import fase3_5

def inicia(hp, mp, qtd_almas, botoes, volumes, janela):
    #inicializacao similar as das fases anteriores

    teclado = Window.get_keyboard()
    funcoes = Funcoes3(janela, volumes)

    morte = Morte(hp, mp, qtd_almas, botoes)

    alma = Alma(153, 25)

    move_tela = 0.3
    botoes=botoes 

    chao = funcoes.inicializa_chao()

    chao_colisivo = [GameImage(resource_path("Images/Mapas/recortes/recorte_final" + str(x + 1) + ".png")) for x in range(10)]
    pos_chao = [[0, janela.height - chao_colisivo[0].height], [356, janela.height - chao_colisivo[1].height],
                [700, janela.height - chao_colisivo[2].height], [1012, janela.height - chao_colisivo[3].height - 65],
                [1385, janela.height - chao_colisivo[4].height - 75], [1980, janela.height - chao_colisivo[5].height - 90],
                [2250, janela.height - chao_colisivo[6].height - 90], [2450, janela.height - chao_colisivo[7].height - 90],
                [2800, janela.height - chao_colisivo[8].height - 90], [3100, janela.height - chao_colisivo[9].height]]
    for x in range(10):
        chao_colisivo[x].set_position(pos_chao[x][0],pos_chao[x][1])

    background, background2, background3 = funcoes.inicializa_fundo()
    
    corrompidos = [0 for _ in range (3)]
    posicaoCorromp=[[350, 160],[2000, 160],[1270, 160]]
    for i in range(len(corrompidos)): corrompidos[i] = Corrompido(posicaoCorromp[i][0], posicaoCorromp[i][1])

    servos = [0 for _ in range (3)]
    posicaoServos=[[1700, 400],[2540, 323],[1000, 410]]
    for i in range(len(servos)): servos[i] = Servo(posicaoServos[i][0], posicaoServos[i][1])

    bolas = []
    pilares = []

    inimigos = [corrompidos, servos, bolas]

    gravidade, normal = 0, 0

    flag_musica = 0

    while True:
        #inicializa musica
        if flag_musica > 3:
            funcoes.toca_musica()
            flag_musica = -10
        
        #checa se o inimigo morreu por dano ou queda para reiniciar a fase
        if morte.current_sprite.y > janela.height or morte.hp <= 14:
            volumes = funcoes.para_musica()
            return inicia(100, 100, morte.almas_salvas, botoes, volumes, janela)

        #desenha o fundo
        funcoes.draw_fundo(background, background2, background3)
        
        #desenha o chao
        for x in range(len(chao)):
            chao[x].draw()

        #atualiza o fundo
        funcoes.atualiza_fundo(background, background2, background3)

        #atualiza parametros necessarios de se renovar a cada loop
        morte, move_tela, gravidade, normal, pilares = funcoes.analisa_estimulos(morte, chao, chao_colisivo, botoes, teclado, \
            janela, background, background2, background3, inimigos, move_tela, gravidade, normal, pilares)

        #checa se foi solicitada a abertura do menu/pause
        if teclado.key_pressed('q'):
            botoes = menu_ajustes(botoes, funcoes, teclado, janela)

        #desenha inimigos
        for grupo in inimigos:
            funcoes.corrige_eixoInimigos(grupo, chao[0].x)
            funcoes.desenha_inimigos(grupo)
            funcoes.update_inimigos(grupo, janela.delta_time())

        
        #desenha contador de almas
        alma.draw()
        alma.update()
        janela.draw_text2(str(morte.qtd_almas), 200, 52, resource_path("Fontes/ROCC.ttf"), 25, (255, 255, 255))

        #checa se o player atingiu a condicao necessaria para ir a proxima fase
        if morte.current_sprite.x > 1070 and chao[0].x < -2900:
            volumes = funcoes.para_musica()
            fade(1200, 700, janela)
            return fase3_5.inicia(morte.hp, morte.mp, morte.qtd_almas, botoes, volumes,  janela)

        #atualiza flags relacionadas ao tempo
        tempo = janela.delta_time()
        if flag_musica >= 0: flag_musica += 1

        #desenha e atualiza o jogador
        morte.draw()
        morte.update(tempo)

        janela.update()

    return 3, morte.hp, morte.mp, morte.qtd_almas, janela, botoes, volumes