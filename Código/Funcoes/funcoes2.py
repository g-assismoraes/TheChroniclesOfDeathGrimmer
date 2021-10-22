from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.window import *
from PPlay.sound import *
from Geral import *

#para alguns detalhes, ver funcoes1
class Funcoes2():

    def __init__(self, janela, volumes):
        self.janela = janela
        self.efeito_vol = volumes[0]
        self.musica_vol = volumes[1]
        self.sons = [Sound(resource_path("Sounds/grito.ogg")), Sound(resource_path("Sounds/corte.ogg"))]
        self.musica = Sound(resource_path("Sounds/mus2.ogg"))
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

    def inicializa_chao(self):
        chao = GameImage(resource_path("Images/Mapas/mapa2/chao.png"))
        chao.set_position(0, self.janela.height-chao.height)

        return chao

    def inicializa_fundo(self):
    
        background=[0,0,0,0,0,0]
        for x in [0,1,2,3,4,5]:
            background[x] = GameImage(resource_path("Images/Background/Fase 2/fundo castelo.png"))
            background[x].set_position(0, 0)
        
        return background
    
    def draw_fundo(self, background):
        for x in range(len(background)):
            background[x].draw()
    
    def atualiza_fundo(self, background, chao):
        for x in range(1,len(background)):
            background[x].x = chao.x
    
    def corrige_eixoInimigos(self, inimigos, correcao):
        for inimigo in inimigos:
            inimigo.current_sprite.x = inimigo.origem[0] + correcao
    
    def desenha_inimigos(self, inimigos):
        [inimigo.current_sprite.draw() for inimigo in inimigos]
    
    def update_inimigos(self, inimigos, tempo):
        [inimigo.update(tempo) for inimigo in inimigos]
    
    def analisa_estimulos(self, morte, chao, chao_colisivo, botoes, teclado, janela, background, inimigos, move_tela, gravidade, normal):
        if not morte.isMorte_spawning():
            y=-1
            tempo = janela.delta_time()*(3/4)
            
            for x in range(len(chao_colisivo)):
                if chao_colisivo[x].x <= morte.current_sprite.x+ 3/5*morte.current_sprite.width and \
                    morte.current_sprite.x+ 2/5*morte.current_sprite.width <= chao_colisivo[x].x + chao_colisivo[x].width:
                    morte.chao = y = x
                    break
            if y == -1:
                morte.current_sprite.y += 10*(normal+gravidade)*tempo
                gravidade += 100*tempo
                if gravidade < 20:gravidade=20
            else:
                if morte.current_sprite.y+morte.current_sprite.height < chao_colisivo[y].y - 1:
                    morte.current_sprite.y += 10 * (normal + gravidade) * tempo
                    gravidade += 100 * tempo
                    if gravidade < 20: gravidade = 20
                elif morte.current_sprite.y+morte.current_sprite.height == chao_colisivo[y].y:
                    normal,gravidade = 0,0
                elif chao_colisivo[y].y + 3/4*chao_colisivo[y].height > morte.current_sprite.y+ morte.current_sprite.height > chao_colisivo[y].y:
                    morte.current_sprite.y = -morte.current_sprite.height + chao_colisivo[y].y
                else:
                    morte.current_sprite.y += 10 * (normal + gravidade) * tempo
                    gravidade += 100 * tempo
                    if gravidade < 20: gravidade = 20

            if teclado.key_pressed(botoes[3][0]) and gravidade == 0:
                morte.current_sprite.y += -2
                normal= -60

            for cavaleiro in inimigos[0]:
                if y == cavaleiro.chao:
                    cavaleiro.atacar(morte, tempo)
                elif cavaleiro.amI_walking() or cavaleiro.amI_takingHit():
                    if cavaleiro.estado == "andar_d" or cavaleiro.estado == "dano_d": cavaleiro.atualiza_estado(1)
                    else: cavaleiro.atualiza_estado(0)
            
            for lanceira in inimigos[1]:
                aux = lanceira.atacar(morte, tempo, y)
                if aux == 1:
                    lanca = Lanca('e', lanceira.origem[0])
                    lanca.current_sprite.set_position(lanceira.current_sprite.x, lanceira.current_sprite.y + lanceira.current_sprite.height/3)
                    inimigos[2].append(lanca)  
                elif aux == 2:
                    lanca = Lanca('d', lanceira.origem[0] + lanceira.current_sprite.width*2/3)
                    lanca.current_sprite.set_position(lanceira.current_sprite.x + lanceira.current_sprite.width*2/3, lanceira.current_sprite.y + lanceira.current_sprite.height/3)
                    inimigos[2].append(lanca)
                
                elif (lanceira.amI_walking() and aux != 3) or (lanceira.amI_attacking() and lanceira.fire_rate <= 0 and aux != 4):
                    if lanceira.estado in ["ataque_d", "dano_d", "andar_d", "longo_d"]: lanceira.atualiza_estado(1)
                    else: lanceira.atualiza_estado(0)
            
            if not morte.isMorte_natural() and (morte.current_sprite.get_curr_frame() == morte.current_sprite.get_final_frame()-1):
               if morte.estado == "idle_d" or morte.estado == "ataque_d" or morte.estado == "especial_d": morte.atualiza_estado(1)
               else: morte.atualiza_estado(2)

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
                        move_tela += 0.3
                    move_tela = 0.3

            elif teclado.key_pressed(botoes[1][0]) and not (morte.current_sprite.x > 1080 and chao[0].x < -2395):
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
                        move_tela += 0.3
                    move_tela = 0.3
            
            if teclado.key_pressed(botoes[2][0]):
                if morte.ataque_cooldown <= 0:
                    self.sons[1].play()
                    self.sons[1].fadeout(400)
                    if morte.estado == "idle_d" or morte.estado == "ataque_d" or morte.estado == "especial_d":
                        morte.atualiza_estado(3)
                    else: morte.atualiza_estado(4)
                    morte.ataque_cooldown = 1

            if teclado.key_pressed(botoes[4][0]) and morte.mp >= 68:
                if morte.grito_cooldown <= 0:
                    self.sons[0].play()
                    self.sons[0].fadeout(600)

                    morte.atualiza_status("mp", -16)

                    if morte.estado == "idle_d" or morte.estado == "especial_d" or morte.estado == "ataque_d":
                        morte.atualiza_estado(5)
                    else: morte.atualiza_estado(6)

                    morte.grito_cooldown = 1.5
            
            if teclado.key_pressed(botoes[5][0]) and morte.mp > 56.8 and 14 < morte.hp < 100:
                if morte.recover_cooldown <= 0:
                    morte.atualiza_status("hp", 17.2)
                    morte.atualiza_status("mp", -4.8)

                    morte.recover_cooldown = 2          

            for grupo in inimigos:
                for inimigo in grupo:
                    if testa_colisao(morte, inimigo):
                        inimigo.take_hit(morte)
                        if inimigo.amI_attacking():
                            morte.atualiza_status("hp", -inimigo.dmg * tempo)
                            if grupo == inimigos[2]:
                                grupo.remove(inimigo)
                                break
                        elif morte.isMorte_attacking():
                            morte.atualiza_status("mp", 5 * tempo)
                        if inimigo.hp <= 0:
                            if inimigo.estado in ("idle_d", "ataque_d", "andar_d", "dano_d", "morte_d", "longo_d", "ataque2_d"):
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

class Cavaleiro():
    def __init__(self, x, y, chao):
        self.sprites = self.inicializa_sprites(x, y)
        self.current_sprite = self.sprites[0]
        self.estado = "idle_e"
        self.hp = 200
        self.dmg = 5
        self.chao = chao
        self.stun = 0
        self.origem = [x, y]
        self.excesso = self.sprites[1].width
    
    def inicializa_sprites(self, x, y):
        idle_esquerda = Sprite(resource_path("Images/Inimigos/Cavaleiro/idle_esquerda.png"), 3)
        idle_direira = Sprite(resource_path("Images/Inimigos/Cavaleiro/idle_direita.png"), 3)
        ataque_esquerda = Sprite(resource_path("Images/Inimigos/Cavaleiro/ataque_esquerda.png"), 6)
        ataque_direita = Sprite(resource_path("Images/Inimigos/Cavaleiro/ataque_direita.png"), 6)
        andar_esquerda = Sprite(resource_path("Images/Inimigos/Cavaleiro/andar_esquerda.png"), 6)
        andar_direita = Sprite(resource_path("Images/Inimigos/Cavaleiro/andar_direita.png"), 6)
        dano_esquerda = Sprite(resource_path("Images/Inimigos/Cavaleiro/takehit_esquerda.png"), 3)
        dano_direita = Sprite(resource_path("Images/Inimigos/Cavaleiro/takehit_direita.png"), 3)
        morte_esquerda = Sprite(resource_path("Images/Inimigos/Cavaleiro/morte_esquerda.png"), 5)
        morte_direita = Sprite(resource_path("Images/Inimigos/Cavaleiro/morte_direita.png"), 5)
        idle_esquerda.set_total_duration(550)
        idle_direira.set_total_duration(550)
        ataque_esquerda.set_total_duration(750)
        ataque_direita.set_total_duration(750)   
        andar_esquerda.set_total_duration(600)
        andar_direita.set_total_duration(600)
        dano_esquerda.set_total_duration(600)
        dano_direita.set_total_duration(600)
        morte_direita.set_total_duration(600)
        morte_esquerda.set_total_duration(600)
        idle_esquerda.set_position(x, y)
        return [idle_esquerda, idle_direira, ataque_esquerda, ataque_direita, andar_esquerda, andar_direita, dano_esquerda, dano_direita,\
            morte_esquerda, morte_direita]
    

    def atacar(self, player, tempo):
        d = (self.current_sprite.x + self.current_sprite.width/2) - (player.current_sprite.x + player.current_sprite.width/2)

        if self.stun <= 0:
            if d > 0:
                if d >= 20:
                    self.atualiza_estado(4)
                    self.origem[0] -= 90 * tempo
                else:
                    self.atualiza_estado(2)
            else:
                if d <= -20:
                    self.atualiza_estado(5)
                    self.origem[0] += 90 * tempo
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

    def atualiza_estado(self, index=0):
        if self.estado == ["idle_e", "idle_d", "ataque_e", "ataque_d", "andar_e", "andar_d", "dano_e", "dano_d", "morte_e", "morte_d"][index]: return 
        self.sprites[index].set_position(self.origem[0], self.origem[1])
        self.current_sprite = self.sprites[index]
        self.current_sprite.curr_frame = 0
        self.estado = ["idle_e", "idle_d", "ataque_e", "ataque_d", "andar_e", "andar_d", "dano_e", "dano_d", "morte_e", "morte_d"][index]

    def amI_idle(self): return self.estado == "idle_d" or self.estado == "idle_e"  

    def amI_attacking(self): return self.estado == "ataque_d" or self.estado == "ataque_e"

    def amI_walking(self): return self.estado == "andar_d" or self.estado == "andar_e"

    def amI_takingHit(self): return self.estado == "dano_d" or self.estado == "dano_e"

    def amI_dying(self): return self.estado == "morte_d" or self.estado == "morte_e"

    def draw(self):
        self.current_sprite.draw()

    def update(self, tempo):
        if self.stun > 0:
            self.stun -= tempo
        self.current_sprite.update()
    
class Lanceira():
    def __init__(self, x, y, chao):
        self.sprites = self.inicializa_sprites(x, y)
        self.current_sprite = self.sprites[0]
        self.estado = "idle_e"
        self.hp = 150
        self.dmg = 5
        self.stun = 0
        self.fire_rate = 0
        self.chao = chao

    def atacar(self, player, tempo, chao): 
        d = (self.current_sprite.x + self.current_sprite.width/2) - (player.current_sprite.x + player.current_sprite.width/2)

        if self.stun <= 0 and (-375 < d < -200 or 200 < d < 375) and self.fire_rate <= 0:
            if d > 0:
                self.atualiza_estado(10)
                self.fire_rate = 2
                return 1
            else:
                self.atualiza_estado(11)
                self.fire_rate = 2
                return 2

        elif self.stun <= 0 and self.chao == chao and -200 < d < 200:
            self.fire_rate = 0
            if d > 0:
                if d >= 30:
                    self.atualiza_estado(4)
                    self.origem[0] -= 100 * tempo
                else:
                    self.atualiza_estado(2)
                    return 4
            else:
                if d <= -30:
                    self.atualiza_estado(5)
                    self.origem[0] += 100 * tempo
                else:
                    self.atualiza_estado(3)
                    return 4

            return 3
        
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
        idle_esquerda = Sprite(resource_path("Images/Inimigos/Lanceira/Idle_esquerda.png"), 8)
        idle_direira = Sprite(resource_path("Images/Inimigos/Lanceira/Idle_direita.png"), 8)
        ataque1_esquerda = Sprite(resource_path("Images/Inimigos/Lanceira/ataque_esquerda.png"), 5)
        ataque1_direita = Sprite(resource_path("Images/Inimigos/Lanceira/ataque_direita.png"), 5)
        ataque2_esquerda = Sprite(resource_path("Images/Inimigos/Lanceira/ataque2_esquerda.png"), 7)
        ataque2_direita = Sprite(resource_path("Images/Inimigos/Lanceira/ataque2_direita.png"), 7)
        andar_esquerda = Sprite(resource_path("Images/Inimigos/Lanceira/correr_esquerda.png"), 8)
        andar_direita = Sprite(resource_path("Images/Inimigos/Lanceira/correr_direita.png"), 8)
        dano_esquerda = Sprite(resource_path("Images/Inimigos/Lanceira/takehit_esquerda.png"), 3)
        dano_direita = Sprite(resource_path("Images/Inimigos/Lanceira/takehit_direita.png"), 3)
        morte_esquerda = Sprite(resource_path("Images/Inimigos/Lanceira/morte_esquerda.png"), 8)
        morte_direita = Sprite(resource_path("Images/Inimigos/Lanceira/morte_direita.png"), 8)
        idle_esquerda.set_total_duration(500)
        idle_direira.set_total_duration(500)
        ataque1_esquerda.set_total_duration(600)
        ataque1_direita.set_total_duration(600)     
        ataque2_esquerda.set_total_duration(1800)
        ataque2_direita.set_total_duration(1800) 
        andar_esquerda.set_total_duration(600)
        andar_direita.set_total_duration(600)
        dano_esquerda.set_total_duration(600)
        dano_direita.set_total_duration(600)
        morte_direita.set_total_duration(600)
        morte_esquerda.set_total_duration(600)
        idle_esquerda.set_position(x, y)
        self.origem = [x, y]
        return [idle_esquerda, idle_direira, ataque1_esquerda, ataque1_direita, andar_esquerda,\
             andar_direita, dano_esquerda, dano_direita, morte_esquerda, morte_direita, ataque2_esquerda, ataque2_direita]
    
    def atualiza_estado(self, index=0):
        if self.estado == ["idle_e", "idle_d", "ataque_e", "ataque_d", "andar_e", "andar_d", "dano_e", "dano_d", "morte_e", "morte_d",\
            "longo_e", "longo_d"][index]: return
        self.sprites[index].set_position(self.current_sprite.x, self.current_sprite.y)
        self.current_sprite = self.sprites[index]
        self.current_sprite.curr_frame = 0
        self.estado = ["idle_e", "idle_d", "ataque_e", "ataque_d", "andar_e", "andar_d", "dano_e", "dano_d", "morte_e", "morte_d",\
            "longo_e", "longo_d"][index]

    def amI_idle(self): return self.estado == "idle_e" or self.estado == "idle_d"

    def amI_attacking(self): return self.estado == "ataque_d" or self.estado == "ataque_e" or self.estado == "longo_e" or self.estado == "longo_d"

    def amI_walking(self): return self.estado == "andar_d" or self.estado == "andar_e"

    def amI_takingHit(self): return self.estado == "dano_d" or self.estado == "dado_e"

    def amI_dying(self): return self.estado == "morte_d" or self.estado == "morte_e"

    def draw(self):
        self.current_sprite.draw()

    def update(self, tempo):
        if self.stun > 0:
            self.stun -= tempo
        if self.fire_rate > 0:
            self.fire_rate -= tempo

        self.current_sprite.update()

class Lanca():
    def __init__(self, flag, x):
        self.current_sprite = self.inicializa_sprite(flag)
        self.dmg = 300
        self.sentido = flag
        self.origem = [x]
        self.hp = 10
    
    def atacar(self): pass
    
    def inicializa_sprite(self, flag):
        if flag == "e": sprite = Sprite(resource_path("Images/Inimigos/Lanceira/lança_esquerda.png"), 4)
        elif flag == "d": sprite = Sprite(resource_path("Images/Inimigos/Lanceira/lança_direita.png"), 4)
        sprite.set_total_duration(500)

        return sprite
    
    def update(self, tempo):
        if self.sentido == "e":
            self.origem[0] -= 120*tempo
        elif self.sentido == "d": self.origem[0] += 120*tempo

        self.current_sprite.update()
    
    def draw(self):
        return self.current_sprite.draw()
    
    def take_hit(self, player): return False

    def amI_attacking(self): return True

    def amI_takingHit(self): pass

    def amI_dying(self): pass