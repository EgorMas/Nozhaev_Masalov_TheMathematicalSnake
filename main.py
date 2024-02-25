import pygame
import random
import sys
import os
import sqlite3

SIZE = (720, 460)
BUTTON = [(128, 255, 0), 5]
CURRENT_SNAKE = None  # Пример переменной: ('Уж', (0, 0, 0), 3, 1) - (Name, (R, G, B), Coeff_time, Coeff_speed))
CURRENT_LEVEL = 1
LIVES = 3
SCORE = 0


def make_current_snake():
    global CURRENT_SNAKE
    if CURRENT_SNAKE == None:
        fullname = os.path.join('data', 'Permanent_base.db')
        try:
            sqlite_connection = sqlite3.connect(fullname)
            cursor = sqlite_connection.cursor()

            sqlite_select_query = """SELECT Last_sanke_id from Last_information"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchone()
            cursor.close()
            sqlite_connection.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        id = records[0]
        fullname = os.path.join('data', 'Permanent_base.db')
        try:
            sqlite_connection = sqlite3.connect(fullname)
            cursor = sqlite_connection.cursor()

            sqlite_select_query = f"""SELECT * from Snakes WHERE id=={id}"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchone()
            cursor.close()
            sqlite_connection.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        corteg = records
        CURRENT_SNAKE = (corteg[1], (corteg[2], corteg[3], corteg[4]), corteg[5], corteg[6])


make_current_snake()


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

    def create_surface(self):
        self.play_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Математическая змейка')

        self.set_fon()
        self.set_title()
        self.set_buttons()
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
                        window = Choose_snake()
                        window.create_surface()
                    elif self.button_up_coords[1][0] <= x <= self.button_up_coords[1][0] + self.button_width and \
                            self.button_up_coords[1][1] <= y <= self.button_up_coords[1][1] + self.button_height:
                        window = Level_choice()
                        window.create_surface()
                        # return
                    elif self.button_up_coords[2][0] <= x <= self.button_up_coords[2][0] + self.button_width and \
                            self.button_up_coords[2][1] <= y <= self.button_up_coords[2][1] + self.button_height:
                        sys.exit()
            pygame.display.flip()

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


class Choose_snake():
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

    def create_surface(self):
        self.terrarium_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Математическая змейка')
        self.set_fon()
        self.set_title()
        self.set_text()
        self.set_buttons()

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
                        self.set_snake(1)
                    elif self.button_up_coords[1][0] <= x <= self.button_up_coords[1][0] + self.button_width and \
                            self.button_up_coords[1][1] <= y <= self.button_up_coords[1][1] + self.button_height:
                        self.set_snake(2)
                    elif self.button_up_coords[2][0] <= x <= self.button_up_coords[2][0] + self.button_width and \
                            self.button_up_coords[2][1] <= y <= self.button_up_coords[2][1] + self.button_height:
                        self.set_snake(3)
                    elif self.button_up_coords[3][0] <= x <= self.button_up_coords[3][0] + self.button_width and \
                            self.button_up_coords[3][1] <= y <= self.button_up_coords[3][1] + self.button_height:
                        self.set_snake(4)
                    elif self.button_up_coords[4][0] <= x <= self.button_up_coords[4][0] + self.button_width and \
                            self.button_up_coords[4][1] <= y <= self.button_up_coords[4][1] + self.button_height:
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

    def set_buttons(self):
        snakes = self.get_information_about_snakes()
        self.set_informatin(snakes)
        snakes.append(("На главную", self.color[0], self.color[1], self.color[2]))
        w = self.screen_width
        h = self.screen_height
        self.button_up_coords = [((w * 2.78 / 100), (h * 21.73 / 100)), ((w * 2.78 / 100), (h * 38.04 / 100)),
                                 ((w * 2.78 / 100), (h * 54.35 / 100)), ((w * 2.78 / 100), (h * 70.65 / 100)),
                                 ((w * 55.55 / 100), (h * 86.96 / 100))]

        for i in range(len(self.button_up_coords)):
            pygame.draw.rect(self.terrarium_surface, (snakes[i][1], snakes[i][2], snakes[i][3]),
                             (self.button_up_coords[i][0], self.button_up_coords[i][1], self.button_width,
                              self.button_height))

            x_coord = self.button_up_coords[i][0] + self.button_width // 2 - ((len(snakes[i][0]) // 2) * \
                                                                              (self.letter_height // 3))
            y_coord = self.button_up_coords[i][1] + self.button_height // 2 - self.letter_height // 3
            if snakes[i][0] == "Черная мамба":
                string_rendered, intro_rect = set_text_global(snakes[i][0], self.letter_height, x_coord, y_coord,
                                                              "white")
            else:
                string_rendered, intro_rect = set_text_global(snakes[i][0], self.letter_height, x_coord, y_coord,
                                                              "black")
            self.terrarium_surface.blit(string_rendered, intro_rect)

    def set_text(self):
        text = "Выберите змейку (по имени, цвету или способностям):"
        string_rendered, intro_rect = set_text_global(text, self.letter_height, self.screen_width * 2.77 / 100,
                                                      self.screen_height * 10.3 / 100)
        self.terrarium_surface.blit(string_rendered, intro_rect)

    def set_informatin(self, snakes):
        text_for_buttons = []
        for snake in snakes:
            text = f"Множители:  время: x{snake[4]}, скорость: x{snake[5]}"
            text_for_buttons.append(text)

        w = self.screen_width
        h = self.screen_height
        self.texts_up_coords = [((w * 51.39 / 100), (h * 21.73 / 100)), ((w * 51.39 / 100), (h * 38.04 / 100)),
                                ((w * 51.39 / 100), (h * 54.35 / 100)), ((w * 51.39 / 100), (h * 70.65 / 100))]

        for i in range(len(self.texts_up_coords)):
            pygame.draw.rect(self.terrarium_surface, (0, 0, 0),
                             (self.texts_up_coords[i][0], self.texts_up_coords[i][1], self.button_width * 1.1,
                              self.button_height))

            x_coord = self.texts_up_coords[i][0] + self.button_width * 1.1 // 2 - ((len(text_for_buttons[i]) // 2) * \
                                                                                   (self.letter_height // 3))
            y_coord = self.texts_up_coords[i][1] + self.button_height // 2 - self.letter_height // 3
            string_rendered, intro_rect = set_text_global(text_for_buttons[i], self.letter_height, x_coord, y_coord)
            self.terrarium_surface.blit(string_rendered, intro_rect)

    def get_from_snakes(self, id):
        fullname = os.path.join('data', 'Permanent_base.db')
        try:
            sqlite_connection = sqlite3.connect(fullname)
            cursor = sqlite_connection.cursor()

            sqlite_select_query = f"""SELECT * from Snakes WHERE id=={id}"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchone()
            cursor.close()
            sqlite_connection.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        return records

    def set_for_last_information(self, id):
        fullname = os.path.join('data', 'Permanent_base.db')
        try:
            sqlite_connection = sqlite3.connect(fullname)
            cursor = sqlite_connection.cursor()

            sql_update_query = f"""UPDATE Last_information SET Last_sanke_id = {id}"""
            cursor.execute(sql_update_query)
            sqlite_connection.commit()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    def set_snake(self, id):
        global CURRENT_SNAKE
        corteg = self.get_from_snakes(id)
        CURRENT_SNAKE = (corteg[1], (corteg[2], corteg[3], corteg[4]), corteg[5], corteg[6])
        self.set_for_last_information(corteg[0])
        window = MainGame()
        window.create_surface()

    def get_information_about_snakes(self):
        fullname = os.path.join('data', 'Permanent_base.db')
        try:
            sqlite_connection = sqlite3.connect(fullname)
            cursor = sqlite_connection.cursor()

            sqlite_select_query = """SELECT Name, Red, Green, Blue, Coeff_time, Coeff_speed from Snakes"""
            cursor.execute(sqlite_select_query)
            snakes = cursor.fetchall()
            cursor.close()
            sqlite_connection.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        return snakes


class Level_choice():
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

    def create_surface(self):
        global CURRENT_LEVEL
        self.choice_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Математическая змейка')

        self.set_title()
        self.set_text()
        self.set_buttons()

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
                        CURRENT_LEVEL = 1
                        playing()
                    elif self.button_up_coords[1][0] <= x <= self.button_up_coords[1][0] + self.button_width and \
                            self.button_up_coords[1][1] <= y <= self.button_up_coords[1][1] + self.button_height:
                        CURRENT_LEVEL = 2
                        playing()
                    elif self.button_up_coords[2][0] <= x <= self.button_up_coords[2][0] + self.button_width and \
                            self.button_up_coords[2][1] <= y <= self.button_up_coords[2][1] + self.button_height:
                        CURRENT_LEVEL = 3
                        playing()
                    elif self.button_up_coords[3][0] <= x <= self.button_up_coords[3][0] + self.button_width and \
                            self.button_up_coords[3][1] <= y <= self.button_up_coords[3][1] + self.button_height:
                        CURRENT_LEVEL = 4
                        playing()
                    elif self.button_up_coords[4][0] <= x <= self.button_up_coords[4][0] + self.button_width and \
                            self.button_up_coords[4][1] <= y <= self.button_up_coords[4][1] + self.button_height:
                        CURRENT_LEVEL = 5
                        playing()
                    elif self.button_up_coords[5][0] <= x <= self.button_up_coords[5][0] + self.button_width and \
                            self.button_up_coords[5][1] <= y <= self.button_up_coords[5][1] + self.button_height:
                        window = MainGame()
                        window.create_surface()
            pygame.display.flip()

    def set_title(self):
        text = "Уровни"
        x_coord = self.screen_width / 2 - ((len(text) / 2) * \
                                           (((self.letter_height + (self.screen_height * 3.26) / 100) / 3)))
        y_coord = self.screen_height / 100
        string_rendered, intro_rect = set_text_global(text,
                                                      int(self.letter_height + ((self.screen_height * 3.26) // 100)),
                                                      x_coord, y_coord)
        self.choice_surface.blit(string_rendered, intro_rect)

    def set_text(self):
        text = "Выберите уровень:"
        intro_text = ["Описание: При поедании ", "яблока - появляется математическая", "викторина на время.",
                      "Конец игры при касании стенок,", "либо при 0 жизней."]

        x_coord = self.screen_width * 2.78 / 100
        y_coord = self.screen_height * 16.3 / 100
        string_rendered, intro_rect = set_text_global(text, self.letter_height + int(self.screen_height * 1.08 // 100),
                                                      x_coord, y_coord)
        self.choice_surface.blit(string_rendered, intro_rect)

        x_coord = self.screen_width * 47.22 / 100
        y_coord = self.screen_height * 19.56 / 100
        for line in intro_text:
            string_rendered, intro_rect = set_text_global(line, self.letter_height, x_coord, y_coord)
            self.choice_surface.blit(string_rendered, intro_rect)
            y_coord += (self.screen_height * 2.17) / 100
            y_coord += intro_rect.height

    def set_buttons(self):
        text_for_buttons = ["Первый уровень: easy", "Второй уровень: easy", "Третий уровень: middle",
                            "Четвёртый уровень: hard", "Пятый уровень: impossible", "На главную"]
        w = self.screen_width
        h = self.screen_height
        self.button_up_coords = [((w * 2.78 / 100), (h * 21.73 / 100)), ((w * 2.78 / 100), (h * 32.61 / 100)),
                                 ((w * 2.78 / 100), (h * 43.48 / 100)), ((w * 2.78 / 100), (h * 54.35 / 100)),
                                 ((w * 2.78 / 100), (h * 65.22 / 100)), ((w * 55.55 / 100), (h * 86.96 / 100))]

        for i in range(len(self.button_up_coords)):
            pygame.draw.rect(self.choice_surface, self.color,
                             (self.button_up_coords[i][0], self.button_up_coords[i][1], self.button_width,
                              self.button_height), self.width_of_frame)

            x_coord = self.button_up_coords[i][0] + self.button_width // 2 - ((len(text_for_buttons[i]) // 2) * \
                                                                              (self.letter_height // 3))
            y_coord = self.button_up_coords[i][1] + self.button_height // 2 - self.letter_height // 3
            string_rendered, intro_rect = set_text_global(text_for_buttons[i], self.letter_height, x_coord, y_coord)
            self.choice_surface.blit(string_rendered, intro_rect)


class Game_palce():
    def __init__(self):
        global SIZE, SCORE
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
        global SCORE, LIVES
        x = (self.screen_width / 100)
        y = (self.screen_height * 2.17 / 100)

        text_for_score = f'Счёт: {SCORE}'
        score_surf, score_rect = set_text_global(text_for_score, int((self.screen_height * 5.22) // 100), x, y, "black")
        self.play_surface.blit(score_surf, score_rect)

        x += len(text_for_score) * int((self.screen_height * 5.22) // 100) / 3

        text_for_lives = f'Жизней: {LIVES}'
        life_surf, life_rect = set_text_global(text_for_lives, int((self.screen_height * 5.22) // 100),
                                               x, y, (227, 27, 110))
        self.play_surface.blit(life_surf, life_rect)

    def game_over(self):
        global LIVES
        LIVES = 3
        window = End_wind()
        window.create_surface()


class End_wind():
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

    def set_title(self):
        text = "GAME OVER"
        x_coord = self.screen_width / 2 - ((len(text) / 2) * \
                                           (((self.letter_height + (self.screen_height * 3.26) / 100) / 3)))
        y_coord = self.screen_height / 100
        string_rendered, intro_rect = set_text_global(text,
                                                      int(self.letter_height + ((self.screen_height * 3.26) // 100)),
                                                      x_coord, y_coord, "red")
        self.end_surface.blit(string_rendered, intro_rect)

    def set_buttons(self):
        text_for_buttons = ["Заново", "На главную"]
        w = self.screen_width
        h = self.screen_height
        self.button_up_coords = [((w * 2.77) / 100, (h * 76.08) / 100), ((w * 55.56) / 100, (h * 76.08) / 100)]

        for i in range(len(self.button_up_coords)):
            pygame.draw.rect(self.end_surface, self.color,
                             (self.button_up_coords[i][0], self.button_up_coords[i][1], self.button_width,
                              self.button_height), self.width_of_frame)

            x_coord = self.button_up_coords[i][0] + self.button_width // 2 - ((len(text_for_buttons[i]) // 2) * \
                                                                              (self.letter_height // 3))
            y_coord = self.button_up_coords[i][1] + self.button_height // 2 - self.letter_height // 3
            string_rendered, intro_rect = set_text_global(text_for_buttons[i], self.letter_height, x_coord, y_coord,
                                                          "white")

            self.end_surface.blit(string_rendered, intro_rect)

    def set_text(self):
        global CURRENT_SNAKE, CURRENT_LEVEL, SCORE
        text = [f'Текущая змейка: {CURRENT_SNAKE[0]}', f"Текущий уровень: {CURRENT_LEVEL}", f'Ваш результат: {SCORE}']

        y_coord = self.screen_height * 19.56 / 100
        for line in text:
            x_coord = self.screen_width / 2 - ((len(line) * (self.letter_height * 1.25) // 3) / 2)
            string_rendered, intro_rect = set_text_global(line, int(self.letter_height * 1.25 // 1), x_coord, y_coord)
            self.end_surface.blit(string_rendered, intro_rect)
            y_coord += (self.screen_height * 2.17) / 100
            y_coord += intro_rect.height

    def create_surface(self):
        global CURRENT_LEVEL
        self.end_surface = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption('Математическая змейка')

        self.set_title()
        self.set_text()
        self.set_buttons()
        self.update_global_score()

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
                        playing()
                    if self.button_up_coords[1][0] <= x <= self.button_up_coords[1][0] + self.button_width and \
                            self.button_up_coords[1][1] <= y <= self.button_up_coords[1][1] + self.button_height:
                        window = MainGame()
                        window.create_surface()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_BACKSPACE:
                        sys.exit()
            pygame.display.flip()

    def update_global_score(self):
        global CURRENT_LEVEL, SCORE
        list_for_request = ['First', 'Second', 'Third', 'Fourth', 'Fift']
        fullname = os.path.join('data', 'Permanent_base.db')
        try:
            sqlite_connection = sqlite3.connect(fullname)
            cursor = sqlite_connection.cursor()

            sqlite_select_query = f"""SELECT {list_for_request[CURRENT_LEVEL - 1]} from Last_information"""
            cursor.execute(sqlite_select_query)
            inf = cursor.fetchall()
            cursor.close()
            sqlite_connection.close()

        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

        if SCORE > inf[0][0]:
            fullname = os.path.join('data', 'Permanent_base.db')
            try:
                sqlite_connection = sqlite3.connect(fullname)
                cursor = sqlite_connection.cursor()

                sql_update_query = f"""UPDATE Last_information SET {list_for_request[CURRENT_LEVEL - 1]} = {SCORE}"""
                cursor.execute(sql_update_query)
                sqlite_connection.commit()

            except sqlite3.Error as error:
                print("Ошибка при работе с SQLite", error)
        SCORE = 0


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

    def snake_body_create(self, food_pos, screen_width, screen_height):
        global SCORE
        self.snake_body.insert(0, list(self.snake_head_pos))
        # если съели еду
        if (self.snake_head_pos[0] == food_pos[0] and
                self.snake_head_pos[1] == food_pos[1]):
            # если съели еду то задаем новое положение еды случайным образом и открываем окно с вопросом
            food_pos = [random.randrange(1, screen_width // 10) * 10,
                        random.randrange(1, screen_height // 10) * 10]
            SCORE += food.matematica()
        else:
            # если не нашли еду, то убираем последний сегмент,
            # если этого не сделать, то змея будет постоянно расти
            self.snake_body.pop()
        return food_pos

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
        global SIZE
        self.screen_width = SIZE[0]
        self.screen_height = SIZE[1]
        self.food_pos = [random.randrange(1, screen_width // 10) * 10,
                         random.randrange(1, screen_height // 10) * 10]

    def draw_food(self, play_surface):
        # отображение еды на экране
        pygame.draw.rect(
            play_surface, (245, 113, 37), pygame.Rect(
                self.food_pos[0], self.food_pos[1],
                10, 10))

    def generator(self):
        global CURRENT_LEVEL
        if CURRENT_LEVEL == 1:
            a = random.randrange(1, 9)
        elif CURRENT_LEVEL == 2:
            a = random.randrange(10, 99)
        elif CURRENT_LEVEL == 3:
            a = random.randrange(100, 999)
        elif CURRENT_LEVEL == 4:
            a = random.randrange(1000, 9999)
        elif CURRENT_LEVEL == 5:
            a = random.randrange(10000, 99999)

        return a

    def create_glush(self, answer):
        global CURRENT_LEVEL
        index = CURRENT_LEVEL - 1
        sp1 = [1, 1, 10, 101, 1010]
        sp2 = [2, 2, 20, 202, 2020]
        virazh = random.randrange(0, 2)
        if virazh == 0:
            a = answer - sp1[index]
            b = answer + sp2[index]
        else:
            a = answer + sp1[index]
            b = answer - sp2[index]
        return a, b

    def matematica(self):
        global CURRENT_SNAKE, LIVES
        answering = True
        time = 15 * CURRENT_SNAKE[2]

        first, second = self.generator(), self.generator()

        virazh = random.randrange(0, 2)
        if virazh == 0:
            deistv = '+'
            answer = first + second
        else:
            deistv = '-'
            answer = first - second

        glush1, glush2 = self.create_glush(answer)

        main_font = pygame.font.SysFont(None, 24)
        posit = random.randrange(1, 4)
        text = f'{first} {deistv} {second} = ?'
        x_coord = 100
        y_coord = self.screen_height * 21.74 / 100
        vopr_surf, vopr_rect = set_text_global(text,
                                               int(self.screen_height * 6 // 100), x_coord, y_coord, "black")
        game.play_surface.blit(vopr_surf, vopr_rect)

        a = pygame.Rect(120, 130, 70, 20)
        b = pygame.Rect(120, 170, 70, 20)
        c = pygame.Rect(120, 210, 70, 20)
        pygame.draw.rect(
            game.play_surface, (0, 0, 0), a, 2)
        pygame.draw.rect(
            game.play_surface, (0, 0, 0), b, 2)
        pygame.draw.rect(
            game.play_surface, (0, 0, 0), c, 2)

        line = []
        if posit == 1:
            a_num = answer
            b_num = glush1
            c_num = glush2
        elif posit == 2:
            a_num = glush2
            b_num = answer
            c_num = glush1
        else:
            a_num = glush1
            b_num = glush2
            c_num = answer

        line.append(a_num)
        line.append(b_num)
        line.append(c_num)

        otvet1_surf = main_font.render(f'{line[0]}', True, (0, 0, 0))
        otvet1_rect = vopr_surf.get_rect()
        otvet1_rect.midtop = (190, 132)
        game.play_surface.blit(otvet1_surf, otvet1_rect)

        otvet2_surf = main_font.render(f'{line[1]}', True, (0, 0, 0))
        otvet2_rect = vopr_surf.get_rect()
        otvet2_rect.midtop = (190, 172)
        game.play_surface.blit(otvet2_surf, otvet2_rect)

        otvet3_surf = main_font.render(f'{line[2]}', True, (0, 0, 0))
        otvet3_rect = vopr_surf.get_rect()
        otvet3_rect.midtop = (190, 212)
        game.play_surface.blit(otvet3_surf, otvet3_rect)

        while answering:
            pygame.draw.rect(game.play_surface, (255, 255, 255),
                             pygame.Rect(55, 70, 200, int(self.screen_height * 5.22 // 100)))
            pygame.draw.rect(game.play_surface, (0, 0, 0), pygame.Rect(55, 70, 190, 190), 3)

            x_coord = self.screen_width * 9.72 / 100
            y_coord = self.screen_height * 17.39 / 100
            ques_surf, ques_rect = set_text_global(f'Осталось времени: {time}', int(self.screen_height * 5.22 // 100),
                                                   x_coord, y_coord, "black")
            game.play_surface.blit(ques_surf, ques_rect)

            pygame.display.flip()
            game.fps.tick(1)

            time -= 1
            if time == 0:
                LIVES -= 1
                if LIVES == 0:
                    self.end()
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
                            LIVES -= 1
                            if LIVES == 0:
                                self.end()
                            return 0

    def end(self):
        pygame.draw.rect(
            game.play_surface, (255, 255, 255), pygame.Rect(
                50, 10, 200, 200))
        pygame.draw.rect(
            game.play_surface, (255, 255, 255), pygame.Rect(
                50, 80, 230, 210))
        pygame.display.flip()
        game.game_over()


def playing():
    global CURRENT_SNAKE
    game1 = MainGame()
    snake = Snake()
    food = Food(game1.screen_width, game1.screen_height)

    game = Game_palce()
    game.create_surface()

    while True:
        snake.dir = game.event(snake.change_dir)

        snake.change_dir()
        snake.head_position()
        food.food_pos = snake.snake_body_create(food.food_pos, game.screen_width, game.screen_height)
        snake.draw_snake(game.play_surface)

        food.draw_food(game.play_surface)

        snake.check_collision(
            game.game_over, game.screen_width, game.screen_height)

        game.text_score_and_lives()
        pygame.display.flip()
        game.fps.tick(15 * CURRENT_SNAKE[3])


game1 = MainGame()
snake = Snake()
food = Food(game1.screen_width, game1.screen_height)

game1.create_surface()

game = Game_palce()
game.create_surface()
print("прошёл сюда")
while True:
    snake.dir = game.event(snake.change_dir)

    snake.change_dir()
    snake.head_position()
    food.food_pos = snake.snake_body_create(food.food_pos, game.screen_width, game.screen_height)
    snake.draw_snake(game.play_surface)

    food.draw_food(game.play_surface)

    snake.check_collision(
        game.game_over, game.screen_width, game.screen_height)

    game.text_score_and_lives()
    pygame.display.flip()
    game.fps.tick(15 * CURRENT_SNAKE[3])
