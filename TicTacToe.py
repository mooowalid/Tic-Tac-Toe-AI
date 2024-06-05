import sys
import pygame
import numpy as np

pygame.init()

# Colors
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Gray = (180, 180, 180)

Width = 300
Height = 300
Line_Width = 5
Board_Rows = 3
Board_Cols = 3
Square_Size = Width // Board_Cols
Circle_Radius = Square_Size // 3
Circle_Width = 15
Cross_Width = 25

screen = pygame.display.set_mode((Width, Height))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(Black)

Board = np.zeros((Board_Rows, Board_Cols))


def draw_lines(color=White):
    for i in range(1, Board_Rows):
        pygame.draw.line(screen, color, (0, Square_Size * i), (Width, Square_Size * i), Line_Width)
        pygame.draw.line(screen, color, (Square_Size * i, 0), (Square_Size * i, Height), Line_Width)


def draw_figures(color=White):
    for row in range(Board_Rows):
        for col in range(Board_Cols):
            if Board[row][col] == 1:
                pygame.draw.circle(screen, color, (col * Square_Size + Square_Size // 2,
                                                    row * Square_Size + Square_Size // 2),
                                   Circle_Radius, Circle_Width)
            elif Board[row][col] == 2:
                pygame.draw.line(screen, color, (col * Square_Size + Square_Size // 4, row * Square_Size + Square_Size // 4),
                                 (col * Square_Size + 3 * Square_Size // 4, row * Square_Size + 3 * Square_Size // 4),
                                 Cross_Width)
                pygame.draw.line(screen, color, (col * Square_Size + Square_Size // 4, row * Square_Size + 3 * Square_Size // 4),
                                 (col * Square_Size + 3 * Square_Size // 4, row * Square_Size + Square_Size // 4),
                                 Cross_Width)


def mark_square(row, col, player):
    Board[row][col] = player


def available_square(row, col):
    return Board[row][col] == 0


def is_board_full(check_board=Board):
    return not (check_board == 0).any()


def check_win(player,Check_board=Board):
    for col in range(Board_Cols):
         if Check_board[0][col] == player and Check_board[1][col] == player and Check_board[2][col] == player :
             return True
    
    for row in range(Board_Rows):
         if Check_board[row][0]==player and Check_board[row][1]==player and Check_board[row][2]==player :
             return True
    
    if Check_board[0][0]==player and Check_board[1][1]==player and Check_board[2][2]==player :
             return True   
    
    if Check_board[0][2]==player and Check_board[1][1]==player and Check_board[2][0]==player :
             return True   
    return False

def minimax(minimax_board, depth, is_maximizing):
    if check_win(2, minimax_board):
        return float('inf')

    if check_win(1, minimax_board):
        return float('-inf')

    if is_board_full(minimax_board):
        return 0

    if is_maximizing:
        best_score = -1000
        for row in range(Board_Rows):
            for col in range(Board_Cols):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 2
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][col] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for row in range(Board_Rows):
            for col in range(Board_Cols):
                if minimax_board[row][col] == 0:
                    minimax_board[row][col] = 1
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][col] = 0
                    best_score = min(score, best_score)
        return best_score


def best_move():
    best_score = -1000
    move = (-1, -1)
    for row in range(Board_Rows):
        for col in range(Board_Cols):
            if Board[row][col] == 0:
                Board[row][col] = 2
                score = minimax(Board, 0, False)
                Board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)
    if move != (-1, -1):
        mark_square(move[0], move[1], 2)
        return True
    return False


def restart_game():
    screen.fill(Black)
    draw_lines()
    for row in range(Board_Rows):
        for col in range(Board_Cols):
            Board[row][col] = 0


draw_lines()
player = 1
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // Square_Size
            mouseY = event.pos[1] // Square_Size

            if available_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)
                if check_win(player):
                    game_over = True
                player = 2 

                if not game_over:
                    if is_board_full():
                        game_over = True
                    else:
                        if best_move():  
                            if check_win(2):
                                game_over = True
                            player = 1  

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1

    if not game_over:
        draw_figures()
    else:
        if check_win(1):
            draw_figures(Green)
            draw_lines(Green)
        elif check_win(2):
            draw_figures(Red)
            draw_lines(Red)
        else:
            draw_figures(Gray)
            draw_lines(Gray)

    pygame.display.update()