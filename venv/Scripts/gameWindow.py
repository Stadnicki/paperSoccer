import pygame
import random
import gameMenu
from config import *
from resultsFile import *
from time import gmtime, strftime


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


class GameField:
    def __init__(self, surface, text_field):
        self.textField = text_field
        self.surface = surface
        self.field = []
        self.field_function = []
        self.connections = []
        self.recent_ball_pos = [4, 5]
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
                             (MARGIN, (MARGIN + RADIUS) * (row + 1) + MARGIN), 2)
            pygame.draw.line(self.surface, colour_picker(6),
                             ((MARGIN + RADIUS) * (COLUMNS - 1) + MARGIN, (MARGIN + RADIUS) * row + MARGIN),
                             ((MARGIN + RADIUS) * (COLUMNS - 1) + MARGIN, (MARGIN + RADIUS) * (row + 1) + MARGIN), 2)

        for column in range(COLUMNS - 1):
            pygame.draw.line(self.surface, colour_picker(6),
                             ((MARGIN + RADIUS) * column + MARGIN, MARGIN),
                             ((MARGIN + RADIUS) * (column + 1) + MARGIN, MARGIN), 2)
            pygame.draw.line(self.surface, colour_picker(6),
                             ((MARGIN + RADIUS) * column + MARGIN, (MARGIN + RADIUS) * (ROWS - 1) + MARGIN),
                             ((MARGIN + RADIUS) * (column + 1) + MARGIN, (MARGIN + RADIUS) * (ROWS - 1) + MARGIN), 2)

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

        # color recent move field
        current_player_color = 4
        if self.textField.string_num == 1:
            current_player_color = 5
        pygame.draw.circle(self.surface, colour_picker(current_player_color),
                           (((MARGIN + RADIUS) * self.recent_ball_pos[0] + MARGIN),
                            ((MARGIN + RADIUS) * self.recent_ball_pos[1] + MARGIN)), 7)

    def forbidden_movement(self, row, column, fromRow, fromColumn):
        print('function forbidden movement, conections ', self.connections[
                    coords_to_num(row, column)])
        if (fromRow == row == 0 or fromColumn == row == (ROWS - 1)) or \
                (fromColumn == column == 0 or fromColumn == column == (COLUMNS - 1)) or \
                (coords_to_num(row, column) in self.connections[
                    coords_to_num(fromRow, fromColumn)]) or \
                ((fromRow == 0 or fromRow == (ROWS - 1)) and (
                        self.field_function[row][column] == 6)) or \
                ((fromColumn == 0 or fromColumn == (COLUMNS - 1)) and
                 (self.field_function[row][column] == 7)):
            print('from', coords_to_num(fromRow, fromColumn),' to ', coords_to_num(row, column), ' is forbidden')
            return True
        print('from', coords_to_num(fromRow, fromColumn),' to ', coords_to_num(row, column), ' is not forbidden')
        return False

    def possible_movement(self, row, column):
        counter = 0
        adj = [(row-1, column-1), (row-1, column), (row-1, column+1), (row, column-1),
               (row, column+1), (row+1, column-1), (row+1, column), (row+1, column+1)]
        for coords in adj:
            if in_field(coords[0], coords[1]) and not self.forbidden_movement(coords[0], coords[1], row, column):
                counter += 1
                # print('from ', row ,'-',column,' to ', coords[0], '-', coords[1], ' is a possible movement')

        print('for ', row, '-',column, ' counter: ', counter)
        return counter

    def mouse_clicked(self):
        pos = pygame.mouse.get_pos()
        column = pos[0] // (RADIUS + MARGIN)
        row = pos[1] // (RADIUS + MARGIN)
        if in_field(row, column):
            if (abs(column - self.recent_ball_pos[0]) <= 1 and
                    abs(row - self.recent_ball_pos[1]) <= 1 and

                    (self.recent_ball_pos[0] != column or self.recent_ball_pos[1] != row)):
                print('clicked field function: ', self.field_function[row][column])

                coords_to_num(row, column)
                print('field function number', self.field_function[row][column])

                print("current: ", coords_to_num(row, column))
                print("array ", self.connections[coords_to_num(self.recent_ball_pos[1], self.recent_ball_pos[0])])

                if self.forbidden_movement(row, column, self.recent_ball_pos[1], self.recent_ball_pos[0]):
                    return

                line_color = 4
                if self.textField.string_num == 1:
                    line_color = 5

                self.colour_circle(4)
                self.field[self.recent_ball_pos[1]][self.recent_ball_pos[0]] = 0
                pygame.draw.line(self.surface, colour_picker(line_color),
                                 ((MARGIN + RADIUS) * self.recent_ball_pos[0] + MARGIN,
                                  (MARGIN + RADIUS) * self.recent_ball_pos[1] + MARGIN),
                                 ((MARGIN + RADIUS) * column + MARGIN, (MARGIN + RADIUS) * row + MARGIN), 2)

                if self.field_function[row][column] == 3:
                    self.textField.update_text_field(2)
                    self.endOfGame = True
                elif self.field_function[row][column] == 4:
                    self.textField.update_text_field(3)
                    self.endOfGame = True
                elif self.field_function[row][column] == 1:
                    pass
                elif self.field_function[row][column] == 6 or self.field_function[row][column] == 7:
                    pass
                else:
                    temp_string_num = not self.textField.string_num
                    self.textField.update_text_field(temp_string_num)
                self.field_function[row][column] = 1

                self.connections[coords_to_num(row, column)].append(
                    coords_to_num(self.recent_ball_pos[1], self.recent_ball_pos[0]))
                print("from ", coords_to_num(row, column), "to ",
                      coords_to_num(self.recent_ball_pos[1], self.recent_ball_pos[0]))

                self.connections[coords_to_num(self.recent_ball_pos[1], self.recent_ball_pos[0])].append(
                    coords_to_num(row, column))

                print("from ", coords_to_num(self.recent_ball_pos[1], self.recent_ball_pos[0]), "to ",
                      coords_to_num(row, column))

                if self.possible_movement(row, column) == 0:
                    winner_string = 2
                    if self.textField.string_num == 1:
                        winner_string = 3
                    self.textField.update_text_field(winner_string)
                    self.endOfGame = True

                self.recent_ball_pos[0] = column
                self.recent_ball_pos[1] = row

    def colour_circle(self, colour_num):
        pos = pygame.mouse.get_pos()
        column = pos[0] // (RADIUS + MARGIN)
        row = pos[1] // (RADIUS + MARGIN)
        if column < COLUMNS and row < ROWS:
            self.field[row][column] = colour_num
            print("Clicked on ", pos, " coord: ", row, column)


def enter_results(text_field, res_file):
    if text_field.string_num == 2 or text_field.string_num == 3:
        res_file.add_result(strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " - " +
                            text_field.get_winner() + " won against " + text_field.get_loser())


def main_loop(nicks):
    res_file = ResultsFile('results')
    exit_flag = False
    game_window = GameWindow()
    text_field = TextField(game_window.Window, nicks)
    game_field = GameField(game_window.Window, text_field)
    text_field.start()
    while not exit_flag:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and game_field.endOfGame == True:
                enter_results(text_field, res_file)
                main_loop(nicks)
            if event.type == pygame.QUIT:
                enter_results(text_field, res_file)
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game_field.mouse_clicked()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    enter_results(text_field, res_file)
                    pygame.quit()
                    gameMenu.main()
                elif event.key == pygame.K_r:
                    main_loop(nicks)

        game_field.draw()
        pygame.display.update()
    gameMenu.main()
