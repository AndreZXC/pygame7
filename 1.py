import pygame
import sys
import os

FPS = 50
pygame.init()
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 50)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


start_screen()


def load_level(name):
    filename = "data/" + name
    if not os.path.isfile(filename):
        print(f"Файл уровня с названием '{name}' не найден.")
        print(f"Чтобы добавить собственные уровни добавьте их в папку 'data', "
              f"файл должен иметь разрешение -.txt.")
        sys.exit()
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {'wall': load_image('box.png'), 'empty': load_image('grass.png')}
player_image = load_image('mario.png')
tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.type = tile_type
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)

    def update(self, mode):
        oldrect = self.rect
        if mode == 'up':
            self.rect = self.rect.move(0, -tile_height)
        if mode == 'down':
            self.rect = self.rect.move(0, tile_height)
        if mode == 'right':
            self.rect = self.rect.move(tile_width, 0)
        if mode == 'left':
            self.rect = self.rect.move(-tile_width, 0)
        colide = pygame.sprite.spritecollideany(self, tiles_group)
        if colide.type == 'wall':
            self.rect = oldrect


all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    return new_player, x, y


player, level_x, level_y = generate_level(load_level(f'{input("level: ")}.txt'))
size = width, height = tile_width * (level_x + 1), tile_height * (level_y + 1)
screen = pygame.display.set_mode(size)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


camera = Camera()
plaing = True
while plaing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            plaing = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_group.update('up')
            if event.key == pygame.K_DOWN:
                player_group.update('down')
            if event.key == pygame.K_LEFT:
                player_group.update('left')
            if event.key == pygame.K_RIGHT:
                player_group.update('right')
    pygame.display.flip()
    screen.fill((0, 0, 0))
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    clock.tick(FPS)
    tiles_group.draw(screen)
    player_group.draw(screen)

