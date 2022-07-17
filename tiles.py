import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load("graphics/empty.png")
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=pos)


class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos, size, over):
        super().__init__()
        if over is True:
            self.image = pygame.image.load("graphics/bomb_finish.png").convert_alpha()
        elif over is False:
            self.image = pygame.image.load("graphics/bomb.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=pos)


class Flag(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load("graphics/flag.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=pos)
