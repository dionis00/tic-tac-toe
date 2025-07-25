import pygame
from pygame import *

win_size = 600
window = pygame.display.set_mode((win_size, win_size + 200))
pygame.display.set_caption('tic-tac-toe')

selection_bg = pygame.transform.scale(pygame.image.load('selection.jpg'), (win_size, win_size))
background = pygame.transform.scale(pygame.image.load('background.jpg'), (win_size, win_size))
clock = pygame.time.Clock()
font.init()
f = font.Font(None, 36)


player = None
current_image = None

is_holding = False

window.blit(selection_bg, (0, 0))

is_empty = [0, 0, 0, 0, 0, 0, 0, 0, 0]
draw_count = 0

choosing = True
run = False
run2 = True
game_over = False
winner_text = ""
wins_cross = 0
wins_circle = 0

class Button():
    def __init__(self, x, y, width, height, img, mouse_btn):
        self.image = transform.scale(image.load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mouse_btn = int(mouse_btn)
        self.holding = False

    def update(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[self.mouse_btn] and not self.holding:
            self.holding = True
            action = True
            print('action')
        if pygame.mouse.get_pressed()[self.mouse_btn] == 0:
            self.holding = False
            action = False

        return action

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


restart_btn = Button(300, 300, 20, 20, 'cross.png', 0)

while choosing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            choosing = False
            run = False
            game_over = False

    pos = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0] == 1:
        if not is_holding:
            is_holding = True

            if pos[0] >= 300:
                player = 'p2'
            else:
                player = 'p1'

            choosing = False
            run = True
    elif pygame.mouse.get_pressed()[0] == 0:
        is_holding = False

    pygame.display.update()
    clock.tick(60)

window.blit(background, (0, 0))

restart_btn = Button(300, 300, 100, 100, 'cross.png', 0)
game_ended_this_turn = False

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            game_over = False

    while run2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                run2 = False
                game_over = False

        wr_text = f.render(str(wins_cross), True, (107, 255, 127))
        wc_text = f.render(str(wins_circle), True, (107, 255, 127))

        if player == 'p1':
            current_image = pygame.transform.scale(pygame.image.load('cross.png'), (100, 100))
        else:
            current_image = pygame.transform.scale(pygame.image.load('circle.png'), (100, 100))

        pos = pygame.mouse.get_pos()
        pos2 = pos[0] // 200 + pos[1] // 200 * 3

        if pygame.mouse.get_pressed()[0] == 1 and not is_holding:
            is_holding = True

            if not is_empty[pos2]:
                is_empty[pos2] = player
                window.blit(current_image, (pos[0] // 200 * 200 + 50, pos[1] // 200 * 200 + 50))

                if is_empty[0:3] == [player, player, player]:
                    winner_text = f'ПЕРЕМІГ ГРАВЕЦЬ {player.upper()}!'
                    game_ended_this_turn = True
                elif is_empty[3:6] == [player, player, player]:
                    winner_text = f'ПЕРЕМІГ ГРАВЕЦЬ {player.upper()}!'
                    game_ended_this_turn = True
                elif is_empty[6:9] == [player, player, player]:
                    winner_text = f'ПЕРЕМІГ ГРАВЕЦЬ {player.upper()}!'
                    game_ended_this_turn = True
                elif [is_empty[0], is_empty[3], is_empty[6]] == [player, player, player]:
                    winner_text = f'ПЕРЕМІГ ГРАВЕЦЬ {player.upper()}!'
                    game_ended_this_turn = True
                elif [is_empty[1], is_empty[4], is_empty[7]] == [player, player, player]:
                    winner_text = f'ПЕРЕМІГ ГРАВЕЦЬ {player.upper()}!'
                    game_ended_this_turn = True
                elif [is_empty[2], is_empty[5], is_empty[8]] == [player, player, player]:
                    winner_text = f'ПЕРЕМІГ ГРАВЕЦЬ {player.upper()}!'
                    game_ended_this_turn = True
                elif [is_empty[0], is_empty[4], is_empty[8]] == [player, player, player]:
                    winner_text = f'ПЕРЕМІГ ГРАВЕЦЬ {player.upper()}!'
                    game_ended_this_turn = True
                elif [is_empty[2], is_empty[4], is_empty[6]] == [player, player, player]:
                    winner_text = f'ПЕРЕМІГ ГРАВЕЦЬ {player.upper()}!'
                    game_ended_this_turn = True
                elif draw_count >= 9:
                    winner_text = 'НІЧИЯ!'
                    game_ended_this_turn = True

                if player == 'p1':
                    player = 'p2'
                else:
                    player = 'p1'

                print(is_empty)
                draw_count += 1
                print(draw_count)

        if pygame.mouse.get_pressed()[0] == 0:
            is_holding = False

        if game_ended_this_turn:
            if player == 'p1':
                wins_cross += 1
            else:
                wins_circle += 1

            # render text AFTER incrementing counters
            wr_text = f.render(str(wins_cross), True, (107, 255, 127))
            wc_text = f.render(str(wins_circle), True, (107, 255, 127))

            # draw updated texts
            window.blit(wr_text, (0, 0))
            window.blit(wc_text, (0, 30))

            restart_btn.draw()

            pygame.display.update()

            run2 = False

        pygame.display.update()
        clock.tick(60)

    if restart_btn.update():
        is_empty = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        draw_count = 0
        window.blit(background, (0, 0))
        game_ended_this_turn = False
        run2 = True

    pygame.display.update()
    clock.tick(60)
