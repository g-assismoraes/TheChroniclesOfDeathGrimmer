from PPlay.window import *
from PPlay.sprite import *
from PPlay.gameimage import *
from Funcoes.funcoes1 import *
from Geral import *
from Funcoes.exibir import *

def inicia(hp, mp, qtd_almas, botoes, volumes, janela):
    teclado = Window.get_keyboard()

    funcoes = Funcoes1(janela, volumes)

    morte = Morte(hp, mp, qtd_almas)

    botoes = botoes

    alma = Alma(153, 25)

    move_tela = 0.3

    chao = funcoes.inicializa_chao()

    #aqui se inicializam os blocos de imagem que serao utilizados para tratamento de colisao para com o chao
    chao_colisivo = [GameImage(resource_path("Images/Mapas/recortes/recorte_chao"+str(x+1)+".png")) for x in range(12)]
    pos_chao=[[0,janela.height-chao_colisivo[0].height],[355,janela.height-chao_colisivo[1].height],
              [706,janela.height-chao_colisivo[2].height],[1009,janela.height-chao_colisivo[3].height],
              [1344,janela.height-chao_colisivo[4].height],[1582,janela.height-chao_colisivo[5].height],
              [2049,janela.height-chao_colisivo[6].height],[2482,janela.height-chao_colisivo[6].height],
              [2629,janela.height-chao_colisivo[6].height],[2776,janela.height-chao_colisivo[6].height],
              [2923,janela.height-chao_colisivo[10].height],[3337,janela.height-chao_colisivo[11].height]]
    
    for x in range(len(chao_colisivo)):
        chao_colisivo[x].set_position(pos_chao[x][0],pos_chao[x][1])

    background, background2, background3 = funcoes.inicializa_fundo()
    
    #inicializacao dos inimigos
    hienas = [0 for _ in range (4)]
    infoHiena=[[466, 560, 1],[765, 513, 2],[1125, 560, 3], [1750, 560, 5]]
    for i in range(len(hienas)): hienas[i] = Hiena(infoHiena[i][0], infoHiena[i][1], infoHiena[i][2])

    elfos = [0 for _ in range (3)]
    posicaoElfos =[[2130, 500], [2900, 500], [3450, 470]]
    for i in range(len(elfos)): elfos[i] = Elfo(posicaoElfos[i][0], posicaoElfos[i][1])
    flechas = []
    
    inimigos = [hienas, elfos, flechas]

    #inicializacao de parametros para a gravidade
    gravidade, normal = 0, 0

    #inicializacao de parametros de controle
    lock_almas = 0
    flag_musica = 0

    #game loop principal da fase 1
    while True:

        #inicializaca a musica da fase
        if flag_musica > 3:
            funcoes.toca_musica()
            flag_musica = -10

        #controla se o player atingiu o necessario para seguir para a proxima fase
        if morte.current_sprite.x > 1000 and chao[0].x < -2675:
            if morte.qtd_almas >= 5:
                volumes = funcoes.para_musica()
                fade(1200, 700, janela)
                return 1, morte.hp, morte.mp, morte.qtd_almas, janela, botoes, volumes

        #desenha o background
        funcoes.draw_fundo(background, background2, background3)

        #exibe o aviso de insuficiencia de condicoes para passar de fase, caso esse seja o caso
        if morte.current_sprite.x > 1000 and morte.qtd_almas < 5: 
            janela.draw_text2("Almas insuficientes!", 960, 455, resource_path("Fontes/ROCC.ttf"), 30, (250, 250, 250))

        #desenha o chao com adereços
        for x in range(len(chao)):
            chao[x].draw()

        #corrige o fundo devido aos efeitos de movimentaçao 
        funcoes.atualiza_fundo(background, background2, background3)

        #atualiza as variaveis que devem ser atualizadas a cada loop
        morte, move_tela, gravidade, normal = funcoes.analisa_estimulos(morte, chao, chao_colisivo, botoes, teclado, \
            janela, background, background2, background3, inimigos, move_tela, gravidade, normal)

        #avalia se foi solicitado a abertura do menu/pause
        if teclado.key_pressed('q'):
            botoes = menu_ajustes(botoes, funcoes, teclado, janela)
        
        #draw e update para os inimigos
        for grupo in inimigos:
            funcoes.corrige_eixoInimigos(grupo, chao[0].x)
            funcoes.desenha_inimigos(grupo)
            funcoes.update_inimigos(grupo, janela.delta_time())

        #desenha na tela o contador de almas
        alma.draw()
        alma.update()
        janela.draw_text2(str(morte.qtd_almas), 200, 52, resource_path("Fontes/ROCC.ttf"), 25, (255, 255, 255))
        
        #reinicia a fase caso o jogador morra por dano ou queda
        if morte.current_sprite.y > janela.height or morte.hp <= 14:
            morte.tentativa += 1
            volumes = funcoes.para_musica()
            return inicia(100, 100, morte.almas_salvas, botoes, volumes, janela)

        #atualizacao das flags ligadas ao tempo
        tempo = janela.delta_time()

        lock_almas += tempo

        if flag_musica >= 0: flag_musica += 1

        #desenha e atualiza o jogador
        morte.draw()
        morte.update(tempo)

        #exibe o aviso para o jogador obter informaçoes iniciais com a placa se o mesmo estiver no alcance
        if morte.chao == 0 and 152 <= morte.current_sprite.x <= 176:
            janela.draw_text2("Pressione Z", 165, 486, resource_path("Fontes/ROCC.ttf"), 30, (250, 250, 250))
            if teclado.key_pressed("z"):
                exibe_ensinaControles(janela, teclado)
        
        #update da tela
        janela.update()