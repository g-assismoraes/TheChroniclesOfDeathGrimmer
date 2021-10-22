from PPlay.sprite import *
from PPlay.gameimage import *
from PPlay.window import *
from PPlay.sound import *
from Geral import *

#para alguns detalhes, ver funcoes1
class Funcoes2_5():

    def __init__(self, janela, volumes):
        self.janela = janela
        self.efeito_vol = volumes[0]
        self.musica_vol = volumes[1]
        self.sons = [Sound(resource_path("Sounds/grito.ogg")), Sound(resource_path("Sounds/corte.ogg"))]
        self.musica = Sound(resource_path("Sounds/mus2_5.ogg"))
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
    
    def analisa_estimulos(self, morte, chao, botoes, teclado, janela, inimigos, gravidade, normal):
        if not morte.isMorte_spawning():
            y=-1
            tempo = janela.delta_time()
            fator = 1.8
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
            
            inimigos[0][0].atacar(morte, tempo)

            if teclado.key_pressed(botoes[3][0]) and gravidade == 0:
                morte.current_sprite.y += -2
                normal= -60
            
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

            inimigo = inimigos[0][0]
            if testa_colisao(morte, inimigo):
                inimigo.take_hit(morte)
                if inimigo.amI_attacking():
                    morte.atualiza_status("hp", -inimigo.dmg * tempo * fator)
                if morte.isMorte_attacking():
                    morte.atualiza_status("mp", 5 * tempo)
                if inimigo.hp <= 140:
                    if inimigo.estado in ("idle_d", "ataque_d", "andar_d", "dano_d", "morte_d", "ataque2_d"): inimigo.atualiza_estado(9)
                    else: inimigo.atualiza_estado(8)

            if inimigo.amI_dying() and inimigo.current_sprite.get_curr_frame() == inimigo.current_sprite.get_final_frame()-1:
                inimigos[0].remove(inimigo)
                morte.qtd_almas += 1
                    
        else:
            if(morte.current_sprite.get_curr_frame()==21):
                morte.atualiza_estado(1)
       
        return morte, gravidade, normal


class Rei():
    def __init__(self, x, y):
        self.sprites = self.inicializa_sprites(x, y)
        self.current_sprite = self.sprites[0]
        self.estado = "idle_e"
        self.hp = 2000
        self.dmg = 0
        self.dmg1 = 7
        self.dmg2 = 150
        self.cooldown = 0
        self.strategia = 0
        self.imortalidade = 0
        self.stun = 0
        self.hud = Hud_BOSS(self)
        self.hud.atualiza()
    
    def inicializa_sprites(self, x, y):
        idle_esquerda = Sprite(resource_path("Images/Inimigos/Rei/Idle_esquerda.png"), 8)
        idle_direira = Sprite(resource_path("Images/Inimigos/Rei/Idle_direita.png"), 8)
        ataque1_esquerda = Sprite(resource_path("Images/Inimigos/Rei/ataque1_esquerda.png"), 12)
        ataque1_direita = Sprite(resource_path("Images/Inimigos/Rei/ataque1_direita.png"), 12)
        ataque2_esquerda = Sprite(resource_path("Images/Inimigos/Rei/ataque2_esquerda.png"), 15)
        ataque2_direita = Sprite(resource_path("Images/Inimigos/Rei/ataque2_direita.png"), 15)
        andar_esquerda = Sprite(resource_path("Images/Inimigos/Rei/corre_esquerda.png"), 8)
        andar_direita = Sprite(resource_path("Images/Inimigos/Rei/corre_direita.png"), 8)
        dano_esquerda = Sprite(resource_path("Images/Inimigos/Rei/takehit_esquerda.png"), 4)
        dano_direita = Sprite(resource_path("Images/Inimigos/Rei/takehit_direita.png"), 4)
        morte_esquerda = Sprite(resource_path("Images/Inimigos/Rei/morte_esquerda.png"), 6)
        morte_direita = Sprite(resource_path("Images/Inimigos/Rei/morte_direita.png"), 6)
        idle_esquerda.set_total_duration(800)
        idle_direira.set_total_duration(800)
        ataque1_esquerda.set_total_duration(1500)
        ataque1_direita.set_total_duration(1500)     
        ataque2_esquerda.set_total_duration(1200)
        ataque2_direita.set_total_duration(1200)   
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

    def atacar(self, player, tempo):
        d = (self.current_sprite.x + self.current_sprite.width/2) - (player.current_sprite.x + player.current_sprite.width/2)

        if self.cooldown <= 0 and self.stun <= 0:
            if self.strategia < 3:
                if d > 0:
                    if d >= 20:
                        self.atualiza_estado(4)
                        self.current_sprite.x -= 150 * tempo
                    else:
                        self.atualiza_estado(10)
                        self.dmg = self.dmg1
                        self.cooldown = 2
                        self.strategia += 1
                else:
                    if d <= -20:
                        self.atualiza_estado(5)
                        self.current_sprite.x += 150 * tempo
                    else:
                        self.atualiza_estado(11)
                        self.dmg = self.dmg1
                        self.cooldown = 2
                        self.strategia += 1

            else:
                if self.current_sprite.x + self.current_sprite.width/2 <= 590:
                    if self.current_sprite.x >= -100 and self.estado != "ataque_d":
                        self.atualiza_estado(4)
                        self.current_sprite.x -= 150 * tempo
                    else:
                        self.atualiza_estado(3)
                        self.current_sprite.x += 600 * tempo
                        self.dmg = self.dmg2
                elif self.current_sprite.x + self.current_sprite.width/2 >= 610:
                    if self.current_sprite.x <= 1000 and self.estado != "ataque_e":
                        self.atualiza_estado(5)
                        self.current_sprite.x += 150 * tempo
                    else:
                        self.atualiza_estado(2)
                        self.current_sprite.x -= 600 * tempo
                        self.dmg = self.dmg2
                else:
                    self.cooldown = 2
                    self.strategia = 0
                    if self.estado == "ataque_d": self.atualiza_estado(1)
                    else: self.atualiza_estado(0)
        
        return 0
 

    def take_hit(self, player):
        if self.imortalidade <= 0:
            if player.isMorte_attacking():
                self.hp -= player.dmgFoice
                self.imortalidade = 0.3
                if self.estado == "idle_d" or self.estado == "idle_e":
                    if self.estado in ("idle_d", "ataque_d", "andar_d", "dano_d", "morte_d", "ataque2_d"): self.atualiza_estado(7)
                    else: self.atualiza_estado(6)
                    self.stun = 2
            elif player.isMorte_special():
                self.hp -= player.dmgGrito
                self.imortalidade = 0.3
                if self.estado == "idle_d" or self.estado == "idle_e":
                    if self.estado in ("idle_d", "ataque_d", "andar_d", "dano_d", "morte_d", "ataque2_d"): self.atualiza_estado(7)
                    else: self.atualiza_estado(6)
                    self.stun = 2

    def atualiza_estado(self, index=0):
        if self.estado == ["idle_e", "idle_d", "ataque_e", "ataque_d", "andar_e", "andar_d", "dano_e", "dano_d", "morte_e", "morte_d", "ataque2_e", "ataque2_d"][index]: return
        self.sprites[index].set_position(self.current_sprite.x, self.current_sprite.y)
        self.current_sprite = self.sprites[index]
        self.current_sprite.curr_frame = 0
        self.estado = ["idle_e", "idle_d", "ataque_e", "ataque_d", "andar_e", "andar_d", "dano_e", "dano_d", "morte_e", "morte_d",\
            "ataque2_e", "ataque2_d"][index]

    def amI_idle(self): return self.estado == "idle_e" or self.estado == "idle_d"

    def amI_attacking(self): return self.estado == "ataque_d" or self.estado == "ataque_e" or self.estado == "ataque2_e" or self.estado == "ataque2_d"

    def amI_walking(self): return self.estado == "andar_d" or self.estado == "andar_e"

    def amI_takingHit(self): return self.estado == "dano_d" or self.estado == "dado_e"

    def amI_dying(self): return self.estado == "morte_d" or self.estado == "morte_e"

    def draw(self):
        self.current_sprite.draw()
    
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

class Hud_BOSS():
    def __init__(self, personagem):
        self.personagem = personagem

        self.fundo = GameImage(resource_path("Images/Outras/backplate_aligned.png"))
        self.fundo.set_position(1200 - self.fundo.width, 8)

        self.life = Sprite(resource_path("Images/Outras/lifebar_boss.png"))
        self.life.set_position(1200 - self.life.width, 8)
        self.life_original = 280

        self.foto = GameImage(resource_path("Images/Outras/reiIcon.png"))
        self.foto.set_position(1200 - self.life.width, 8)
    
    def desenha(self):
        self.fundo.draw()
        self.life.draw()
        self.foto.draw()
    
    def atualiza(self):
        if 0 <= self.personagem.hp <= 2000: self.life.width = self.personagem.hp/2000*self.life_original