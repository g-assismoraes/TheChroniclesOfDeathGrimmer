from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.window import *
from PPlay.sound import *
from Geral import *
import math
import random

#para alguns detalhes, ver funcoes1
class Funcoes3_5():

    def __init__(self, janela, volumes):
        self.janela = janela
        self.efeito_vol = volumes[0]
        self.musica_vol = volumes[1]
        self.sons = [Sound(resource_path("Sounds/grito.ogg")), Sound(resource_path("Sounds/corte.ogg"))]
        self.musica = Sound(resource_path("Sounds/mus3_5.ogg"))
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
    
    def desenha_inimigos(self, inimigos):
        [inimigo.current_sprite.draw() for inimigo in inimigos]
    
    def update_inimigos(self, inimigos, tempo):
        [inimigo.update(tempo) for inimigo in inimigos]
    
    def analisa_estimulos(self, morte, chao, botoes, teclado, janela, inimigos, gravidade, normal, ataques):
        if not morte.isMorte_spawning():
            inimigo = inimigos[0][0]

            y=-1
            tempo = janela.delta_time()*(3/4)
            if chao.x <= morte.current_sprite.x+ 3/5*morte.current_sprite.width and \
                morte.current_sprite.x+ 2/5*morte.current_sprite.width <= chao.x + chao.width:
                morte.chao = y = 1
            if y == -1:
                morte.current_sprite.y += 10*(normal+gravidade)*tempo
                gravidade += 100*tempo
                if gravidade < 20:gravidade=20
            else:
                if morte.current_sprite.y+morte.current_sprite.height < chao.y - 1:
                    morte.current_sprite.y += 10 * (normal + gravidade) * tempo
                    gravidade += 100 * tempo
                    if gravidade < 20: gravidade = 20
                elif morte.current_sprite.y + morte.current_sprite.height == chao.y:
                    normal,gravidade = 0,0
                elif chao.y + 3/4*chao.height > morte.current_sprite.y+ morte.current_sprite.height > chao.y:
                    morte.current_sprite.y = -morte.current_sprite.height + chao.y
                else:
                    morte.current_sprite.y += 10 * (normal + gravidade) * tempo
                    gravidade += 100 * tempo
                    if gravidade < 20: gravidade = 20

            if teclado.key_pressed(botoes[3][0]) and gravidade == 0:
                morte.current_sprite.y += -2
                normal= -60

            aux = inimigo.atacar(morte, tempo)

            caes = ataques[2]
            if aux == 2:
                if inimigo.current_sprite.x > 600:
                    caes.append(Cao(inimigo.current_sprite.x + 50, 540, -1, 150))
                    caes.append(Cao(inimigo.current_sprite.x + 50, 540, -1, 100))
                else:
                    caes.append(Cao(inimigo.current_sprite.x + 50, 540, 1, 150))
                    caes.append(Cao(inimigo.current_sprite.x + 50, 540, 1, 100))
            
            for cao in caes:
                dx = (cao.current_sprite.x + cao.current_sprite.width/2) - (morte.current_sprite.x + morte.current_sprite.width/2)
                dy = (cao.current_sprite.y + cao.current_sprite.height/2) - (morte.current_sprite.y + morte.current_sprite.height/2)

                cao.draw()
                cao.update(tempo)

                if cao.sentido == 1:
                    cao.current_sprite.x += cao.vel * tempo
                    cao.atualiza_estado(1)
                else:
                    cao.current_sprite.x -= cao.vel * tempo
                    cao.atualiza_estado(0)
                
                if cao.current_sprite.x < 0: cao.sentido = 1
                if cao.current_sprite.x > 1050: cao.sentido = -1

                if (-75 < dx < 75) and (-50 < dy < 50):
                    if morte.isMorte_attacking() or morte.isMorte_special():
                        caes.remove(cao)
                        morte.atualiza_status("mp", 5)
                        morte.atualiza_status("hp", 2)
                    else:
                        morte.atualiza_status("hp", -cao.dmg * tempo)

            bolas = ataques[1]
            if aux == 3:
                z = 100
                bolas.append(Bola(inimigo.current_sprite.x + z, inimigo.current_sprite.y + z, 0))
                bolas.append(Bola(inimigo.current_sprite.x + z, inimigo.current_sprite.y + z, 60))
                bolas.append(Bola(inimigo.current_sprite.x + z, inimigo.current_sprite.y + z, 120))
                bolas.append(Bola(inimigo.current_sprite.x + z, inimigo.current_sprite.y + z, 180))
                bolas.append(Bola(inimigo.current_sprite.x + z, inimigo.current_sprite.y + z, 240))
                bolas.append(Bola(inimigo.current_sprite.x + z, inimigo.current_sprite.y + z, 300))
            
            for bola in bolas:
                dx = (bola.current_sprite.x + bola.current_sprite.width/2) - (morte.current_sprite.x + morte.current_sprite.width/2)
                dy = (bola.current_sprite.y + bola.current_sprite.height/2) - (morte.current_sprite.y + morte.current_sprite.height/2)

                bola.origem = [inimigo.current_sprite.x + 100, inimigo.current_sprite.y + 100]

                bola.draw()
                bola.update(tempo)

                if bola.destruction <= 0:
                    bolas.remove(bola)

                if (-60 < dx < 60) and (-60 < dy < 60):
                    morte.atualiza_status("hp", - bola.dmg * tempo)

            pilares = ataques[0]
            if aux == 4:
                pilares.append(Pilar(inimigo.current_sprite.x + 50, 0, "e"))
                pilares.append(Pilar(inimigo.current_sprite.x + 50, 0, "d"))
            
            for pilar in pilares:
                d = (pilar.x + pilar.width/2) - (morte.current_sprite.x + morte.current_sprite.width/2)
                pilar.draw()
                pilar.atualiza(tempo)

                if -60 < d < 60 and pilar.estado == 1:
                    morte.atualiza_status("hp", - pilar.dmg)
                    pilar.estado = 0
                
                if pilar.destruction <= 0:
                    pilares.remove(pilar)
        
            
            if not morte.isMorte_natural() and (morte.current_sprite.get_curr_frame() == morte.current_sprite.get_final_frame()-1):
               if morte.estado == "idle_d" or morte.estado == "ataque_d" or morte.estado == "especial_d": morte.atualiza_estado(1)
               else: morte.atualiza_estado(2)

            if teclado.key_pressed(botoes[0][0]) and not (morte.current_sprite.x < -30):
                morte.atualiza_estado(2)
                morte.current_sprite.move_x(-300*tempo)

            elif teclado.key_pressed(botoes[1][0]) and not (morte.current_sprite.x + morte.current_sprite.width > self.janela.width + 30):
                morte.atualiza_estado(1)
                morte.current_sprite.move_x(300*tempo)

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

            if testa_colisao(morte, inimigo):
                inimigo.take_hit(morte)
                if inimigo.amI_attacking():
                    morte.atualiza_status("hp", -inimigo.dmg * tempo)
                if morte.isMorte_attacking():
                    morte.atualiza_status("mp", 5 * tempo)
                if inimigo.hp <= 250:
                    inimigos[0].remove(inimigo)
                    
        else:
            if(morte.current_sprite.get_curr_frame()==21):
                morte.atualiza_estado(1)
       
        return morte, gravidade, normal, ataques

class Rei():
    def __init__(self, x, y):
        self.sprites = self.inicializa_sprites(x, y)
        self.current_sprite = self.sprites[0]
        self.estado = "idle_e"
        self.hp = 3333
        self.dmg = 0
        self.dmg1 = 0
        self.dmg2 = 25
        self.cooldown = 0
        self.strategia = 0
        self.imortalidade = 0
        self.stun = 0
        self.oscilacao = 0
        self.lock = 0
        self.hud = Hud_BOSS(self)
        self.hud.atualiza()

    def inicializa_sprites(self, x, y):
        idle_direita = Sprite(resource_path("Images/Inimigos/Rei da Calamidade/idle_direita.png"), 6)
        idle_esquerda = Sprite(resource_path("Images/Inimigos/Rei da Calamidade/idle_esquerda.png"), 6)
        ataque_esquerda = Sprite(resource_path("Images/Inimigos/Rei da Calamidade/ataque_esquerda.png"), 23)
        ataque_direita = Sprite(resource_path("Images/Inimigos/Rei da Calamidade/ataque_direita.png"), 23)
        idle_direita.set_total_duration(600)
        idle_esquerda.set_total_duration(600)
        ataque_esquerda.set_total_duration(1300)
        ataque_direita.set_total_duration(1300)

        idle_esquerda.set_position(x, y)
        self.origem = [x, y]
        return [idle_esquerda, idle_direita, ataque_esquerda, ataque_direita]
    
    def atualiza_estado(self, index=0):
        if self.estado == ["idle_e", "idle_d", "ataque_e", "ataque_d"][index]: return
        self.sprites[index].set_position(self.current_sprite.x, self.current_sprite.y)
        self.current_sprite = self.sprites[index]
        self.current_sprite.curr_frame = 0
        self.estado = ["idle_e", "idle_d", "ataque_e", "ataque_d"][index]

    def amI_idle(self): return self.estado == "idle_d" or self.estado == "idle_e"

    def amI_attacking(self): return self.estado == "ataque_e" or self.estado == "ataque_d"

    def draw(self):
        self.current_sprite.draw()
    
    def amI_takingHit(self): pass

    def atacar(self, player, tempo):
        d = (self.current_sprite.x + self.current_sprite.width/2) - (player.current_sprite.x + player.current_sprite.width/2)
        xv = 150 * tempo

        if self.strategia == 0:
            aux = random.randint(0, 9)

            if aux in [0, 3, 7, 8]:
                self.strategia = 1
            elif aux in [2, 6, 9]:
                self.strategia = 2
            elif aux in [1, 5]:
                self.strategia = 3
            elif aux in [4]:
                self.strategia = 4
        
        if self.cooldown <= 0:
            if self.strategia == 1:
                if self.current_sprite.y >= 400:
                    if self.current_sprite.x + self.current_sprite.width/2 <= 580:
                        if self.current_sprite.x >= -50 and self.estado != "ataque_d":
                            self.current_sprite.x -= 150 * tempo
                        else:
                            self.atualiza_estado(3)
                            self.current_sprite.x += 250 * tempo
                            self.dmg = self.dmg2
                    elif self.current_sprite.x + self.current_sprite.width/2 >= 620:
                        if self.current_sprite.x <= 1000 and self.estado != "ataque_e":
                            self.current_sprite.x += 150 * tempo
                        else:
                            self.atualiza_estado(2)
                            self.current_sprite.x -= 250 * tempo
                            self.dmg = self.dmg2
                    else:
                        self.cooldown = 7
                        self.strategia = 0
                        self.dmg = self.dmg1
                        if self.estado == "ataque_d": self.atualiza_estado(1)
                        else: self.atualiza_estado(0)     
                else:
                    self.current_sprite.y += 150 * tempo           

                return 1

            if self.strategia == 2:
                if (self.current_sprite.x + self.current_sprite.width/2) > 600:
                    if (395 <= self.current_sprite.y <= 405) and \
                    (1140 <= self.current_sprite.x + self.current_sprite.width/2 <= 1160): 
                        self.strategia = 0
                        self.cooldown = 7
                        return 2
                    else: 
                        if self.current_sprite.y > 405: self.current_sprite.y -= 150 * tempo
                        else: self.current_sprite.y += 150 * tempo

                        if self.current_sprite.x + self.current_sprite.width/2 > 1150: self.current_sprite.x -= 150 * tempo
                        else: self.current_sprite.x += 150 * tempo      
                else:
                    if (395 <= self.current_sprite.y <= 405) and \
                    (90 <= self.current_sprite.x + self.current_sprite.width/2 <= 110): 
                        self.strategia = 0
                        self.cooldown = 7
                        return 2
                    else: 
                        if self.current_sprite.y > 405: self.current_sprite.y -= 150 * tempo
                        else: self.current_sprite.y += 150 * tempo

                        if self.current_sprite.x + self.current_sprite.width/2 > 100: self.current_sprite.x -= 150 * tempo
                        else: self.current_sprite.x += 150 * tempo   

            if self.strategia == 3:
                self.strategia = 0
                self.cooldown = 7
                return 3

            if self.strategia == 4:
                if 375 <= self.current_sprite.y <= 385 and \
                590 <= self.current_sprite.x + self.current_sprite.width/2 <= 610: 
                    self.strategia = 0
                    self.cooldown = 7
                    return 4
                else:
                    if self.current_sprite.y > 380: self.current_sprite.y -= 150 * tempo
                    else: self.current_sprite.y += 150 * tempo

                    if self.current_sprite.x + self.current_sprite.width/2 > 600: self.current_sprite.x -= 150 * tempo
                    else: self.current_sprite.x += 150 * tempo
                

        else:
            if 260 <= self.current_sprite.y - 50*math.sin(math.radians(self.oscilacao)) <= 280:
                if d > 0: self.atualiza_estado(0)
                else: self.atualiza_estado(1)
                if self.lock == 0:
                    self.current_sprite.x -= xv
                    if self.current_sprite.x < 0:
                        self.lock = 1
                if self.lock == 1:
                    self.current_sprite.x += xv
                    if self.current_sprite.x + self.current_sprite.width > 1200:
                        self.lock = 0
                
                self.current_sprite.y = 270 + 50*math.sin(math.radians(self.oscilacao)) 
                self.oscilacao += 200 * tempo
            else:
                if self.current_sprite.y - 50*math.sin(math.radians(self.oscilacao)) > 280: self.current_sprite.y -= 150 * tempo
                else: self.current_sprite.y += 150 * tempo
                

    def take_hit(self, player):
        if self.imortalidade <= 0:
            if player.isMorte_attacking():
                self.hp -= player.dmgFoice
                self.imortalidade = 0.3
                if self.estado == "idle_d" or self.estado == "idle_e":
                    if self.estado in ("idle_d", "ataque_d", "andar_d", "dano_d", "morte_d", "ataque2_d"): self.atualiza_estado(1)
                    else: self.atualiza_estado(0)
                    self.stun = 2
            elif player.isMorte_special():
                self.hp -= player.dmgGrito
                self.imortalidade = 0.3
                if self.estado == "idle_d" or self.estado == "idle_e":
                    if self.estado in ("idle_d", "ataque_d", "andar_d", "dano_d", "morte_d", "ataque2_d"): self.atualiza_estado(1)
                    else: self.atualiza_estado(0)
                    self.stun = 2

    def update(self, tempo):
        if self.cooldown > 0:
            self.cooldown -= tempo
        
        if self.imortalidade > 0:
            self.imortalidade -= tempo
        
        if self.stun > 0:
            self.stun -= tempo

        self.hud.atualiza()
        self.hud.desenha()

        self.current_sprite.update()

class Bola():

    def __init__(self, x, y, delta):
        self.current_sprite = self.inicializa_sprite()
        self.dmg = 25
        self.origem = [x, y]
        self.hp = 1000
        self.oscilacao = delta
        self.destruction = 10
    
    def atacar(self): pass
    
    def inicializa_sprite(self):
        sprite = Sprite(resource_path("Images/Inimigos/Rei da Calamidade/bola de fogo.png"), 3)
        sprite.set_total_duration(500)

        return sprite
    
    def update(self, tempo):

        self.current_sprite.x = self.origem[0] + 150*math.sin(math.radians(self.oscilacao)) 
        self.current_sprite.y = self.origem[1] + 150*math.cos(math.radians(self.oscilacao)) 

        self.oscilacao += 100 * tempo
        self.destruction -= tempo
        self.current_sprite.update()
    
    def draw(self):
        return self.current_sprite.draw()
    
    def take_hit(self, player): return False

    def amI_attacking(self): return True

    def amI_takingHit(self): pass

    def amI_dying(self): pass

class Pilar(Sprite):

    def __init__(self, x, y, flag):
        super().__init__(resource_path("Images/Inimigos/Corrompido/pilar.png"), 2)
        self.set_position(x, y)
        self.set_total_duration(200)
        self.destruction = 6
        self.sentido = flag
        self.estado = 1
        self.dmg = 25
        self.hp = 1000
    
    def atacar(self, player, tempo): pass

    def take_hit(self, player): pass
    
    def atualiza(self, tempo):
        if self.sentido == "d": self.x += 150 * tempo
        else: self.x -= 150 * tempo

        self.destruction -= tempo

        self.update()

class Cao():

    def __init__(self, x, y, sentido, vel):
        self.sprites = self.inicializa_sprites(x, y)
        self.current_sprite = self.sprites[0]
        self.estado = "idle"
        self.dmg = 15
        self.hp = 5
        self.vel = vel
        self.sentido = sentido

    def atacar(self, player, tempo): pass

    def take_hit(self, player): pass
    
    def inicializa_sprites(self, x, y):
        andar_esquerda = Sprite(resource_path("Images/Inimigos/Rei da Calamidade/hell-hound-run_esquerda.png"), 5)
        andar_direita = Sprite(resource_path("Images/Inimigos/Rei da Calamidade/hell-hound-run_direita.png"), 5)
        andar_esquerda.set_position(x, y)
        andar_esquerda.set_total_duration(400)
        andar_direita.set_total_duration(400)
        return [andar_esquerda, andar_direita]
    
    def atualiza_estado(self, index=0):
        if self.estado == ["andar_e", "andar_d"][index]: return
        self.sprites[index].set_position(self.current_sprite.x, self.current_sprite.y)
        self.current_sprite = self.sprites[index]
        self.current_sprite.curr_frame = 0
        self.estado = ["andar_e", "andar_d"][index]

    def draw(self):
        self.current_sprite.draw()

    def update(self, tempo):
        self.current_sprite.update()

class Hud_BOSS():
    def __init__(self, personagem):
        self.personagem = personagem

        self.fundo = GameImage(resource_path("Images/Outras/backplate_aligned.png"))
        self.fundo.set_position(1200 - self.fundo.width, 8)

        self.life = Sprite(resource_path("Images/Outras/lifebar_boss.png"))
        self.life.set_position(1200 - self.life.width, 8)
        self.life_original = 280

        self.foto = GameImage(resource_path("Images/Outras/calamidadeIcon.png"))
        self.foto.set_position(1200 - self.life.width, 8)
    
    def desenha(self):
        self.fundo.draw()
        self.life.draw()
        self.foto.draw()
    
    def atualiza(self):
        if 0 <= self.personagem.hp <= 3333: self.life.width = self.personagem.hp/3333*self.life_original