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