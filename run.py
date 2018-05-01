import pygame, sys;

WIDTH = 15
HEIGHT = 15
MARGIN = 30
ROWS = 11
COLUMNS = 9


def colourPicker(x):
    return {
        0: (0, 0, 0),
        1: (255, 100, 100),
        2: (255, 255, 255),
        3: (0, 120, 20),
        4: (255, 0, 0),
    }[x]


class GameWindow:
    def __init__(self):
        pygame.init()
        self.gameClock = pygame.time.Clock()
        self.Window = pygame.display.set_mode((800, 600))
        self.Window.fill(colourPicker(3))
        pygame.display.flip()
        pygame.display.set_caption('Paper Soccer')

class GameField:
    def __init__(self):
        self.field = []
        self.recentBallPos = [4, 5]
        self.previousColumn = 0
        self.previousRow = 0
        for row in range(ROWS):
            self.field.append([])
            for column in range(COLUMNS):
                self.field[row].append(2)

    def draw(self, surface):
        for row in range(ROWS):
            for column in range(COLUMNS):
                colour = colourPicker(self.field[row][column])
                pygame.draw.circle(surface, colour,
                                   (((MARGIN + WIDTH) * column + MARGIN),
                                    ((MARGIN + HEIGHT) * row + MARGIN)), 7)
        pygame.draw.circle(surface, colourPicker(4),
                           (((MARGIN + WIDTH) * self.recentBallPos[0] + MARGIN),
                            ((MARGIN + HEIGHT) * self.recentBallPos[1] + MARGIN)), 7)

    def mouseClicked(self):
        pos = pygame.mouse.get_pos()
        column = pos[0] // (WIDTH + MARGIN)
        row = pos[1] // (HEIGHT + MARGIN)
        if column < COLUMNS and row < ROWS:
            self.colourCircle(4)
            self.field[self.recentBallPos[1]][self.recentBallPos[0]] = 0
            self.recentBallPos[0] = column
            self.recentBallPos[1] = row

    def colourCircle(self, colourNum):
        pos = pygame.mouse.get_pos()
        column = pos[0] // (WIDTH + MARGIN)
        row = pos[1] // (HEIGHT + MARGIN)
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
    gameField = GameField()
    while not exitFlag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitFlag = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                gameField.colourCircle(0)
            elif event.type == pygame.MOUSEMOTION:
                gameField.mouseover()

        gameField.draw(gameWindow.Window)
        pygame.display.update()




def mainLoop():
    exitFlag = False;
    gameWindow = GameWindow()
    gameField = GameField()
    while not exitFlag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitFlag = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                gameField.mouseClicked()

        gameField.draw(gameWindow.Window)
        pygame.display.update()


def main():
    mainLoop()


if  __name__ == "__main__":
    main()
