from PPlay import sprite
from PPlay.sprite import *
from PPlay.gameimage import *
import os
import sys

#essa função esta relacionada a criacao do arquivo .exe final
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#metodo utilizado para testar colisao
def testa_colisao(invididuo1, individuo2):
    return invididuo1.current_sprite.x + invididuo1.current_sprite.width*3/5 > individuo2.current_sprite.x + 2/5*individuo2.current_sprite.width\
    and invididuo1.current_sprite.x + invididuo1.current_sprite.width*2/5 < individuo2.current_sprite.x + 3/5*individuo2.current_sprite.width\
    and invididuo1.current_sprite.y + invididuo1.current_sprite.height*4/5 > individuo2.current_sprite.y + 1/5*individuo2.current_sprite.height\
    and invididuo1.current_sprite.y + invididuo1.current_sprite.height*1/5 < individuo2.current_sprite.y + 4/5*individuo2.current_sprite.height


#classe que controla os dados e exibicao do HUD do jogador
class Hud():
    def __init__(self, personagem):
        self.personagem = personagem

        self.fundo = GameImage(resource_path("Images/Outras/backplate_aligned.png"))
        self.fundo.set_position(7, 8)

        self.life = Sprite(resource_path("Images/Outras/bar_left_aligned.png"))
        self.life.set_position(7, 8)
        self.life_original = 150

        self.mana = Sprite(resource_path("Images/Outras/bar_right_aligned.png"))
        self.mana.set_position(7, 8)
        self.mana_original = 280

        self.foto = GameImage(resource_path("Images/Outras/fotinha.png"))
        self.foto.set_position(7, 8)
    
    def desenha(self):
        self.fundo.draw()
        self.life.draw()
        self.mana.draw()
        self.foto.draw()
    
    def atualiza(self):
        if 0 <= self.personagem.hp <= 100: self.life.width = self.personagem.hp/100*self.life_original
        if 52 <= self.personagem.mp <= 100: self.mana.width = self.personagem.mp/100*self.mana_original


#classe do player
class Morte():
    
    def __init__(self, hp=100, mp=100, almas=0, tentativa=1):
        self.sprites = self.inicializa_sprites()
        self.current_sprite = self.sprites[0]
        self.estado = "spawn"
        self.hp = hp
        self.mp = mp
        self.qtd_almas = almas
        self.almas_salvas = almas
        self.chao = -1
        self.tentativa = tentativa
        self.hud = Hud(self)
        self.hud.atualiza()
        self.dmgFoice = 15
        self.dmgGrito = 70
        self.recover_cooldown = 0
        self.grito_cooldown = 0
        self.ataque_cooldown = 0


    def inicializa_sprites(self):
        spawn_morte = Sprite(resource_path("Images/Player/spawn.png"),22)
        spawn_morte.set_total_duration(1800)
        spawn_morte.set_position(50, 450)

        idle_direita = Sprite(resource_path("Images/Player/idle_direita.png"),8)
        idle_direita.set_total_duration(1000)

        idle_esquerda = Sprite(resource_path("Images/Player/idle_esquerda.png"),8)
        idle_esquerda.set_total_duration(1000)

        ataque_direita = Sprite(resource_path("Images/Player/ataque_direita.png"),13)
        ataque_direita.set_total_duration(300) 

        ataque_esquerda = Sprite(resource_path("Images/Player/ataque_esquerda.png"),13)
        ataque_esquerda.set_total_duration(300) 

        especial_esquerda = Sprite(resource_path("Images/Player/especial_esquerda.png"), 9)
        especial_esquerda.set_total_duration(450) 

        especial_direita = Sprite(resource_path("Images/Player/especial_direita.png"), 9)
        especial_direita.set_total_duration(450) 

        return [spawn_morte, idle_direita, idle_esquerda, ataque_direita, ataque_esquerda, especial_direita, especial_esquerda]
    
    def atualiza_estado(self, index=0):
        if (self.estado == "especial_d" or self.estado == "especial_e"):
            if self.current_sprite.curr_frame == self.current_sprite.get_final_frame() - 1: pass
            else: return
        elif (self.estado == "ataque_d" or self.estado == "ataque_e"):
            if self.current_sprite.curr_frame == self.current_sprite.get_final_frame() - 1: pass
            else: return
        if index == 5 or index == 6: self.current_sprite.curr_frame = 0
        if index == 3 or index == 4: self.current_sprite.curr_frame = 0
        self.sprites[index].set_position(self.current_sprite.x, self.current_sprite.y)
        self.current_sprite = self.sprites[index]
        self.estado = ["spawn", "idle_d", "idle_e", "ataque_d", "ataque_e", "especial_d", "especial_e"][index]
        
    def atualiza_status(self, status, qtd):
        if status == "hp":
            if 0 <= self.hp <= 100:
                if self.hp + qtd > 100: self.hp = 100
                elif self.hp + qtd < 0: self.hp = 0       
                else: self.hp += qtd
        elif status == "mp":
            if 49 <= self.mp <= 100:
                if self.mp + qtd > 100: self.mp = 100
                elif self.mp + qtd < 49: self.mp = 49       
                else: self.mp += qtd


    def isMorte_spawning(self): return self.estado == "spawn" 

    def isMorte_natural(self): return self.estado == "idle_d" or self.estado == "idle_e"
    
    def isMorte_attacking(self): return self.estado == "ataque_d" or self.estado == "ataque_e"

    def isMorte_special(self): return self.estado == "especial_e" or self.estado == "especial_d"

    def draw(self):
        self.current_sprite.draw()
    
    def update(self, tempo):
        if self.recover_cooldown > 0: self.recover_cooldown -= tempo
        if self.grito_cooldown > 0: self.grito_cooldown -= tempo
        if self.ataque_cooldown > 0: self.ataque_cooldown -= tempo
        
        self.hud.desenha()
        self.hud.atualiza()
        self.current_sprite.update()


#classe auxiliar para desenho do contador de almas
class Alma(Sprite):

    def __init__(self, x, y):
        super().__init__(resource_path("Images/Inimigos/Alma/sprite almas idle.png"), 4)
        self.set_total_duration(600)
        self.set_position(x, y)
        self.origem = [x, y]
    
    def atualiza(self, correcao):
        self.x = self.origem[0] + correcao
        self.update()