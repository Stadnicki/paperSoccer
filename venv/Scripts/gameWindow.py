import pygame
import random
import gameMenu
from config import *
from resultsFile import *
from time import gmtime, strftime, time



class TextField:
    def __init__(self, surface, nicks):
        self.nicks = nicks
        print('nicks: ', nicks[0], nicks[1])
        self.string_num = 0
        self.strings = {
            0: (str(nicks[0]) + '\'s turn').center(50),
            1: (str(nicks[1]) + '\'s turn').center(50),
            2: (str(nicks[0]) + ' wins').center(50),
            3: (str(nicks[1]) + ' wins').center(50)}
        self.surface = surface
        self.resultFont = pygame.font.SysFont("Georgia", 30)

    def start(self):
        self.string_num = random.randint(0, 1)
        if self.string_num == 0:
            self.update_text_field(0)
        else:
            self.update_text_field(1)

    def get_winner(self):
        if self.string_num == 2:
            return self.nicks[0]
        elif self.string_num == 3:
            return self.nicks[1]
        else:
            return 'error'

    def get_loser(self):
        if self.string_num == 2:
            return self.nicks[1]
        elif self.string_num == 3:
            return self.nicks[0]
        else:
            return 'error'

    def update_text_field(self, string_number):
        self.string_num = string_number
        text_colour = 5
        if string_number == 0 or string_number == 2:
            text_colour = 4
        result_text = self.resultFont.render(self.strings[string_number], 1, colour_picker(text_colour),
                                             colour_picker(3))
        self.surface.blit(result_text, ((self.surface.get_width() - result_text.get_width()) / 2,
                                        (self.surface.get_height() - 2 * result_text.get_height())))


class GameWindow:
    def __init__(self):
        pygame.init()
        self.gameClock = pygame.time.Clock()
        self.Window = pygame.display.set_mode(((COLUMNS * (RADIUS + MARGIN) + RADIUS), 600))
        self.Window.fill(colour_picker(3))
        pygame.display.flip()
        pygame.display.set_caption('Paper Soccer')


# field functions:
# 0 - free field
# 1 - visited
# 6 - end line
# 7 - side line


def coords_to_num(row, column):
    # print(row, " ", column, " is ", row * COLUMNS + column)
    return row * COLUMNS + column


def in_field(row, column):
    if 0 <= row < 11 and 0 <= column < 9:
        return True
    return False


def in_range(row, column, from_row, from_column):
    if in_field(row, column) and (abs(column - from_column) <= 1 and
                                  abs(row - from_row) <= 1 and (from_column != column or from_row != row)):
        return True
    else:
        return False


class GameField:
    def __init__(self, surface, text_field):
        self.textField = text_field
        self.surface = surface
        self.field = []
        self.field_function = []
        self.connections = []
        self.recent_ball_pos = [4, 5]
        self.start_time = time()
        self.game_time = ""
        self.endOfGame = False
        self.prepare()

    def prepare(self):
        for x in range(ROWS * COLUMNS):
            self.connections.append([])

        for row in range(ROWS):
            self.field.append([])
            self.field_function.append([])
            for column in range(COLUMNS):
                self.field[row].append(2)
                self.field_function[row].append(0)
                self.field_function[row].append([])

        for column in range(COLUMNS):
            self.field_function[0][column] = 6
            self.field_function[ROWS - 1][column] = 6
            self.field[0][column] = 6
            self.field[ROWS - 1][column] = 6

        for row in range(ROWS):
            self.field_function[row][0] = 7
            self.field_function[row][COLUMNS - 1] = 7
            self.field[row][0] = 6
            self.field[row][COLUMNS - 1] = 6

            self.field_function[0][0] = self.field_function[0][COLUMNS - 1] = \
                self.field_function[ROWS - 1][0] = self.field_function[ROWS - 1][COLUMNS - 1] = 8

        for row in range(ROWS - 1):
            pygame.draw.line(self.surface, colour_picker(6),
                             (MARGIN, (MARGIN + RADIUS) * row + MARGIN),
                             (MARGIN, (MARGIN + RADIUS) * (row + 1) + MARGIN), SIDELINE_TH)
            pygame.draw.line(self.surface, colour_picker(6),
                             ((MARGIN + RADIUS) * (COLUMNS - 1) + MARGIN, (MARGIN + RADIUS) * row + MARGIN),
                             ((MARGIN + RADIUS) * (COLUMNS - 1) + MARGIN, (MARGIN + RADIUS) * (row + 1) + MARGIN), SIDELINE_TH)

        for column in range(COLUMNS - 1):
            pygame.draw.line(self.surface, colour_picker(6),
                             ((MARGIN + RADIUS) * column + MARGIN, MARGIN),
                             ((MARGIN + RADIUS) * (column + 1) + MARGIN, MARGIN), SIDELINE_TH)
            pygame.draw.line(self.surface, colour_picker(6),
                             ((MARGIN + RADIUS) * column + MARGIN, (MARGIN + RADIUS) * (ROWS - 1) + MARGIN),
                             ((MARGIN + RADIUS) * (column + 1) + MARGIN, (MARGIN + RADIUS) * (ROWS - 1) + MARGIN), SIDELINE_TH)

        # number 3 - player 1 wins
        self.field_function[0][3] = self.field_function[0][4] = self.field_function[0][5] = 3
        self.field[0][3] = self.field[0][4] = self.field[0][5] = 5

        # number 4 - player 2 wins
        self.field_function[10][3] = self.field_function[10][4] = self.field_function[10][5] = 4
        self.field[10][3] = self.field[10][4] = self.field[10][5] = 4

        self.field_function[5][4] = 1  # start field marked as

    def draw(self):
        for row in range(ROWS):
            for column in range(COLUMNS):
                colour = colour_picker(self.field[row][column])
                pygame.draw.circle(self.surface, colour,
                                   (((MARGIN + RADIUS) * column + MARGIN),
                                    ((MARGIN + RADIUS) * row + MARGIN)), 7)
        self.color_current_player()

    def color_current_player(self):
        # color current field
        current_player_color = 4
        if self.textField.string_num in [1, 2]:
            current_player_color = 5
        pygame.draw.circle(self.surface, colour_picker(current_player_color),
                           (((MARGIN + RADIUS) * self.recent_ball_pos[0] + MARGIN),
                            ((MARGIN + RADIUS) * self.recent_ball_pos[1] + MARGIN)), 7)

    def forbidden_movement(self, row, column, from_row, from_column):
        if (from_row == row == 0 or from_column == row == (ROWS - 1)) or \
                (from_column == column == 0 or from_column == column == (COLUMNS - 1)) or \
                (coords_to_num(row, column) in self.connections[
                    coords_to_num(from_row, from_column)]) or \
                ((from_row == 0 or from_row == (ROWS - 1)) and (
                        self.field_function[row][column] == 6)) or \
                ((from_column == 0 or from_column == (COLUMNS - 1)) and
                 (self.field_function[row][column] == 7)):
            # print('from', coords_to_num(from_row, from_column), ' to ', coords_to_num(row, column), ' is forbidden')
            return True
        # print('from', coords_to_num(from_row, from_column), ' to ', coords_to_num(row, column), ' is not forbidden')
        return False

    def possible_movement(self, row, column):
        counter = 0
        adj = [(row - 1, column - 1), (row - 1, column), (row - 1, column + 1), (row, column - 1),
               (row, column + 1), (row + 1, column - 1), (row + 1, column), (row + 1, column + 1)]
        for coordinates in adj:
            if in_field(coordinates[0], coordinates[1]) and not self.forbidden_movement(coordinates[0], coordinates[1], row, column):
                counter += 1

        print('for ', row, '-', column, ' counter: ', counter)
        return counter

    def select_line_color(self):
        line_color = 4
        if self.textField.string_num == 1:
            line_color = 5
        return line_color

    def draw_movement_line(self, row, column, from_row, from_column):
        self.field[from_row][from_column] = 0
        pygame.draw.line(self.surface, colour_picker(self.select_line_color()),
                         ((MARGIN + RADIUS) * from_column + MARGIN,
                          (MARGIN + RADIUS) * from_row + MARGIN),
                         ((MARGIN + RADIUS) * column + MARGIN, (MARGIN + RADIUS) * row + MARGIN), MOVEMENT_LINE)

    def long_movement(self, row, column):
        if self.field_function[row][column] in [1, 6, 7, 8]:
            return True
        else:
            return False

    def check_if_goal(self, row, column):
        if self.field_function[row][column] == 3:
            self.textField.update_text_field(2)
            return True
        elif self.field_function[row][column] == 4:
            self.textField.update_text_field(3)
            return True
        return False

    def change_player(self):
        temp_string_num = not self.textField.string_num
        self.textField.update_text_field(temp_string_num)

    def add_connection(self, row, column, from_row, from_column):
        self.connections[coords_to_num(row, column)].append(
            coords_to_num(from_row, from_column))

        self.connections[coords_to_num(from_row, from_column)].append(
            coords_to_num(row, column))

    def if_blocked(self, row, column):
        if self.possible_movement(row, column) == 0:
            winner_string = 3
            if self.textField.string_num == 1:
                winner_string = 2
            self.textField.update_text_field(winner_string)
            self.endOfGame = True

    def get_game_time(self):
        return str(round(time()-self.start_time))

    def movement_processing(self, row, column):
        if in_range(row, column, self.recent_ball_pos[1], self.recent_ball_pos[0]):
            print('clicked field function number: ', self.field_function[row][column])

            # if chosen movement is forbidden then do nothing
            if self.forbidden_movement(row, column, self.recent_ball_pos[1], self.recent_ball_pos[0]):
                return

            self.draw_movement_line(row, column, self.recent_ball_pos[1], self.recent_ball_pos[0])

            if self.check_if_goal(row, column):
                self.endOfGame = True
            elif self.long_movement(row, column):
                print("long movement")
                pass
            else:
                print("changing player")
                self.change_player()

            self.field_function[row][column] = 1
            self.add_connection(row, column, self.recent_ball_pos[1], self.recent_ball_pos[0])

            self.if_blocked(row, column)

            self.recent_ball_pos[0] = column
            self.recent_ball_pos[1] = row

    def mouse_clicked(self):
        pos = pygame.mouse.get_pos()
        column = pos[0] // (RADIUS + MARGIN)
        row = pos[1] // (RADIUS + MARGIN)
        self.movement_processing(row, column)


def enter_results(text_field, game_field, res_file):
    if text_field.string_num == 2 or text_field.string_num == 3:
        res_file.add_result( text_field.get_winner() + " won against " + text_field.get_loser() +
                             "\n\t" + "-- date: " + strftime("%Y-%m-%d %H:%M:%S", gmtime())+
                             "\n\t" + "-- game time: " + game_field.get_game_time() + " s")


def main_loop(nicks):
    res_file = ResultsFile('results')
    exit_flag = False
    game_window = GameWindow()
    text_field = TextField(game_window.Window, nicks)
    game_field = GameField(game_window.Window, text_field)
    text_field.start()
    while not exit_flag:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and game_field.endOfGame is True:
                enter_results(text_field,game_field, res_file)
                main_loop(nicks)
            if event.type == pygame.QUIT:
                enter_results(text_field, game_field, res_file)
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game_field.mouse_clicked()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    enter_results(text_field, game_field, res_file)
                    pygame.quit()
                    gameMenu.main()
                elif event.key == pygame.K_r:
                    main_loop(nicks)

        game_field.draw()
        pygame.display.update()
    gameMenu.main()
