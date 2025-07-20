import pygame
from pygame import *

pygame.init()

win_size = 600
window = pygame.display.set_mode((win_size, win_size + 200))
pygame.display.set_caption('tic-tac-toe')

# Загрузка и масштабирование изображений
selection_bg = pygame.transform.scale(pygame.image.load('selection.jpg'), (win_size, win_size))
background = pygame.transform.scale(pygame.image.load('background.jpg'), (win_size, win_size))
clock = pygame.time.Clock()

player = None # Переменная для хранения текущего игрока ('p1' для крестиков, 'p2' для ноликов)
current_image = None # Изображение для текущего хода (крестик или нолик)

is_holding = False # Флаг для отслеживания удержания кнопки мыши (предотвращает множественные клики)

# Отображаем экран выбора игрока
window.blit(selection_bg, (0, 0))

# Состояние игрового поля: 0 - пустая ячейка, 'p1' - крестик, 'p2' - нолик
is_empty = [0, 0, 0, 0, 0, 0, 0, 0, 0]
draw_count = 0 # Счетчик ходов, для определения ничьей

choosing = True # Флаг для цикла выбора игрока
run = False # Флаг для основного игрового цикла
game_over = False # Флаг для состояния "игра завершена"
winner_text = "" # Переменная для текста о победителе/ничьей
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

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[self.mouse_btn] and not self.holding:
            self.holding = True
            action = True
        if pygame.mouse.get_pressed()[self.mouse_btn] == 0:
            self.holding = False
            action = False

        window.blit(self.image, (self.rect.x, self.rect.y))
        return action

restart_btn = Button(300, 300, 20, 20, 'cross.png', 0)

# --- Цикл выбора игрока ---
while choosing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            choosing = False # Выходим из цикла выбора
            run = False      # Устанавливаем run в False, чтобы игра не запускалась
            game_over = False # Устанавливаем game_over в False
            
    pos = pygame.mouse.get_pos() # Получаем текущие координаты мыши

    if pygame.mouse.get_pressed()[0] == 1: # Если нажата левая кнопка мыши
        if not is_holding: # Проверяем, не удерживается ли кнопка с предыдущего кадра
            is_holding = True # Устанавливаем флаг удержания

            if pos[0] >= 300: # Если клик был в правой половине экрана (выбор 'O')
                player = 'p2' # Игрок 2 (нолик) ходит первым
            else: # Если клик был в левой половине экрана (выбор 'X')
                player = 'p1' # Игрок 1 (крестик) ходит первым

            choosing = False # Завершаем цикл выбора
            run = True       # Начинаем основной игровой цикл
    elif pygame.mouse.get_pressed()[0] == 0: # Если кнопка мыши отпущена
        is_holding = False # Сбрасываем флаг удержания

    pygame.display.update()
    clock.tick(60)

# --- Подготовка к основному игровому циклу ---
# Отображаем фон игрового поля, как только выбор игрока сделан
window.blit(background, (0, 0))

# --- Основной игровой цикл ---
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False # Выход из игры
            game_over = False # Устанавливаем game_over в False

    # Определяем, какое изображение использовать для текущего хода
    if player == 'p1':
        current_image = pygame.transform.scale(pygame.image.load('cross.png'), (100, 100))
    else:
        current_image = pygame.transform.scale(pygame.image.load('circle.png'), (100, 100))

    pos = pygame.mouse.get_pos() # Получаем текущие координаты мыши
    # Вычисляем индекс ячейки, на которую указывает мышь (0-8)
    pos2 = pos[0] // 200 + pos[1] // 200 * 3 

    if pygame.mouse.get_pressed()[0] == 1 and not is_holding: # Если нажата левая кнопка мыши и не удерживается
        is_holding = True # Устанавливаем флаг удержания

        if not is_empty[pos2]: # Проверяем, что выбранная ячейка пуста
            is_empty[pos2] = player # Записываем текущего игрока в массив состояния поля
            # Отображаем изображение хода в центре соответствующей ячейки
            window.blit(current_image, (pos[0] // 200 * 200 + 50, pos[1] // 200 * 200 + 50))

            print(is_empty) # Выводим состояние поля в консоль
            draw_count += 1 # Увеличиваем счетчик ходов
            print(draw_count)

            # --- Проверка условий победы ---
            game_ended_this_turn = False # Флаг для отслеживания завершения игры в текущем ходе

            # Проверка по горизонталям
            if is_empty[0:3] == [player, player, player]:
                winner_text = f'ПЕРЕМІГ ГРАВЕЦЬ {player.upper()}!'
                game_ended_this_turn = True
            elif is_empty[3:6] == [player, player, player]:
                winner_text = f'ПЕРЕМІГ ГРАВЕЦЬ {player.upper()}!'
                game_ended_this_turn = True
            elif is_empty[6:9] == [player, player, player]:
                winner_text = f'ПЕРЕМІГ ГРАВЕЦЬ {player.upper()}!'
                game_ended_this_turn = True
            # Проверка по вертикалям
            elif [is_empty[0], is_empty[3], is_empty[6]] == [player, player, player]:
                winner_text = f'ПЕРЕМІГ ГРАВЕЦЬ {player.upper()}!'
                game_ended_this_turn = True
            elif [is_empty[1], is_empty[4], is_empty[7]] == [player, player, player]:
                winner_text = f'ПЕРЕМІГ ГРАВЕЦЬ {player.upper()}!'
                game_ended_this_turn = True
            elif [is_empty[2], is_empty[5], is_empty[8]] == [player, player, player]:
                winner_text = f'ПЕРЕМІГ ГРАВЕЦЬ {player.upper()}!'
                game_ended_this_turn = True
            # Проверка по диагоналям
            elif [is_empty[0], is_empty[4], is_empty[8]] == [player, player, player]:
                winner_text = f'ПЕРЕМІГ ГРАВЕЦЬ {player.upper()}!'
                game_ended_this_turn = True
            elif [is_empty[2], is_empty[4], is_empty[6]] == [player, player, player]:
                winner_text = f'ПЕРЕМІГ ГРАВЕЦЬ {player.upper()}!'
                game_ended_this_turn = True
            # Проверка на ничью (только если игра не закончилась победой)
            elif draw_count >= 9:
                winner_text = 'НІЧИЯ!'
                game_ended_this_turn = True
            
            # Если игра закончилась в этом ходу, устанавливаем флаги завершения
            if game_ended_this_turn:
                run = False # Выход из основного игрового цикла
                game_over = True # Переход в состояние отображения результата
                if player == 'p1':
                    wins_cross += 1
                else:
                    wins_circle += 2
            else: # Если никто не выиграл и игра не ничья, передаем ход другому игроку
                if player == 'p1':
                    player = 'p2'
                else:
                    player = 'p1'

    # Сброс флага is_holding, когда кнопка мыши отпущена
    if pygame.mouse.get_pressed()[0] == 0:
        is_holding = False

    pygame.display.update() # Обновляем экран
    clock.tick(60) # Устанавливаем FPS

restart_btn = Button(300, 300, 20, 20, 'cross.png', 0)

while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            choosing = False # Выходим из цикла выбора
            run = False      # Устанавливаем run в False, чтобы игра не запускалась
            game_over = False # Устанавливаем game_over в False

    # Задаем шрифт для текста победителя
    font = pygame.font.Font(None, 74) # Размер шрифта 74

    # Создаем текстовую поверхность
    text_surface = font.render(winner_text, True, (255, 255, 255)) # Белый цвет текста
    
    # Получаем прямоугольник текста для центрирования
    text_rect = text_surface.get_rect(center=(win_size // 2, win_size // 2))

    # Очищаем экран и отображаем фон (или можно оставить игровое поле)
    window.blit(background, (0, 0)) # Можно оставить текущее игровое поле или использовать новый фон
    # window.fill((0, 0, 0)) # Или залить экран черным цветом, если хотите полностью черный фон

    # Отображаем все текущие крестики и нолики, которые были на поле
    # Это важно, чтобы поле не исчезло, когда появится текст
    for i in range(9):
        if is_empty[i] == 'p1':
            img = pygame.transform.scale(pygame.image.load('cross.png'), (100, 100))
        elif is_empty[i] == 'p2':
            img = pygame.transform.scale(pygame.image.load('circle.png'), (100, 100))
        else:
            continue # Пропускаем пустые ячейки

        row = i // 3
        col = i % 3
        window.blit(img, (col * 200 + 50, row * 200 + 50))

    restart_btn.draw()
    
    # Отображаем текст победителя поверх всего
    window.blit(text_surface, text_rect)
    pygame.display.update()
    clock.tick(60)  # Устанавливаем FPS

pygame.quit() # Завершаем Pygame
