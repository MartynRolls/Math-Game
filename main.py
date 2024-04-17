from Core import Game
import pygame
from sys import exit
from math import sin, cos, pi

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
colours = [(210, 215, 220), (250, 225, 120), (165, 195, 100), (180, 195, 240), (185, 130, 195)]

orderSelected = []
circle = {'radius': [110 for _ in range(6)],
          'centre': [(0, 0) for _ in range(6)]}
level = 0
game = Game(0)
colour1 = colours[0]
colour2 = colours[1]
total = 0

X, Y = 600, 600
screen = pygame.display.set_mode((X, Y), pygame.RESIZABLE)
clock = pygame.time.Clock()

while True:
    screen.fill(white)
    # Setting needed variables for detecting mouse position
    X, Y = pygame.display.get_surface().get_size()
    circleSize = min(X, Y) / 10
    distance = circleSize * 3
    X /= 2
    Y /= 2 / 1.15

    for i in range(6):
        circleX = X - distance * sin(pi * i / 3)
        circleY = Y - distance * cos(pi * i / 3)
        circle['centre'][i] = (circleX, circleY)

    for i, rad in enumerate(circle['radius']):
        if i in orderSelected and rad < 120:
            circle['radius'][i] += 1
        elif i not in orderSelected and rad > 110:
            circle['radius'][i] -= 2

    # Checking events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Detecting if the mouse pointer clicked, and its location
        elif event.type == pygame.MOUSEBUTTONDOWN:
            Xpos, Ypos = pygame.mouse.get_pos()

            for i in range(6):
                circleX, circleY = circle['centre'][i]

                if ((circleX - circleSize * 1.3 < Xpos < circleX + circleSize * 1.3) and
                        (circleY - circleSize * 1.3 < Ypos < circleY + circleSize * 1.3)):
                    if i in orderSelected:
                        orderSelected = orderSelected[:orderSelected.index(i)]
                    elif len(game.operations) >= len(orderSelected):
                        orderSelected.append(i)

    # Setting up backplate for displaying goal on
    for i in range(level + 1):
        tempDistance = distance * (9 + level - i) / 9 * 1.04
        points = [(X - tempDistance * sin(pi * i / 3), Y - tempDistance * cos(pi * i / 3)) for i in range(6)]
        pygame.draw.polygon(screen, white, points)

        tempDistance = distance * (9 + level - i) / 9
        points = [(X - tempDistance * sin(pi * i / 3), Y - tempDistance * cos(pi * i / 3)) for i in range(6)]
        pygame.draw.polygon(screen, colours[i], points)

    # Making sure player hasn't won yet
    if not (total == game.goal and len(orderSelected) == len(game.operations) + 1):
        # Writing goal on display plate
        font = pygame.font.Font(None, int(circleSize * 2.5))
        text_surface = font.render(str(game.goal), True, white)
        screen.blit(text_surface, text_surface.get_rect(center=(X, Y)))

        # Drawing lines between selected numbers
        for e, i in enumerate(orderSelected):
            if e + 1 != len(orderSelected):
                pygame.draw.line(screen, colour2, circle['centre'][i], circle['centre'][orderSelected[e+1]], width=int(circleSize / 8))

        # Circling the selected numbers
        for i in range(6):
            diameter = 0.01 * circleSize * circle['radius'][i]
            pygame.draw.circle(screen, colour2, circle['centre'][i], diameter)

    # Drawing the circles for the numbers, and then writing the numbers
    font = pygame.font.Font(None, int(circleSize))
    for i, number in enumerate(game.numbersList):
        colour = colour2 if i in orderSelected else colour1
        pygame.draw.circle(screen, white, circle['centre'][i], circleSize * 1.1)
        pygame.draw.circle(screen, colour, circle['centre'][i], circleSize)

        if not (total == game.goal and len(orderSelected) == len(game.operations) + 1):
            text_surface = font.render(str(number), True, white)
            screen.blit(text_surface, text_surface.get_rect(center=circle['centre'][i]))

    # Adding the numbers together for total
    total = 0
    if len(orderSelected) > 0:
        total = game.numbersList[orderSelected[0]]
        for i in range(len(orderSelected) - 1):
            total = eval(str(total) + game.operations[i] + str(game.numbersList[orderSelected[i + 1]]))

    # Checking for win
    if total == game.goal and len(orderSelected) == len(game.operations) + 1:
        if level < 3:
            level += 1
            game = Game(level)
            colour1 = colours[level]
            colour2 = colours[level + 1]
            orderSelected = []
            step = []
        else:
            print(level)
            colour1 = colours[4]
            level = 4

    else:  # If there's no win, write out top line
        string = ''

        for i, operator in enumerate(game.operations):
            string += str(game.numbersList[orderSelected[i]]) if i < len(orderSelected) else '?'
            string += operator if operator != '*' else '×'
        string += str(game.numbersList[orderSelected[-1]]) if len(game.operations) < len(orderSelected) else '?'

        string += '=' + str(total)

        text_surface = font.render(string, True, black)
        screen.blit(text_surface, text_surface.get_rect(center=(X, Y / 5)))

    pygame.display.flip()
    clock.tick(60)
