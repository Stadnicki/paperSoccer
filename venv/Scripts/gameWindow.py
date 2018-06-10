import pygame, random, gameMenu

RADIUS = 15
MARGIN = 30
ROWS = 11
COLUMNS = 9
TEXTPOS = ((MARGIN + RADIUS) * 11 + MARGIN)


def colour_picker(x):
    return {
        0: (0, 0, 0),
        1: (255, 100, 100),
        2: (0, 100, 0),
        3: (0, 120, 20),
        4: (255, 0, 0),
        5: (0, 0, 255),
        6: (255, 255, 255),
        7: (255,255,0),
    }[x]

# 0 black
# 1 bright red
# 2 dark green
# 3 green
# 4 red
# 5 blue
# 6 white
# 7 yellow

class TextField:
    def __init__(self, surface, nicks):
        print ('nicks: ', nicks[0], nicks[1])
        self.string_num = 0
        self.strings = {
                0: (str(nicks[0])+'\'s turn').center(50),
                1: (str(nicks[1])+'\'s turn').center(50),
                2: (str(nicks[0])+' wins').center(50),
                3: (str(nicks[1])+' wins').center(50)}
        self.surface = surface
        self.resultFont = pygame.font.SysFont("Georgia", 30)

    def start(self):
        self.string_num = random.randint(0, 1)
        if self.string_num == 0:
            self.update_text_field(0)
        else:
            self.update_text_field(1)

    def update_text_field(self, string_number):
        self.string_num = string_number
        text_colour = 5
        if string_number == 0 or string_number == 2:
            text_colour = 4
        result_text = self.resultFont.render(self.strings[string_number], 1, colour_picker(text_colour), colour_picker(3))
        self.surface.blit(result_text, ((self.surface.get_width() - result_text.get_width()) / 2,
                                       (self.surface.get_height() - 2 * result_text.get_height())))


class GameWindow:
    def __init__(self):
        pygame.init()
        self.gameClock = pygame.time.Clock()
        self.Window = pygame.display.set_mode(((COLUMNS*(RADIUS+MARGIN)+RADIUS), 600))
        self.Window.fill(colour_picker(3))
        pygame.display.flip()
        pygame.display.set_caption('Paper Soccer')

# field functions:
# 0 - free field
# 1 - visited
# 6 - side line

class GameField:
    def __init__(self, surface, text_field):
        self.textField = text_field
        self.surface = surface
        self.field = []
        self.field_function = []
        self.connections = []
        self.recent_ball_pos = [4, 5]
        self.previous_column = 0
        self.previous_row = 0
        self.endOfGame = False

        for x in range(ROWS*COLUMNS):
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
            self.field_function[ROWS-1][column] = 6
            self.field[0][column] = 6
            self.field[ROWS-1][column] = 6

        for row in range(ROWS):
            self.field_function[row][0] = 7
            self.field_function[row][COLUMNS-1] = 7
            self.field[row][0] = 6
            self.field[row][COLUMNS - 1] = 6

            self.field_function[0][0] = self.field_function[0][COLUMNS-1] = self.field_function[ROWS-1][0] =  self.field_function[ROWS-1][COLUMNS-1] = 8

        for row in range(ROWS-1):
            pygame.draw.line(self.surface, colour_picker(6),
                             ( MARGIN, (MARGIN + RADIUS) * row + MARGIN),
                             ( MARGIN, (MARGIN + RADIUS) * (row+1) + MARGIN), 2)
            pygame.draw.line(self.surface, colour_picker(6),
                             ( (MARGIN + RADIUS) * (COLUMNS-1) + MARGIN, (MARGIN + RADIUS) * row + MARGIN),
                             ( (MARGIN + RADIUS) * (COLUMNS-1) + MARGIN, (MARGIN + RADIUS) * (row+1) + MARGIN), 2)

        for column in range(COLUMNS - 1):
            pygame.draw.line(self.surface, colour_picker(6),
                             ((MARGIN + RADIUS) * column + MARGIN, MARGIN),
                             ((MARGIN + RADIUS) * (column + 1) + MARGIN, MARGIN), 2)
            pygame.draw.line(self.surface, colour_picker(6),
                             ((MARGIN + RADIUS) * column + MARGIN,(MARGIN + RADIUS) * (ROWS-1) + MARGIN),
                             ((MARGIN + RADIUS) * (column + 1) + MARGIN, (MARGIN + RADIUS) * (ROWS-1) + MARGIN), 2)

        # number 3 - player 1 wins
        self.field_function[0][3] = self.field_function[0][4] = self.field_function[0][5] = 3
        self.field[0][3] = self.field[0][4] = self.field[0][5] = 5

        # number 4 - player 2 wins
        self.field_function[10][3] = self.field_function[10][4] = self.field_function[10][5] = 4
        self.field[10][3] = self.field[10][4] = self.field[10][5] = 4

        self.field_function[5][4] = 1 # start field marked as

    def draw(self):
        for row in range(ROWS):
            for column in range(COLUMNS):
                colour = colour_picker(self.field[row][column])
                pygame.draw.circle(self.surface, colour,
                                   (((MARGIN + RADIUS) * column + MARGIN),
                                    ((MARGIN + RADIUS) * row + MARGIN)), 7)
        pygame.draw.circle(self.surface, colour_picker(7),
                           (((MARGIN + RADIUS) * self.recent_ball_pos[0] + MARGIN),
                            ((MARGIN + RADIUS) * self.recent_ball_pos[1] + MARGIN)), 7)


    def coords_to_num(self, row, column):
        print(row, " ", column, " is ", row*COLUMNS+column)
        return row*COLUMNS+column

    def mouse_clicked(self):
        pos = pygame.mouse.get_pos()
        column = pos[0] // (RADIUS + MARGIN)
        row = pos[1] // (RADIUS + MARGIN)
        if column < COLUMNS and row < ROWS:
            print(abs(column-self.recent_ball_pos[0]), '   ', abs(row - self.recent_ball_pos[1]))
            if(abs(column-self.recent_ball_pos[0]) <= 1 and
                    abs(row - self.recent_ball_pos[1]) <= 1 and

                    (self.recent_ball_pos[0] != column or self.recent_ball_pos[1] != row )):
                print ('clicked field function: ', self.field_function[row][column])

                self.coords_to_num(row, column)
                print('field function number', self.field_function[row][column])

                print("current: ", self.coords_to_num(row, column))
                print("array ", self.connections[self.coords_to_num(self.recent_ball_pos[1], self.recent_ball_pos[0])])

                if(self.recent_ball_pos[1] == row == 0 or self.recent_ball_pos[1] == row == (ROWS-1) or
                    self.recent_ball_pos[0] == column == 0 or self.recent_ball_pos[0] == column == (COLUMNS-1)):
                    return

                if self.coords_to_num(row, column) in self.connections[self.coords_to_num(self.recent_ball_pos[1], self.recent_ball_pos[0])]:
                    return

                if (self.recent_ball_pos[1] == 0 or self.recent_ball_pos[1] == (ROWS-1)) and \
                        (self.field_function[row][column] == 6):
                    return

                if (self.recent_ball_pos[0] == 0 or self.recent_ball_pos[0] == (COLUMNS-1)) and \
                        (self.field_function[row][column] == 7):
                    return

                self.colour_circle(4)
                self.field[self.recent_ball_pos[1]][self.recent_ball_pos[0]] = 0
                pygame.draw.line(self.surface, colour_picker(0),
                                 ((MARGIN + RADIUS)*self.recent_ball_pos[0]+MARGIN,
                                  (MARGIN + RADIUS)*self.recent_ball_pos[1]+MARGIN),
                                 ((MARGIN + RADIUS)*column+MARGIN, (MARGIN + RADIUS)*row+MARGIN), 2)

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

                self.connections[self.coords_to_num(row, column)].append(
                    self.coords_to_num(self.recent_ball_pos[1], self.recent_ball_pos[0]))
                print("from ", self.coords_to_num(row, column), "to ", self.coords_to_num(self.recent_ball_pos[1], self.recent_ball_pos[0]))

                self.connections[self.coords_to_num(self.recent_ball_pos[1], self.recent_ball_pos[0])].append(
                    self.coords_to_num(row, column))

                print("from ",self.coords_to_num(self.recent_ball_pos[1], self.recent_ball_pos[0]), "to ",
                      self.coords_to_num(row, column))


                self.recent_ball_pos[0] = column
                self.recent_ball_pos[1] = row

    def colour_circle(self, colour_num):
        pos = pygame.mouse.get_pos()
        column = pos[0] // (RADIUS + MARGIN)
        row = pos[1] // (RADIUS + MARGIN)
        if column < COLUMNS and row < ROWS:
            self.previous_column = column
            self.previous_row = row
            self.field[row][column] = colour_num
            print("Clicked on ", pos, " coord: ", row, column)


def main_loop(nicks):
    exit_flag = False;
    game_window = GameWindow()
    text_field = TextField(game_window.Window, nicks)
    game_field = GameField(game_window.Window, text_field)
    text_field.start()
    while not exit_flag:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and game_field.endOfGame == True:
                main_loop(nicks)
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game_field.mouse_clicked()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    pygame.quit()
                    gameMenu.main()
                elif event.key == pygame.K_r:
                    main_loop(nicks)

        game_field.draw()
        pygame.display.update()
    gameMenu.main()
