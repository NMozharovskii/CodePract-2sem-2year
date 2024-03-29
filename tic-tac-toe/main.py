import pygame
import sys



def check_win(mas, sign):
    zeroes = 0
    for row in mas:
        zeroes += row.count(0)
        if row.count(sign) == 3:
            return sign
    for col in range(3):
        if mas[0][col] == sign and mas[1][col] == sign and mas[2][col] == sign:
            return sign
    if mas[0][0] == sign and mas[1][1] == sign and mas[2][2] == sign:
        return sign
    if mas[0][2] == sign and mas[1][1] == sign and mas[2][0] == sign:
        return sign
    if zeroes == 0:
        return 'Piece'
    return False


pygame.init()
size_block = 100
margin = 15
width = height = size_block * 3 + margin * 4

size_window = (width, height)
screen = pygame.display.set_mode(size_window)
pygame.display.set_caption("Крестики - Нолики")

black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)
mas = [[0] * 3 for i in range(3)]
query = 0
signX = 1
signO = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            col = x_mouse // (size_block + margin)
            row = y_mouse // (size_block + margin)
            if mas[row][col] == 0:
                if query%2 == 0:
                    mas[row][col] = 'X'
                else:
                    mas[row][col] = 'O'
                query += 1

    for row in range(3):
        for col in range(3):
            if mas[row][col] == 'X':
                color = signX
            elif mas[row][col] == 'O':
                color = signO
            else:
                color = white
            x = col * size_block + (col + 1) * margin
            y = row * size_block + (row + 1) * margin
            pygame.draw.rect(screen, white, (x, y, size_block, size_block))
            if color == signX:
                pygame.draw.line(screen, black, (x + 5, y + 5), (x + size_block - 5, y + size_block - 5), 3)
                pygame.draw.line(screen, black, (x + size_block - 5, y + 5), (x + 5, y + size_block - 5 ), 3)
            elif color == signO:
                pygame.draw.circle(screen, black, (x + size_block//2, y + size_block//2), size_block//2 - 3, 3)

    if (query - 1)%2 == 0:
        game_over = check_win(mas, 'X')
    else:
        game_over = check_win(mas, 'O')

    if game_over:
        screen.fill(black)
        font = pygame.font.SysFont('stxinqkai', 80)
        text1 = font.render(game_over, True, white)
        text_rect = text1.get_rect()
        text_x = screen.get_width()/2 - text_rect.width/2
        text_y = screen.get_height()/2 - text_rect.height/2
        screen.blit(text1, (text_x, text_y))


    pygame.display.update()
