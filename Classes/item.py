import pygame


class Item:
    def __init__(self, name, lvl):
        self.name = name
        self.lvl = lvl
        self.range = 0
        self.dmg = 0
        self.speed = 0
        self.cool_down = 0
        self.base_hit_box = 0
        if self.name == "bow":
            self.range = 700
            self.dmg = self.lvl * 6
            self.speed = 20
            self.cool_down = 1.5
            self.base_hit_box = pygame.Rect((0, 0), (15, 50))
        elif self.name == "dagger":
            self.range = 120
            self.dmg = self.lvl * 10
            self.speed = 1
            self.cool_down = 2
            self.base_hit_box = pygame.Rect((0, 0), (40, 140))
        else:
            self.range = 300
            self.dmg = self.lvl * 2
            self.speed = 15
            self.cool_down = 0.5
            self.base_hit_box = pygame.Rect((0, 0), (15, 15))
