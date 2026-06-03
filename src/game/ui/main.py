# ==========================================
# Team Number: 3
# Variant Name: main.py
# Student Names: Ivan Lopez, Maria Ortiz, Jenny Leon
# ==========================================

#library imports
import pygame, sys

#display module
window_height = 400
window_width = 400
grass = (107, 179, 108)
street = (224, 224, 224)

#grid
def drawGrid():
    blockSize = 50
    for x in range(0, window_width, blockSize):
        for y in range(0, window_height, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, street, rect, 1)

#game loop
def gameLoop():
    global screen, clock
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("City Builder")
    clock = pygame.time.Clock()
    screen.fill(grass)

    while True:
        drawGrid()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(30)

gameLoop()