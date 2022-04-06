import time

# GLOBAL VARIABLES
collide_list = [4, 5, 22, 23, 26, 39, 40, 41, 43, 57, 59, 60, 75, 76, 77, 78, 92, 93, 94, 95, 96]


class Player:
    def __init__(self, nickname, ip, key):
        self.x = 1000
        self.y = 1000
        self.dirX = 0
        self.dirY = 0
        self.Class = "Mage"
        self.last_used_ability = 0
        self.last_moved_time = 0
        self.other_players_list = []
        self.projectiles = []
        self.picked = 0
        self.inventory = []  # to add items later
        self.gold = 0
        self.health = 100
        self.nickname = nickname
        self.ip = ip
        self.key = key

    def check_collision(self, map):
        return int(map[self.y // 64][self.x // 64]) in collide_list

    def move(self):
        if time.time() - self.last_moved_time > 10 ** -3:
            self.x += self.dirX
            if self.check_collision():
                self.x -= self.dirX
            self.y += self.dirY
            if self.check_collision():
                self.y -= self.dirY

    def attack(self, mouseX, mouseY):
        self.projectiles.append(particle(self.x, self.y, mouseX, mouseY, self.inventory[self.picked]))

    def use_ability(self):
        if time.time() - self.last_used_ability > self.Class.cooldown:
            self.last_used_ability = time.time()
            self.Class.use_ability()
