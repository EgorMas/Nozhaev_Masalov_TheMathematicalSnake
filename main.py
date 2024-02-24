import pygame
import random
import sys
import os
import sqlite3

SIZE = (720, 460)
BUTTON = [(128, 255, 0), 5]
CURRENT_SNAKE = ('Обычная змейка', (0, 0, 255), 1, 1)
CURRENT_LEVEL = 1


def set_fon_global(name):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Не удаётся загрузить:", name)
        raise SystemExit(message)
    image = image.convert_alpha()
    return image


def set_text_global(text, letter_height, x_coord, y_coord, color="white"):
    font = pygame.font.Font(None, letter_height - 5)
    string_rendered = font.render(text, 1, pygame.Color(color))
    intro_rect = string_rendered.get_rect()
    intro_rect.x = x_coord
    intro_rect.y = y_coord
    return string_rendered, intro_rect


class MainGame():
    def __init__(self):
        global SIZE, BUTTON
        pygame.init()
        self.screen_width = SIZE[0]
        self.screen_height = SIZE[1]

        corteg = BUTTON[0]
        self.color = pygame.Color(corteg[0], corteg[1], corteg[2])
        self.button_width = (self.screen_width * 41.6) // 100
        self.button_height = (self.screen_height * 9) // 100
        self.width_of_frame = BUTTON[1]

        self.letter_height = int((self.screen_height * 6.52) // 100)

    def set_fon(self):
        fon = pygame.transform.scale(set_fon_global('forest.jpg'), (self.screen_width, self.screen_height))
        self.play_surface.blit(fon, (0, 0))

    def set_title(self):
        text = "Главное меню"
        x_coord = self.screen_width / 2 - ((len(text) / 2) * \
                                           (((self.letter_height + (self.screen_height * 3.26) / 100) / 3)))
        y_coord = self.screen_height / 100
        string_rendered, intro_rect = set_text_global(text,
                                                      int(self.letter_height + ((self.screen_height * 3.26) // 100)),
                                                      x_coord, y_coord)
        self.play_surface.blit(string_rendered, intro_rect)

    def set_buttons(self):
        text_for_buttons = ["Выбрать змейку", "Играть", "Выйти"]
        w = self.screen_width
        h = self.screen_height
        self.button_up_coords = [((w * 2.77) / 100, (h * 76.08) / 100), ((w * 55.56) / 100, (h * 76.08) / 100),
                                 ((w * 55.56) / 100, (h * 86.95) / 100)]

        for i in range(len(self.button_up_coords)):
            pygame.draw.rect(self.play_surface, self.color,
                             (self.button_up_coords[i][0], self.button_up_coords[i][1], self.button_width,
                              self.button_height), self.width_of_frame)

            x_coord = self.button_up_coords[i][0] + self.button_width // 2 - ((len(text_for_buttons[i]) // 2) * \
                                                                              (self.letter_height // 3))
            y_coord = self.button_up_coords[i][1] + self.button_height // 2 - self.letter_height // 3
            string_rendered, intro_rect = set_text_global(text_for_buttons[i], self.letter_height, x_coord, y_coord)
            self.play_surface.blit(string_rendered, intro_rect)

    def set_text(self):
        intro_text = ["Описание: При поедании яблока - появляется математическая",
                      "викторина на время. Конец игры при касании стенок,", "либо при 0 жизней."]

        y_coord = (self.screen_height * 19.56) / 100
        x_coord = (self.screen_width * 1.39) / 100
        for line in intro_text:
            string_rendered, intro_rect = set_text_global(line, self.letter_height, x_coord, y_coord)
            self.play_surface.blit(string_rendered, intro_rect)
            y_coord += (self.screen_height * 2.17) / 100
            y_coord += intro_rect.height

    def get_from_data(self):
        fullname = os.path.join('data', 'Permanent_base.db')
        try:
            sqlite_connection = sqlite3.connect(fullname)
            cursor = sqlite_connection.cursor()

            sqlite_select_query = """SELECT * from Last_information"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchone()
            cursor.close()
            sqlite_connection.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        return records

    def set_information(self):
        global CURRENT_SNAKE
        scores = self.get_from_data()
        named_text = ["Текущая змейка: ", "Лучшие результаты по уровням:"]
        levels_text = ["Первый уровень:        ", "Второй уровень:         ", "Третий  уровень:        ",
                       "Четвёртый уровень:   ", "Пятый уровень:          "]

        y_coord = (self.screen_height * 17.39) / 100
        x_coord = (self.screen_width * 2.78) / 100

        text = named_text[0] + CURRENT_SNAKE[0]
        string_rendered, intro_rect = set_text_global(text, self.letter_height, x_coord, y_coord, "red")
        self.play_surface.blit(string_rendered, intro_rect)

        y_coord += (self.letter_height - (self.screen_height * 1.09) / 100) * 2
        text_2 = named_text[1]
        string_rendered, intro_rect = set_text_global(text_2, self.letter_height, x_coord, y_coord, "white")
        self.play_surface.blit(string_rendered, intro_rect)

        y_coord += self.letter_height - (self.screen_height * 1.09) / 100
        for i in range(5):
            text_for_setting = levels_text[i] + str(scores[i])
            string_rendered, intro_rect = set_text_global(text_for_setting, self.letter_height, x_coord, y_coord)
            self.play_surface.blit(string_rendered, intro_rect)
            y_coord += self.letter_height - (self.screen_height * 3.26) / 100
            y_coord += intro_rect.height

    def create_surface(self):
        self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Математическая змейка')

        self.set_fon()
        self.set_buttons()
        self.set_title()
        # self.set_text()
        self.set_information()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    x = pos[0]
                    y = pos[1]
                    if self.button_up_coords[0][0] <= x <= self.button_up_coords[0][0] + self.button_width and \
                            self.button_up_coords[0][1] <= y <= self.button_up_coords[0][1] + self.button_height:
                        window = Check_snake()
                        window.create_surface()
                    elif self.button_up_coords[1][0] <= x <= self.button_up_coords[1][0] + self.button_width and \
                            self.button_up_coords[1][1] <= y <= self.button_up_coords[1][1] + self.button_height:
                        return
                    elif self.button_up_coords[2][0] <= x <= self.button_up_coords[2][0] + self.button_width and \
                            self.button_up_coords[2][1] <= y <= self.button_up_coords[2][1] + self.button_height:
                        sys.exit()
            pygame.display.flip()


class Check_snake():
    def __init__(self):
        global SIZE
        pygame.init()
        self.screen_width = SIZE[0]
        self.screen_height = SIZE[1]
        self.color = pygame.Color(128, 255, 0)

        corteg = BUTTON[0]
        self.color = pygame.Color(corteg[0], corteg[1], corteg[2])
        self.button_width = (self.screen_width * 41.6) // 100
        self.button_height = (self.screen_height * 9) // 100
        self.width_of_frame = BUTTON[1]

        self.letter_height = int((self.screen_height * 6.52) // 100)

        self.score = 0
        self.lives = 3
        self.fps = pygame.time.Clock()

    def create_surface(self):
        self.terrarium_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Математическая змейка')
        self.set_fon()
        self.set_title()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    window = MainGame()
                    window.create_surface()
            pygame.display.flip()

    def set_fon(self):
        fon = pygame.transform.scale(set_fon_global('Terrarium.jpg'), (self.screen_width, self.screen_height))
        self.terrarium_surface.blit(fon, (0, 0))

    def set_title(self):
        text = "Террариум"
        x_coord = self.screen_width / 2 - ((len(text) / 2) * \
                                           (((self.letter_height + (self.screen_height * 3.26) / 100) / 3)))
        y_coord = self.screen_height / 100
        string_rendered, intro_rect = set_text_global(text,
                                                      int(self.letter_height + ((self.screen_height * 3.26) // 100)),
                                                      x_coord, y_coord, "black")
        self.terrarium_surface.blit(string_rendered, intro_rect)


class Game_palce():
    def __init__(self):
        global SIZE
        pygame.init()
        self.screen_width = SIZE[0]
        self.screen_height = SIZE[1]

        self.score = 0
        self.lives = 3
        self.fps = pygame.time.Clock()

    def create_surface(self):
        self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Математическая змейка')

    def event(self, dir):
        # обработка событий (нажатие клавиш, выход)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                # dir - направление змеи, обработка нажатия клавиши, изменение направления движения
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    dir = "R"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    dir = "L"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    dir = "U"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    dir = "D"
                # выход из змейки в случае нажатия клавиши escape
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            # обработка закрытия змейки по [X]
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # возвращение направления змейки
        return dir

    def text_score_and_lives(self, rasp=1):
        # создание счётчика очков  и счётчика жизней в двух случаях
        # rasp=1 - счёт и жизни в левом верхнем углу (во время основного геймплея), жизни считаются как обычно
        # rasp=0 - счёт под надписью Game Over (в конце игры), жизни обнуляются, в левом верхнем углу
        score_font = pygame.font.SysFont(None, int((self.screen_height * 5.22) // 100))
        score_surf = score_font.render(
            'Счёт: {0}'.format(self.score), True, (0, 0, 0))
        score_rect = score_surf.get_rect()
        lives_font = pygame.font.SysFont(None, int((self.screen_height * 5.22) / 100))
        lives_surf = lives_font.render(
            'Жизней: {0}'.format(self.lives), True, (227, 27, 110))
        lives_rect = lives_surf.get_rect()
        lives_rect.midtop = ((self.screen_width * 22.22 / 100), (self.screen_height * 2.17 / 100))
        if rasp == 1:
            score_rect.midtop = ((self.screen_width * 11.11 / 100), (self.screen_height * 2.17 / 100))
        else:
            score_rect.midtop = ((self.screen_width * 50 / 100), (self.screen_height * 26.09 / 100))
            lives_surf = lives_font.render(
                'Жизней: 0', True, (227, 27, 110))
        # создание текста на экране
        self.play_surface.blit(lives_surf, lives_rect)
        self.play_surface.blit(score_surf, score_rect)

    def game_over(self):
        # конец игры (смерть змейки), вывод надписи Game Over и счёта под ней
        end_font = pygame.font.SysFont(None, int(self.screen_width * 10 / 100))
        end_surf = end_font.render('Game over', True, (255, 0, 0))
        end_rect = end_surf.get_rect()
        end_rect.midtop = ((self.screen_width * 50 / 100), (self.screen_height * 3.26 / 100))
        self.play_surface.blit(end_surf, end_rect)
        self.text_score_and_lives(0)
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                        sys.exit()
            pygame.display.flip()


class Snake():
    def __init__(self):
        # важные переменные - позиция головы змеи и его тела
        self.snake_head_pos = [100, 50]  # [x, y]
        # начальное тело змеи состоит из трех сегментов
        # голова - первый элемент, хвост - последний
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.snake_color = (32, 178, 170)
        # направление движение змеи, изначально будет вправо
        self.direction = "R"
        self.dir = self.direction

    def change_dir(self):
        # изменение направления движения змейки
        # условие, что новое изменение не противоположно прошлому (лево-право, верх-низ)
        if any((self.dir == "R" and not self.direction == "L",
                self.dir == "L" and not self.direction == "R",
                self.dir == "U" and not self.direction == "D",
                self.dir == "D" and not self.direction == "U")):
            self.direction = self.dir

    def head_position(self):
        # движение головы
        if self.direction == "R":
            self.snake_head_pos[0] += 10
        elif self.direction == "L":
            self.snake_head_pos[0] -= 10
        elif self.direction == "U":
            self.snake_head_pos[1] -= 10
        elif self.direction == "D":
            self.snake_head_pos[1] += 10

    def snake_body_create(self, score, food_pos, screen_width, screen_height):
        self.snake_body.insert(0, list(self.snake_head_pos))
        # если съели еду
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            # если съели еду то задаем новое положение еды случайным образом и открываем окно с вопросом
            food_pos = [random.randrange(1, screen_width // 10) * 10,
                        random.randrange(1, screen_height // 10) * 10]
            score += food.matematica()
        else:
            # если не нашли еду, то убираем последний сегмент,
            # если этого не сделать, то змея будет постоянно расти
            self.snake_body.pop()
        return score, food_pos

    def draw_snake(self, play_surface):
        global CURRENT_SNAKE
        color = CURRENT_SNAKE[1]
        # отображение змеи на экране
        play_surface.fill((255, 255, 255))
        for pos in self.snake_body:
            # pygame.Rect(x,y, sizex, sizey)
            pygame.draw.rect(
                play_surface, (color[0], color[1], color[2]), pygame.Rect(
                    pos[0], pos[1], 10, 10))

    def check_collision(self, game_over, screen_width, screen_height):
        # проверка на соприкосновение со стенами или с сегментами тела
        if any((
                self.snake_head_pos[0] > screen_width - 10
                or self.snake_head_pos[0] < 0,
                self.snake_head_pos[1] > screen_height - 10
                or self.snake_head_pos[1] < 0
        )):
            game_over()
        for block in self.snake_body[1:]:
            # проверка на то, что первый элемент(голова) врезался в любой другой сегмент тела
            if (block[0] == self.snake_head_pos[0] and
                    block[1] == self.snake_head_pos[1]):
                game_over()


class Food():
    def __init__(self, screen_width, screen_height):
        self.food_pos = [random.randrange(1, screen_width // 10) * 10,
                         random.randrange(1, screen_height // 10) * 10]

    def draw_food(self, play_surface):
        # отображение еды на экране
        pygame.draw.rect(
            play_surface, (245, 113, 37), pygame.Rect(
                self.food_pos[0], self.food_pos[1],
                10, 10))

    def matematica(self):
        answering = True
        time = 10
        first, second = random.randrange(1, 100), random.randrange(1, 100)
        glush1, glush2 = random.randrange(1, 100), random.randrange(1, 100)
        virazh = random.randrange(0, 2)
        answer = 0
        posit = random.randrange(1, 4)
        deistv = None
        if virazh == 0:
            deistv = '+'
            answer = first + second
        else:
            deistv = '-'
            answer = first - second
        main_font = pygame.font.SysFont(None, 24)
        while answering:
            pygame.draw.rect(
                game.play_surface, (255, 255, 255), pygame.Rect(
                    50, 80, 200, 200))
            pygame.draw.rect(
                game.play_surface, (0, 0, 0), pygame.Rect(
                    55, 70, 190, 190), 3)
            ques_surf = main_font.render(
                'Осталось времени: {0}'.format(time), True, (0, 0, 0))
            ques_rect = ques_surf.get_rect()
            ques_rect.midtop = (150, 80)
            vopr_surf = main_font.render(f'{first} {deistv} {second} = ?', True, (0, 0, 0))
            vopr_rect = vopr_surf.get_rect()
            vopr_rect.midtop = (150, 100)
            game.play_surface.blit(ques_surf, ques_rect)
            game.play_surface.blit(vopr_surf, vopr_rect)
            a = pygame.Rect(120, 130, 60, 20)
            b = pygame.Rect(120, 170, 60, 20)
            c = pygame.Rect(120, 210, 60, 20)
            pygame.draw.rect(
                game.play_surface, (0, 0, 0), a, 2)
            pygame.draw.rect(
                game.play_surface, (0, 0, 0), b, 2)
            pygame.draw.rect(
                game.play_surface, (0, 0, 0), c, 2)
            if posit == 1:
                otvet1_surf = main_font.render(f'{answer}', True, (0, 0, 0))
                otvet1_rect = vopr_surf.get_rect()
                otvet1_rect.midtop = (180, 132)
                game.play_surface.blit(otvet1_surf, otvet1_rect)
                otvet2_surf = main_font.render(f'{glush1}', True, (0, 0, 0))
                otvet2_rect = vopr_surf.get_rect()
                otvet2_rect.midtop = (180, 172)
                game.play_surface.blit(otvet2_surf, otvet2_rect)
                otvet3_surf = main_font.render(f'{glush2}', True, (0, 0, 0))
                otvet3_rect = vopr_surf.get_rect()
                otvet3_rect.midtop = (180, 212)
                game.play_surface.blit(otvet3_surf, otvet3_rect)

            elif posit == 2:
                otvet1_surf = main_font.render(f'{glush1}', True, (0, 0, 0))
                otvet1_rect = vopr_surf.get_rect()
                otvet1_rect.midtop = (180, 132)
                game.play_surface.blit(otvet1_surf, otvet1_rect)
                otvet2_surf = main_font.render(f'{answer}', True, (0, 0, 0))
                otvet2_rect = vopr_surf.get_rect()
                otvet2_rect.midtop = (180, 172)
                game.play_surface.blit(otvet2_surf, otvet2_rect)
                otvet3_surf = main_font.render(f'{glush2}', True, (0, 0, 0))
                otvet3_rect = vopr_surf.get_rect()
                otvet3_rect.midtop = (180, 212)
                game.play_surface.blit(otvet3_surf, otvet3_rect)
            else:
                otvet1_surf = main_font.render(f'{glush2}', True, (0, 0, 0))
                otvet1_rect = vopr_surf.get_rect()
                otvet1_rect.midtop = (180, 132)
                game.play_surface.blit(otvet1_surf, otvet1_rect)
                otvet2_surf = main_font.render(f'{glush1}', True, (0, 0, 0))
                otvet2_rect = vopr_surf.get_rect()
                otvet2_rect.midtop = (180, 172)
                game.play_surface.blit(otvet2_surf, otvet2_rect)
                otvet3_surf = main_font.render(f'{answer}', True, (0, 0, 0))
                otvet3_rect = vopr_surf.get_rect()
                otvet3_rect.midtop = (180, 212)
                game.play_surface.blit(otvet3_surf, otvet3_rect)
            pygame.display.flip()
            game.fps.tick(1)
            time -= 1
            if time == 0:
                game.lives -= 1
                if game.lives == 0:
                    pygame.draw.rect(
                        game.play_surface, (255, 255, 255), pygame.Rect(
                            50, 10, 200, 200))
                    pygame.draw.rect(
                        game.play_surface, (255, 255, 255), pygame.Rect(
                            50, 80, 230, 210))
                    pygame.display.flip()
                    game.game_over()
                return 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                        sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if posit == 1 and a.collidepoint(event.pos):
                            answering = False
                            return 1
                        elif posit == 2 and b.collidepoint(event.pos):
                            answering = False
                            return 1
                        elif posit == 3 and c.collidepoint(event.pos):
                            answering = False
                            return 1
                        else:
                            answering = False
                            game.lives -= 1
                            if game.lives == 0:
                                pygame.draw.rect(
                                    game.play_surface, (255, 255, 255), pygame.Rect(
                                        50, 10, 200, 200))
                                pygame.draw.rect(
                                    game.play_surface, (255, 255, 255), pygame.Rect(
                                        50, 80, 230, 210))
                                pygame.display.flip()
                                game.game_over()
                            return 0


game1 = MainGame()
snake = Snake()
food = Food(game1.screen_width, game1.screen_height)

game1.create_surface()

game = Game_palce()
game.create_surface()

while True:
    snake.dir = game.event(snake.change_dir)

    snake.change_dir()
    snake.head_position()
    game.score, food.food_pos = snake.snake_body_create(
        game.score, food.food_pos, game.screen_width, game.screen_height)
    snake.draw_snake(game.play_surface)

    food.draw_food(game.play_surface)

    snake.check_collision(
        game.game_over, game.screen_width, game.screen_height)

    game.text_score_and_lives()
    pygame.display.flip()
    game.fps.tick(17)
