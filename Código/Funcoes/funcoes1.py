from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.window import*
from PPlay.sound import *
from Geral import *

class Funcoes1():

    #inicializa parametros importantes para o controle da fase posteriormente, principalmente musicais
    def __init__(self, janela, volumes):
        self.janela = janela
        self.efeito_vol = volumes[0]
        self.musica_vol = volumes[1]
        self.sons = [Sound(resource_path("Sounds/grito.ogg")), Sound(resource_path("Sounds/corte.ogg"))]
        self.musica = Sound(resource_path("Sounds/mus1.ogg"))
        self.musica.set_repeat(True)
        self.atualiza_efeitos(self.efeito_vol)
        self.atualiza_musicas(self.musica_vol)

    #funcoes relacionadas a musica
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

    #inicializa gameimages dos blocos de chao em suas devidas posicoes
    def inicializa_chao(self):
        chao = [GameImage(resource_path("Images/Mapas/recortes/recorte1_"+str(x+1)+".png")) for x in range(7)]
        pos_chao=[[0,self.janela.height-chao[0].height],[355,self.janela.height-chao[1].height],
                [2049,self.janela.height-chao[2].height],[2482,self.janela.height-63],
                [2629,self.janela.height-63],[2776,self.janela.height-63],
                [2923,self.janela.height-chao[6].height]]

        for x in range(len(chao)):
            chao[x].set_position(pos_chao[x][0],pos_chao[x][1])
    
        return chao
    
    #inicializa as camadas de fundo, para que sejam usadas na ideia de movimentação
    def inicializa_fundo(self):
        background=[0,0,0,0,0]
        background2=[0,0,0,0,0]
        background3=[0,0,0,0,0]
        for x in range(len(background)):
            background[x] = GameImage(resource_path("Images/Background/Fase 1/background" + str(x + 1) + ".png"))
            background[x].set_position(-background[x].width, self.janela.height - background[x].height)
            background2[x] = GameImage(resource_path("Images/Background/Fase 1/background" + str(x + 1) + ".png"))
            background2[x].set_position(self.janela.width - background[x].width, self.janela.height - background[x].height)
            background3[x] = GameImage(resource_path("Images/Background/Fase 1/background" + str(x + 1) + ".png"))
            background3[x].set_position(background[x].width, self.janela.height - background[x].height)
        
        return background, background2, background3
    
    #desenha o fundo
    def draw_fundo(self, background, background2, background3):
        for x in range(len(background)):
            background[x].draw()
            background2[x].draw()
            background3[x].draw()

    
    #atualiza o fundo quando necessario (pós alteraçao da posicao devido a ideia de velocidade)
    def atualiza_fundo(self, background, background2, background3):
        for x in range(1,len(background)):
            if background[x].x >= 0:
                background[x].x -= background[x].width
                background2[x].x -= background2[x].width
                background3[x].x -= background3[x].width
            elif background3[x].x <= self.janela.width-background3[x].width:
                background[x].x += background[x].width
                background2[x].x += background2[x].width
                background3[x].x += background3[x].width
    
    #corrige os inimigos a se mexerem juntamente ao seu respectivo solo, ao encontro da movimentacao de tela
    def corrige_eixoInimigos(self, inimigos, correcao):
        for inimigo in inimigos:
            inimigo.current_sprite.x = inimigo.origem[0] + correcao
    
    # desenha um vetor de inimigos
    def desenha_inimigos(self, inimigos):
        [inimigo.current_sprite.draw() for inimigo in inimigos]
    
    #updata um vetor de inimigos
    def update_inimigos(self, inimigos, tempo):
        [inimigo.update(tempo) for inimigo in inimigos]
    
    #retorna o chao para a posicao inicial
    def reinicia_chao(self, chao):

        pos_chao=[[0,self.janela.height-chao[0].height],[355,self.janela.height-chao[1].height],
                [2049,self.janela.height-chao[2].height],[2482,self.janela.height-63],
                [2629,self.janela.height-63],[2776,self.janela.height-63],
                [2923,self.janela.height-chao[6].height]]

        for x in range(len(chao)):
            chao[x].set_position(pos_chao[x][0],pos_chao[x][1])
    
    #funcao que dita o fluxo logico de cada loop, atualizando todas as variaveis e personagens do jogo
    def analisa_estimulos(self, morte, chao, chao_colisivo, botoes, teclado, janela, background, background2, background3, inimigos, move_tela, gravidade, normal):
        if not morte.isMorte_spawning():
            #simulaçao de gravidade
            y=-1
            tempo = janela.delta_time()
            for x in range(len(chao_colisivo)):
                if chao_colisivo[x].x <= morte.current_sprite.x+ 3/5*morte.current_sprite.width and \
                    morte.current_sprite.x+ 2/5*morte.current_sprite.width <= chao_colisivo[x].x + chao_colisivo[x].width:
                    morte.chao = y = x
                    break
            if y == -1:
                morte.current_sprite.y += 10*(normal+gravidade)*tempo
                gravidade += 100*tempo
                if gravidade < 20: gravidade = 20
            else:
                if morte.current_sprite.y+morte.current_sprite.height < chao_colisivo[y].y - 1:
                    morte.current_sprite.y += 10 * (normal + gravidade) * tempo
                    gravidade += 100 * tempo
                    if gravidade < 20: gravidade = 20
                elif morte.current_sprite.y+morte.current_sprite.height == chao_colisivo[y].y:
                    normal,gravidade = 0, 0
                elif chao_colisivo[y].y + 3/4*chao_colisivo[y].height > morte.current_sprite.y+ morte.current_sprite.height > chao_colisivo[y].y:
                    morte.current_sprite.y = -morte.current_sprite.height + chao_colisivo[y].y
                else:
                    morte.current_sprite.y += 10 * (normal + gravidade) * tempo
                    gravidade += 100 * tempo
                    if gravidade < 20: gravidade = 20
            
            #pulo
            if teclado.key_pressed(botoes[3][0]) and gravidade == 0:
                morte.current_sprite.y += -2
                normal= -60

            #checa as acoes para os inimigos de cada classe
            for hiena in inimigos[0]:
                if y == hiena.chao:
                    hiena.atacar(morte, tempo)
                elif hiena.amI_walking() or hiena.amI_takingHit():
                    if hiena.estado == "andar_d" or hiena.estado == "dano_d": hiena.atualiza_estado(1)
                    else: hiena.atualiza_estado(0)
            
            for elfo in inimigos[1]:
                aux = elfo.atacar(morte, tempo)
                if aux == 1:
                    flecha = Flecha('e', elfo.origem[0])
                    flecha.current_sprite.set_position(elfo.current_sprite.x, elfo.current_sprite.y + elfo.current_sprite.height/3)
                    inimigos[2].append(flecha)  
                elif aux == 2:
                    flecha = Flecha('d', elfo.origem[0] + elfo.current_sprite.width*2/3)
                    flecha.current_sprite.set_position(elfo.current_sprite.x + elfo.current_sprite.width*2/3, elfo.current_sprite.y + elfo.current_sprite.height/3)
                    inimigos[2].append(flecha)
                
                elif elfo.amI_attacking() and elfo.fire_rate <= 0:
                    if elfo.estado == "ataque_d" or elfo.estado == "dano_d": elfo.atualiza_estado(1)
                    else: elfo.atualiza_estado(0)
            
            if not morte.isMorte_natural() and (morte.current_sprite.get_curr_frame() == morte.current_sprite.get_final_frame()-1):
               if morte.estado == "idle_d" or morte.estado == "ataque_d" or morte.estado == "especial_d": morte.atualiza_estado(1)
               else: morte.atualiza_estado(2)

            #movimentacao para os lados
            if teclado.key_pressed(botoes[0][0]):
                morte.atualiza_estado(2)
                if morte.current_sprite.x > 200:
                    morte.current_sprite.move_x(-300*tempo)
                elif chao_colisivo[0].x <= -10:
                    for i in range(len(chao)):
                        chao[i].x += 400 * tempo
                    for x in range(len(chao_colisivo)):
                        chao_colisivo[x].x += 400 * tempo
                    morte.current_sprite.x += 0.1
                elif morte.current_sprite.x > -10:
                    morte.current_sprite.move_x(-300*tempo)
                if morte.current_sprite.x < 200 and chao_colisivo[0].x <= -10:
                    for x in range(1, len(background)):
                        background[x].x += move_tela
                        background2[x].x += move_tela
                        background3[x].x += move_tela
                        move_tela += 0.3
                    move_tela = 0.3

            elif teclado.key_pressed(botoes[1][0]) and not (morte.current_sprite.x > 1000 and chao[0].x < -2675):
                morte.atualiza_estado(1)
                if janela.width - morte.current_sprite.x > 300:
                    morte.current_sprite.move_x(300*tempo)
                elif chao_colisivo[len(chao_colisivo) - 1].x + chao_colisivo[len(chao_colisivo) - 1].width >= janela.width + 1:
                    for i in range(len(chao)):
                        chao[i].x -= 400 * tempo
                    for x in range(len(chao_colisivo)):
                        chao_colisivo[x].x -= 400 * tempo
                    morte.current_sprite.x -= 0.1
                elif morte.current_sprite.x < janela.width:
                    morte.current_sprite.move_x(300*tempo)
                if morte.current_sprite.x > 900 and chao_colisivo[len(chao_colisivo) - 1].x + chao_colisivo[len(chao_colisivo) - 1].width\
                     >= janela.width + 1:
                    for x in range(1, len(background)):
                        background[x].x -= move_tela
                        background2[x].x -= move_tela
                        background3[x].x -= move_tela
                        move_tela += 0.3
                    move_tela = 0.3

            #ataque basico
            if teclado.key_pressed(botoes[2][0]):
                if morte.ataque_cooldown <= 0:
                    self.sons[1].play()
                    self.sons[1].fadeout(400)
                    if morte.estado == "idle_d" or morte.estado == "ataque_d" or morte.estado == "especial_d":
                        morte.atualiza_estado(3)
                    else: morte.atualiza_estado(4)
                    morte.ataque_cooldown = 1

            #ataque especial
            if teclado.key_pressed(botoes[4][0]) and morte.mp >= 68:
                if morte.grito_cooldown <= 0:
                    self.sons[0].play()
                    self.sons[0].fadeout(600)

                    morte.atualiza_status("mp", -16)

                    if morte.estado == "idle_d" or morte.estado == "especial_d" or morte.estado == "ataque_d":
                        morte.atualiza_estado(5)
                    else: morte.atualiza_estado(6)

                    morte.grito_cooldown = 1.5
            
            #cura
            if teclado.key_pressed(botoes[5][0]) and morte.mp > 56.8 and 14 < morte.hp < 100:
                if morte.recover_cooldown <= 0:
                    morte.atualiza_status("hp", 17.2)
                    morte.atualiza_status("mp", -4.8)

                    morte.recover_cooldown = 2 

            #checa o dano dos inimigos sobre o player e os efeitos das acoes do player sobre os inimigos
            for grupo in inimigos:
                for inimigo in grupo:
                    if testa_colisao(morte, inimigo):
                        inimigo.take_hit(morte)
                        if inimigo.amI_attacking():
                            morte.atualiza_status("hp", -inimigo.dmg * tempo)
                            if grupo == inimigos[2]:
                                grupo.remove(inimigo)
                                break
                        if morte.isMorte_attacking():
                            morte.atualiza_status("mp", 5 * tempo)
                        if inimigo.hp <= 0:
                            if inimigo.estado in ("idle_d", "ataque_d", "andar_d", "dano_d", "morte_d"):
                                inimigo.atualiza_estado(9)
                            else: inimigo.atualiza_estado(8)

                    if inimigo.amI_dying() and inimigo.current_sprite.get_curr_frame() == inimigo.current_sprite.get_final_frame()-1\
                        and grupo != inimigos[2]:
                        grupo.remove(inimigo)
                        morte.qtd_almas += 1
                        break

                    if grupo == inimigos[2]:
                        if -10 > inimigo.current_sprite.x > 4000:
                            grupo.remove(inimigo)

        else:
            if(morte.current_sprite.get_curr_frame()==21):
                morte.atualiza_estado(1)
   
        return morte, move_tela, gravidade, normal

class Hiena():
    def __init__(self, x, y, chao):
        self.sprites = self.inicializa_sprites(x, y)
        self.current_sprite = self.sprites[0]
        self.estado = "idle"
        self.dmg = 2
        self.hp = 100
        self.chao = chao
        self.origem = [x, y]
        self.stun = 0

    def atacar(self, player, tempo):
        d = (self.current_sprite.x + self.current_sprite.width/2) - (player.current_sprite.x + player.current_sprite.width/2)

        if self.stun <= 0:
            if d > 0:
                if d >= 20:
                    self.atualiza_estado(4)
                    self.origem[0] -= 100 * tempo
                else:
                    self.atualiza_estado(2)
            else:
                if d <= -20:
                    self.atualiza_estado(5)
                    self.origem[0] += 100 * tempo
                else:
                    self.atualiza_estado(3)
        return 0

    
    def take_hit(self, player):
        if self.stun <= 0:
            if player.isMorte_attacking():
                self.hp -= player.dmgFoice
                self.stun = 0.6
                if self.estado == "ataque_e" or self.estado == "andar_e": self.atualiza_estado(6)
                else: self.atualiza_estado(7)
            elif player.isMorte_special():
                self.hp -= player.dmgGrito
                self.stun = 2.5
                if self.estado == "ataque_e" or self.estado == "andar_e": self.atualiza_estado(6)
                else: self.atualiza_estado(7)
    
    def inicializa_sprites(self, x, y):
        idle_esquerda = Sprite(resource_path("Images/Inimigos/Hiena/idle_esquerda.png"), 4)
        idle_direira = Sprite(resource_path("Images/Inimigos/Hiena/idle_direita.png"), 4)
        ataque_esquerda = Sprite(resource_path("Images/Inimigos/Hiena/ataque_esquerda.png"), 7)
        ataque_direita = Sprite(resource_path("Images/Inimigos/Hiena/ataque_direita.png"), 7)
        andar_esquerda = Sprite(resource_path("Images/Inimigos/Hiena/andar_esquerda.png"), 6)
        andar_direita = Sprite(resource_path("Images/Inimigos/Hiena/andar_direita.png"), 6)
        dano_esquerda = Sprite(resource_path("Images/Inimigos/Hiena/dano_esquerda.png"), 2)
        dano_direita = Sprite(resource_path("Images/Inimigos/Hiena/dano_direita.png"), 2)
        morte_esquerda = Sprite(resource_path("Images/Inimigos/Hiena/morte_esquerda.png"), 6)
        morte_direita = Sprite(resource_path("Images/Inimigos/Hiena/morte_direita.png"), 6)
        idle_esquerda.set_total_duration(600)
        idle_direira.set_total_duration(600)
        ataque_esquerda.set_total_duration(600)
        ataque_direita.set_total_duration(600)   
        andar_esquerda.set_total_duration(600)
        andar_direita.set_total_duration(600)
        dano_esquerda.set_total_duration(200)
        dano_direita.set_total_duration(200)
        morte_direita.set_total_duration(600)
        morte_esquerda.set_total_duration(600)
        idle_esquerda.set_position(x, y)
        return [idle_esquerda, idle_direira, ataque_esquerda, ataque_direita, andar_esquerda, andar_direita, dano_esquerda, dano_direita,\
            morte_esquerda, morte_direita]
    
    def atualiza_estado(self, index=0):
        if self.estado == ["idle_e", "idle_d", "ataque_e", "ataque_d", "andar_e", "andar_d", "dano_e", "dano_d", "morte_e", "morte_d"][index]: return
        self.sprites[index].set_position(self.current_sprite.x, self.current_sprite.y)
        self.current_sprite = self.sprites[index]
        self.current_sprite.curr_frame = 0
        self.estado = ["idle_e", "idle_d", "ataque_e", "ataque_d", "andar_e", "andar_d", "dano_e", "dano_d", "morte_e", "morte_d"][index]

    def amI_idle(self): return self.estado == "idle"

    def amI_attacking(self): return self.estado == "ataque_d" or self.estado == "ataque_e"

    def amI_walking(self): return self.estado == "andar_d" or self.estado == "andar_e"

    def amI_takingHit(self): return self.estado == "dano_d" or self.estado == "dano_e"

    def amI_dying(self): return self.estado == "morte_e" or self.estado == "morte_d"

    def draw(self):
        self.current_sprite.draw()

    def update(self, tempo):
        if self.stun > 0:
            self.stun -= tempo
        self.current_sprite.update()

class Elfo():
    def __init__(self, x, y):
        self.sprites = self.inicializa_sprites(x, y)
        self.current_sprite = self.sprites[0]
        self.estado = "idle"
        self.hp = 100
        self.stun = 0
        self.dmg = 2
        self.fire_rate = 0
    
    def inicializa_sprites(self, x, y):
        idle_esquerda = Sprite(resource_path("Images/Inimigos/Arqueiro/Idle_esquerda.png"), 10)
        idle_direira = Sprite(resource_path("Images/Inimigos/Arqueiro/Idle_direita.png"), 10)
        ataque_esquerda = Sprite(resource_path("Images/Inimigos/Arqueiro/ataque_esquerda.png"), 6)
        ataque_direita = Sprite(resource_path("Images/Inimigos/Arqueiro/ataque_direita.png"), 6)
        andar_esquerda = Sprite(resource_path("Images/Inimigos/Arqueiro/correr_esquerda.png"), 8)
        andar_direita = Sprite(resource_path("Images/Inimigos/Arqueiro/correr_direita.png"), 8)
        dano_esquerda = Sprite(resource_path("Images/Inimigos/Arqueiro/takehit_esquerda.png"), 3)
        dano_direita = Sprite(resource_path("Images/Inimigos/Arqueiro/takehit_direita.png"), 3)
        morte_esquerda = Sprite(resource_path("Images/Inimigos/Arqueiro/morte_esquerda.png"), 10)
        morte_direita = Sprite(resource_path("Images/Inimigos/Arqueiro/morte_direita.png"), 10)
        idle_esquerda.set_total_duration(800)
        idle_direira.set_total_duration(800)
        ataque_esquerda.set_total_duration(2000)
        ataque_direita.set_total_duration(2000)   
        andar_esquerda.set_total_duration(600)
        andar_direita.set_total_duration(600)
        dano_esquerda.set_total_duration(600)
        dano_direita.set_total_duration(600)
        morte_direita.set_total_duration(600)
        morte_esquerda.set_total_duration(600)
        idle_esquerda.set_position(x, y)
        self.origem = [x, y]
        return [idle_esquerda, idle_direira, ataque_esquerda, ataque_direita, andar_esquerda, andar_direita, dano_esquerda, dano_direita,\
            morte_esquerda, morte_direita]
    
    def atacar(self, player, tempo):
        d = (self.current_sprite.x + self.current_sprite.width/2) - (player.current_sprite.x + player.current_sprite.width/2)

        if self.stun <= 0 and -375 < d < 375 and self.fire_rate <= 0:
            if d > 0:
                self.atualiza_estado(2)
                self.fire_rate = 2
                return 1
            else:
                self.atualiza_estado(3)
                self.fire_rate = 2
                return 2
        
        return 0

    def take_hit(self, player):
        if self.stun <= 0:
            if player.isMorte_attacking():
                self.hp -= player.dmgFoice
                self.stun = 0.6
                if self.estado == "ataque_e" or self.estado == "andar_e": self.atualiza_estado(6)
                else: self.atualiza_estado(7)
            elif player.isMorte_special():
                self.hp -= player.dmgGrito
                self.stun = 2.5
                if self.estado == "ataque_e" or self.estado == "andar_e": self.atualiza_estado(6)
                else: self.atualiza_estado(7)
    
    def atualiza_estado(self, index=0):
        if self.estado == ["idle_e", "idle_d", "ataque_e", "ataque_d", "andar", "andar", "dano_e", "dano_d", "morte_e", "morte_d"][index]: return
        self.sprites[index].set_position(self.current_sprite.x, self.current_sprite.y)
        self.current_sprite = self.sprites[index]
        self.current_sprite.curr_frame = 0
        self.estado = ["idle_e", "idle_d", "ataque_e", "ataque_d", "andar", "andar", "dano_e", "dano_d", "morte_e", "morte_d"][index]

    def amI_idle(self): return self.estado == "idle"

    def amI_attacking(self): return self.estado == "ataque_d" or self.estado == "ataque_e"

    def amI_walking(self): return self.estado == "andar_d" or self.estado == "andar_e"

    def amI_takingHit(self): return self.estado == "dano_d" or self.estado == "dano_e"

    def amI_dying(self): return self.estado == "morte_e" or self.estado == "morte_d"

    def draw(self):
        self.current_sprite.draw()

    def update(self, tempo):
        if self.stun > 0:
            self.stun -= tempo
        if self.fire_rate > 0:
            self.fire_rate -= tempo

        self.current_sprite.update()

class Flecha():
    def __init__(self, flag, x):
        self.current_sprite = self.inicializa_sprite(flag)
        self.dmg = 200
        self.sentido = flag
        self.origem = [x]
        self.hp = 10
    
    def atacar(self): pass
    
    def inicializa_sprite(self, flag):
        if flag == "e": sprite = Sprite(resource_path("Images/Inimigos/Arqueiro/flecha_esquerda.png"), 2)
        elif flag == "d": sprite = Sprite(resource_path("Images/Inimigos/Arqueiro/flecha_direita.png"), 2)
        sprite.set_total_duration(800)

        return sprite
    
    def update(self, tempo):
        if self.sentido == "e":
            self.origem[0] -= 120*tempo
        elif self.sentido == "d": self.origem[0] += 120*tempo

        self.current_sprite.update()
    
    def draw(self):
        return self.current_sprite.draw()
    
    def take_hit(self, player): return False

    def amI_takingHit(self): pass
    
    def amI_attacking(self): return True

    def amI_dying(self): pass

