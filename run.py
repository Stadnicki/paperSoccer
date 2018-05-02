import pygame, random

RADIUS = 15
MARGIN = 30
ROWS = 11
COLUMNS = 9
TEXTPOS = ((MARGIN + RADIUS) * 11 + MARGIN)


def colourPicker(x):
    return {
        0: (0, 0, 0),
        1: (255, 100, 100),
        2: (255, 255, 255),
        3: (0, 120, 20),
        4: (255, 0, 0),
        5: (0, 0, 255)
    }[x]

# 0 black
# 1 bright red
# 2 white
# 4 red
# 5 blue
class TextField:
    def __init__(self, surface):
        self.stringNum = 0
        self.strings = {
                0: 'Player 1 turn',
                1: 'Player 2 turn',
                2: 'Player 1 wins',
                3: 'Player 2 wins'}
        self.surface = surface
        self.resultFont = pygame.font.SysFont("arial", 50)

    def start(self):
        self.stringNum = random.randint(0, 1)
        if self.stringNum == 0:
            self.updateTextField(0)
        else:
            self.updateTextField(1)

    def updateTextField(self, stringNumber):
        self.stringNum = stringNumber
        self.surface.fill(colourPicker(3))
        resultText = self.resultFont.render(self.strings[stringNumber], 1, colourPicker(5))
        self.surface.blit(resultText, ((self.surface.get_width() - resultText.get_width()) / 2,
                                       (self.surface.get_height() - 1.5 * resultText.get_height())))



class GameWindow:
    def __init__(self):
        pygame.init()
        self.gameClock = pygame.time.Clock()
        self.Window = pygame.display.set_mode(((COLUMNS*(RADIUS+MARGIN)+RADIUS), 600))
        self.Window.fill(colourPicker(3))
        pygame.display.flip()
        pygame.display.set_caption('Paper Soccer')

class GameField:
    def __init__(self, surface, textField):
        self.textField = textField
        self.surface = surface
        self.field = []
        self.fieldFunction = []
        self.recentBallPos = [4, 5]
        self.previousColumn = 0
        self.previousRow = 0
        for row in range(ROWS):
            self.field.append([])
            self.fieldFunction.append([])
            for column in range(COLUMNS):
                self.field[row].append(2)
                self.fieldFunction[row].append(0)

        self.fieldFunction[0][3] = self.fieldFunction[0][4] = self.fieldFunction[0][5] = 3
        # number 3 - player 1 wins
        self.field[0][3] = self.field[0][4] = self.field[0][5] = 5
        # number 4 - player 2 wins
        self.fieldFunction[10][3] = self.fieldFunction[10][4] = self.fieldFunction[10][5] = 4
        self.field[10][3] = self.field[10][4] = self.field[10][5] = 5

    def draw(self):
        for row in range(ROWS):
            for column in range(COLUMNS):
                colour = colourPicker(self.field[row][column])
                pygame.draw.circle(self.surface, colour,
                                   (((MARGIN + RADIUS) * column + MARGIN),
                                    ((MARGIN + RADIUS) * row + MARGIN)), 7)
        pygame.draw.circle(self.surface, colourPicker(4),
                           (((MARGIN + RADIUS) * self.recentBallPos[0] + MARGIN),
                            ((MARGIN + RADIUS) * self.recentBallPos[1] + MARGIN)), 7)



    def mouseClicked(self):
        pos = pygame.mouse.get_pos()
        column = pos[0] // (RADIUS + MARGIN)
        row = pos[1] // (RADIUS + MARGIN)
        if column < COLUMNS and row < ROWS:
            print(abs(column-self.recentBallPos[0]), '   ', abs(row - self.recentBallPos[1]))
            if(abs(column-self.recentBallPos[0]) <= 1 and
                    abs(row - self.recentBallPos[1]) <= 1 and
                    (self.recentBallPos[0] != column or self.recentBallPos[1] != row )):
                self.colourCircle(4)
                self.field[self.recentBallPos[1]][self.recentBallPos[0]] = 0
                self.recentBallPos[0] = column
                self.recentBallPos[1] = row
                print('field function number', self.fieldFunction[row][column])
                if self.fieldFunction[row][column] == 3:
                    self.textField.updateTextField(2)
                elif self.fieldFunction[row][column] == 4:
                    self.textField.updateTextField(3)
                else:
                    tempStringNum = not self.textField.stringNum
                    self.textField.updateTextField(tempStringNum)
                self.fieldFunction[row][column] = 1


    def colourCircle(self, colourNum):
        pos = pygame.mouse.get_pos()
        column = pos[0] // (RADIUS + MARGIN)
        row = pos[1] // (RADIUS + MARGIN)
        if column < COLUMNS and row < ROWS:
            self.previousColumn = column
            self.previousRow = row
            self.field[row][column] = colourNum
            print("Clicked on ", pos, " coord: ", row, column)

    def reWhite(self):
        if self.field[self.previousRow][self.previousColumn] != 0:
            self.field[self.previousRow][self.previousColumn] = 2


def mainLoop():
    exitFlag = False;
    gameWindow = GameWindow()
    textField = TextField(gameWindow.Window)
    gameField = GameField(gameWindow.Window, textField)
    textField.start()
    while not exitFlag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitFlag = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                gameField.mouseClicked()

        gameField.draw()
        pygame.display.update()


def main():
    mainLoop()


if  __name__ == "__main__":
    main()
