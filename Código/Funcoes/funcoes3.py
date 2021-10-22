from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.window import *
from PPlay.sound import *
from Geral import *
import math

#para alguns detalhes, ver funcoes1
class Funcoes3():

    def __init__(self, janela, volumes):
        self.janela = janela
        self.efeito_vol = volumes[0]
        self.musica_vol = volumes[1]
        self.sons = [Sound(resource_path("Sounds/grito.ogg")), Sound(resource_path("Sounds/corte.ogg"))]
        self.musica = Sound(resource_path("Sounds/mus3.ogg"))
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
        chao = [GameImage(resource_path("Images/Mapas/recortes/recorte_final" + str(x + 1) + "A.png")) for x in range(10)]
        pos_chao = [[0, self.janela.height - chao[0].height], [356, self.janela.height - chao[1].height],
                [700, self.janela.height - chao[2].height], [1012, self.janela.height - chao[3].height-65],
                [1385, self.janela.height - chao[4].height-75], [1980, self.janela.height - chao[5].height-90],
                [2250, self.janela.height - chao[6].height-90], [2450, self.janela.height - chao[7].height-90],
                [2800, self.janela.height - chao[8].height-90], [3100, self.janela.height - chao[9].height]]
        
        for x in range(len(chao)):
            chao[x].set_position(pos_chao[x][0],pos_chao[x][1])
    
        return chao
    
    def reinicia_chao(self, chao):
        pos_chao = [[0, self.janela.height - chao[0].height], [356, self.janela.height - chao[1].height],
                [700, self.janela.height - chao[2].height], [1012, self.janela.height - chao[3].height-55],
                [1385, self.janela.height - chao[4].height-75], [1980, self.janela.height - chao[5].height-90],
                [2250, self.janela.height - chao[6].height-90], [2500, self.janela.height - chao[7].height-152],
                [2800, self.janela.height - chao[8].height-90], [3100, self.janela.height - chao[9].height]]
        
        for x in range(len(chao)):
            chao[x].set_position(pos_chao[x][0],pos_chao[x][1])

    def analisa_estimulos(self, morte, chao, chao_colisivo, botoes, teclado, janela, background, background2, background3, inimigos, move_tela, gravidade, normal, pilares):
        if not morte.isMorte_spawning():
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

            for corrompido in inimigos[0]:
                aux = corrompido.atacar(morte, tempo)

                if aux == 1:
                    pilares.append(Pilar(corrompido.current_sprite.x - 50, 0))
                    inimigos[0].remove(corrompido)
            
            for pilar in pilares:
                d = (pilar.x + pilar.width/2) - (morte.current_sprite.x + morte.current_sprite.width/2)
                pilar.draw()
                pilar.atualiza(tempo)

                if -60 < d < 60:
                    morte.atualiza_status("hp", - pilar.dmg * tempo)
                
                if pilar.destruction <= 0:
                    pilares.remove(pilar)


            for servo in inimigos[1]:
                aux = servo.atacar(morte, tempo)
                if aux == 1:
                    bola = Bola('e', servo.origem[0], servo.origem[1])
                    bola.current_sprite.set_position(servo.current_sprite.x, servo.current_sprite.y + servo.current_sprite.height/3)
                    inimigos[2].append(bola)  
                elif aux == 2:
                    bola = Bola('d', servo.origem[0] + servo.current_sprite.width*2/3, servo.origem[1])
                    bola.current_sprite.set_position(servo.current_sprite.x + servo.current_sprite.width*2/3, servo.current_sprite.y + servo.current_sprite.height/3)
                    inimigos[2].append(bola)
                
                elif servo.amI_attacking() and servo.fire_rate <= 0:
                    if servo.estado == "ataque_d": servo.atualiza_estado(1)
                    else: servo.atualiza_estado(0)

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
                        background2[x].x += move_tela
                        background3[x].x += move_tela
                        move_tela += 0.3
                    move_tela = 0.3

            elif teclado.key_pressed(botoes[1][0]) and not (morte.current_sprite.x > 1070 and chao[0].x < -2900):
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

            if teclado.key_pressed(botoes[2][0]):
                if morte.ataque_cooldown <= 0:
                    self.sons[1].play()
                    self.sons[1].fadeout(400)
                    if morte.estado == "idle_d" or morte.estado == "ataque_d" or morte.estado == "especial_d":
                        morte.atualiza_estado(3)
                    else: morte.atualiza_estado(4)
                    morte.ataque_cooldown = 1
            
            if teclado.key_pressed(botoes[4][0]) and morte.mp > 68:
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
                            grupo.remove(inimigo)
                            break

                    if grupo == inimigos[2]:
                        if -10 > inimigo.current_sprite.x > 4000:
                            grupo.remove(inimigo)

        else:
            if(morte.current_sprite.get_curr_frame()==21):
                morte.atualiza_estado(1)

        return morte, move_tela, gravidade, normal, pilares
    
    def inicializa_fundo(self):
        background=[0,0,0,0,0,0]
        background2=[0,0,0,0,0,0]
        background3=[0,0,0,0,0,0]
        for x in range(len(background)):
            background[x] = GameImage(resource_path("Images/Background/Fase 3/background" + str(x + 1) + ".png"))
            background[x].set_position(-background[x].width, self.janela.height - background[x].height)
            background2[x] = GameImage(resource_path("Images/Background/Fase 3/background" + str(x + 1) + ".png"))
            background2[x].set_position(self.janela.width - background[x].width, self.janela.height - background[x].height)
            background3[x] = GameImage(resource_path("Images/Background/Fase 3/background" + str(x + 1) + ".png"))
            background3[x].set_position(background[x].width, self.janela.height - background[x].height)
        
        return background, background2, background3
    
    def draw_fundo(self, background, background2, background3):
        for x in range(len(background)):
            background[x].draw()
            background2[x].draw()
            background3[x].draw()
    
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
    
    
    def corrige_eixoInimigos(self, inimigos, correcao):
        for inimigo in inimigos:
            inimigo.current_sprite.x = inimigo.origem[0] + correcao
    
    def desenha_inimigos(self, inimigos):
        [inimigo.current_sprite.draw() for inimigo in inimigos]
    
    def update_inimigos(self, inimigos, tempo):
        [inimigo.update(tempo) for inimigo in inimigos]
        
class Corrompido():
    def __init__(self, x, y): 
        self.sprites = self.inicializa_sprites(x, y)
        self.current_sprite = self.sprites[0]
        self.estado = "idle_e"
        self.hp = 1
        self.dmg = 5
        self.stun = 0
        self.oscilacao = 1

    def inicializa_sprites(self, x, y):
        idle_e = Sprite(resource_path("Images/Inimigos/Corrompido/idle_e.png"), 8)
        idle_d = Sprite(resource_path("Images/Inimigos/Corrompido/idle_d.png"), 8)
        ataque_e = Sprite(resource_path("Images/Inimigos/Corrompido/ataque_e.png"), 8)
        ataque_d = Sprite(resource_path("Images/Inimigos/Corrompido/ataque_d.png"), 8)
        dano_e = Sprite(resource_path("Images/Inimigos/Corrompido/dano_e.png"), 4)
        dano_d = Sprite(resource_path("Images/Inimigos/Corrompido/dano_d.png"), 4)
        idle_e.set_total_duration(800)
        idle_d.set_total_duration(800)
        ataque_e.set_total_duration(800)
        ataque_d.set_total_duration(800)
        dano_e.set_total_duration(600)
        dano_d.set_total_duration(600)
        idle_e.set_position(x, y)
        self.origem = [x, y]
        return [idle_e, idle_d, ataque_e, ataque_d, dano_e, dano_d]

    def atacar(self, player, tempo):
        d = (self.current_sprite.x + self.current_sprite.width/2) - (player.current_sprite.x + player.current_sprite.width/2)
        
        if self.stun <= 0 and -375 < d < 375:
            if self.origem[1] < player.current_sprite.y:
                self.origem[1] += 100 * tempo
            else:
                self.origem[1] -= 100 * tempo

            if d > 0:
                if d >= 10:
                    self.atualiza_estado(0)
                elif -30 < self.current_sprite.y - player.current_sprite.y < 30:
                    self.atualiza_estado(2)
                    return 1
                self.origem[0] -= 100 * tempo
            else:
                if d <= -10:
                    self.atualiza_estado(1)
                elif -30 < self.current_sprite.y - player.current_sprite.y < 30:
                    self.atualiza_estado(3)
                    return 1
                self.origem[0] += 100 * tempo

        return 0

    def take_hit(self, player):
        if self.stun <= 0:
            if player.isMorte_attacking():
                self.hp -= player.dmgFoice
                self.stun = 1
                if self.estado == "ataque_e" or self.estado == "andar_e": self.atualiza_estado(4)
                else: self.atualiza_estado(5)
            elif player.isMorte_special():
                self.hp -= player.dmgGrito
                self.stun = 3
                if self.estado == "ataque_e" or self.estado == "andar_e": self.atualiza_estado(4)
                else: self.atualiza_estado(5)

    def atualiza_estado(self, index=0):
        if self.estado == ["idle_e", "idle_d", "ataque_e", "ataque_d", "dano_e", "dano_d"][index]: return
        self.sprites[index].set_position(self.current_sprite.x, self.current_sprite.y)
        self.current_sprite = self.sprites[index]
        self.current_sprite.curr_frame = 0
        self.estado = ["idle_e", "idle_d", "ataque_e", "ataque_d", "dano_e", "dano_d"][index]

    def amI_idle(self): return self.estado == "idle_e" or self.estado == "idle_d"

    def amI_attacking(self): return self.estado == "ataque_e" or self.estado == "ataque_d"

    def amI_takingHit(self): return self.estado == "dano_e" or self.estado == "dano_d"

    def draw(self):
        self.current_sprite.draw()

    def update(self, tempo):
        if self.stun > 0:
            self.stun -= tempo
        
        self.current_sprite.y = self.origem[1] + 50*math.sin(math.radians(self.oscilacao)) 
        self.oscilacao += 200* tempo
        self.current_sprite.update()

class Servo():
    def __init__(self, x, y): 
        self.sprites = self.inicializa_sprites(x, y)
        self.current_sprite = self.sprites[0]
        self.estado = "idle_e"
        self.hp = 100
        self.dmg = 5
        self.stun = 0
        self.fire_rate = 0
    
    def inicializa_sprites(self, x, y):
        idle_direita = Sprite(resource_path("Images/Inimigos/Servo da Calamidade/idle_direita.png"), 6)
        idle_esquerda = Sprite(resource_path("Images/Inimigos/Servo da Calamidade/idle_esquerda.png"), 6)
        ataca_direita = Sprite(resource_path("Images/Inimigos/Servo da Calamidade/ataca_direita.png"), 4)
        ataca_esquerda = Sprite(resource_path("Images/Inimigos/Servo da Calamidade/ataca_esquerda.png"), 4)
        idle_direita.set_total_duration(600)
        idle_esquerda.set_total_duration(600)
        ataca_direita.set_total_duration(2800)
        ataca_esquerda.set_total_duration(2800)

        idle_esquerda.set_position(x, y)
        self.origem = [x, y]
        return [idle_esquerda, idle_direita, ataca_esquerda, ataca_direita]
    
    def atualiza_estado(self, index=0):
        if self.estado == ["idle_e", "idle_d", "ataque_e", "ataque_d"][index]: return
        self.sprites[index].set_position(self.current_sprite.x, self.current_sprite.y)
        self.current_sprite = self.sprites[index]
        self.current_sprite.curr_frame = 0
        self.estado = ["idle_e", "idle_d", "ataque_e", "ataque_d"][index]
    
    def take_hit(self, player):
        if self.stun <= 0:
            if player.isMorte_attacking():
                self.hp -= player.dmgFoice
                self.stun = 0.6
                if self.estado == "ataque_e": self.atualiza_estado(0)
                else: self.atualiza_estado(1)
            elif player.isMorte_special():
                self.hp -= player.dmgGrito
                self.stun = 2.5
                if self.estado == "ataque_e": self.atualiza_estado(0)
                else: self.atualiza_estado(1)

    def atacar(self, player, tempo):
        d = (self.current_sprite.x + self.current_sprite.width/2) - (player.current_sprite.x + player.current_sprite.width/2)

        if self.stun <= 0 and -375 < d < 375 and self.fire_rate <= 0:
            if d > 0:
                self.atualiza_estado(2)
                self.fire_rate = 2.5
                return 1
            else:
                self.atualiza_estado(3)
                self.fire_rate = 2.5
                return 2
        
        return 0

    def amI_idle(self): return self.estado == "idle_e" or self.estado == "idle_d"

    def amI_attacking(self): return self.estado == "ataque_e" or self.estado == "ataque_d"

    def amI_takingHit(self): return self.amI_idle()

    def draw(self):
        self.current_sprite.draw()

    def update(self, tempo):
        if self.stun > 0:
            self.stun -= tempo
        if self.fire_rate > 0:
            self.fire_rate -= tempo

        self.current_sprite.update()


class Bola():

    def __init__(self, flag, x, y):
        self.current_sprite = self.inicializa_sprite(flag)
        self.dmg = 140
        self.sentido = flag
        self.origem = [x, y]
        self.hp = 10
        self.oscilacao = 1
    
    def atacar(self): pass
    
    def inicializa_sprite(self, flag):
        if flag == "e": sprite = Sprite(resource_path("Images/Inimigos/Servo da Calamidade/bola_esquerda.png"), 3)
        elif flag == "d": sprite = Sprite(resource_path("Images/Inimigos/Servo da Calamidade/bola_direita.png"), 3)
        sprite.set_total_duration(500)

        return sprite
    
    def update(self, tempo):
        if self.sentido == "e":
            self.origem[0] -= 120*tempo
        elif self.sentido == "d": self.origem[0] += 120*tempo

        self.current_sprite.y = self.origem[1] + 100*math.sin(math.radians(self.oscilacao)) 
        self.oscilacao += 100 * tempo
        self.current_sprite.update()
    
    def draw(self):
        return self.current_sprite.draw()
    
    def take_hit(self, player): return False

    def amI_attacking(self): return True

    def amI_takingHit(self): pass

    def amI_dying(self): pass

class Pilar(Sprite):

    def __init__(self, x, y):
        super().__init__(resource_path("Images/Inimigos/Corrompido/pilar.png"), 2)
        self.set_position(x, y)
        self.set_total_duration(200)
        self.destruction = 3
        self.dmg = 200
        self.hp = 1000
    
    def atacar(self, player, tempo): pass

    def take_hit(self, player): pass
    
    def atualiza(self, tempo):
        self.destruction -= tempo
        self.update()