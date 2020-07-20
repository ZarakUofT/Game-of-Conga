from config import *


def find_coords(position):
    return int((position-1)/4), int(((position-1) % 4))


def find_position(row, col):
    return ((4*row) + col + 1)


def find_pos(mouseX, mouseY):
    if HEIGHT*LINE_AD_Y < mouseY < HEIGHT*LINE_AD_X:
        if WIDTH*LINE_AD_Y < mouseX < WIDTH * LINE_AD_X:
            position = 1
        elif WIDTH * LINE_AD_X < mouseX < int(WIDTH/2):
            position = 2
        elif int(WIDTH/2) < mouseX < WIDTH * (1 - LINE_AD_X):
            position = 3
        elif WIDTH*(1 - LINE_AD_X) < mouseX < WIDTH*(1 - LINE_AD_Y):
            position = 4
        else:
            position = 17
    elif HEIGHT*LINE_AD_X < mouseY < int(HEIGHT/2):
        if WIDTH*LINE_AD_Y < mouseX < WIDTH * LINE_AD_X:
            position = 5
        elif WIDTH * LINE_AD_X < mouseX < int(WIDTH/2):
            position = 6
        elif int(WIDTH/2) < mouseX < WIDTH * (1 - LINE_AD_X):
            position = 7
        elif WIDTH*(1 - LINE_AD_X) < mouseX < WIDTH*(1 - LINE_AD_Y):
            position = 8
        else:
            position = 17
    elif int(HEIGHT/2) < mouseY < HEIGHT*(1 - LINE_AD_X):
        if WIDTH*LINE_AD_Y < mouseX < WIDTH * LINE_AD_X:
            position = 9
        elif WIDTH * LINE_AD_X < mouseX < int(WIDTH/2):
            position = 10
        elif int(WIDTH/2) < mouseX < WIDTH * (1 - LINE_AD_X):
            position = 11
        elif WIDTH*(1 - LINE_AD_X) < mouseX < WIDTH*(1 - LINE_AD_Y):
            position = 12
        else:
            position = 17
    elif HEIGHT*(1 - LINE_AD_X) < mouseY < HEIGHT*(1 - LINE_AD_Y):
        if WIDTH*LINE_AD_Y < mouseX < WIDTH * LINE_AD_X:
            position = 13
        elif WIDTH * LINE_AD_X < mouseX < int(WIDTH/2):
            position = 14
        elif int(WIDTH/2) < mouseX < WIDTH * (1 - LINE_AD_X):
            position = 15
        elif WIDTH*(1 - LINE_AD_X) < mouseX < WIDTH*(1 - LINE_AD_Y):
            position = 16
        else:
            position = 17
    else:
        position = 17
    return position


def init_window(window):
    board = pygame.Surface(window.get_size())
    board = board.convert()
    board.fill((150, 150, 100))

    pygame.draw.line(board, (0, 0, 0), (WIDTH*LINE_AD_X, HEIGHT *
                                        LINE_AD_Y), (WIDTH*LINE_AD_X, HEIGHT*(1-LINE_AD_Y)), 2)
    pygame.draw.line(board, (0, 0, 0), (WIDTH*(1-LINE_AD_X), HEIGHT *
                                        LINE_AD_Y), (WIDTH*(1-LINE_AD_X), HEIGHT*(1-LINE_AD_Y)), 2)
    pygame.draw.line(board, (0, 0, 0), (int(WIDTH/2), HEIGHT *
                                        LINE_AD_Y), (int(WIDTH/2), HEIGHT*(1-LINE_AD_Y)), 2)

    pygame.draw.line(board, (0, 0, 0), (WIDTH*LINE_AD_Y, HEIGHT *
                                        LINE_AD_Y), (WIDTH*LINE_AD_Y, HEIGHT*(1-LINE_AD_Y)), 2)
    pygame.draw.line(board, (0, 0, 0), (WIDTH*(1-LINE_AD_Y), HEIGHT *
                                        LINE_AD_Y), (WIDTH*(1-LINE_AD_Y), HEIGHT*(1-LINE_AD_Y)), 2)

    pygame.draw.line(board, (0, 0, 0), (HEIGHT*LINE_AD_Y, WIDTH *
                                        LINE_AD_X), (HEIGHT*(1-LINE_AD_Y), WIDTH*LINE_AD_X), 2)
    pygame.draw.line(board, (0, 0, 0), (HEIGHT*LINE_AD_Y, WIDTH *
                                        (1-LINE_AD_X)), (HEIGHT*(1-LINE_AD_Y), WIDTH*(1-LINE_AD_X)), 2)

    pygame.draw.line(board, (0, 0, 0), (HEIGHT*LINE_AD_Y,
                                        int(WIDTH/2)), (HEIGHT*(1-LINE_AD_Y), int(WIDTH/2)), 2)

    pygame.draw.line(board, (0, 0, 0), (HEIGHT*LINE_AD_Y, WIDTH *
                                        LINE_AD_Y), (HEIGHT*(1-LINE_AD_Y), WIDTH*LINE_AD_Y), 2)
    pygame.draw.line(board, (0, 0, 0), (HEIGHT*LINE_AD_Y, WIDTH *
                                        (1-LINE_AD_Y)), (HEIGHT*(1-LINE_AD_Y), WIDTH*(1-LINE_AD_Y)), 2)

    return board


def game_status(status, board, color):
    text_col = PLAYER_COLOR['White']
    if color == PLAYER_COLOR['White']:
        text_col = PLAYER_COLOR['Black']
    pos_y = HEIGHT*(1-LINE_AD_Y) + 20
    font = pygame.font.SysFont("calibri", int(WIDTH/18))
    board.fill(color, (0, pos_y + 20, WIDTH, HEIGHT * LINE_AD_Y))
    text1 = font.render(status, 1, text_col)
    text2 = font.render(f"Your Symbol: {HUMAN}", 1, text_col)
    text3 = font.render(f"AI Symbol: {AI}", 1, text_col)
    board.blit(text1, (int(WIDTH/15), pos_y + 30))
    board.blit(text2, (int(WIDTH/15), HEIGHT/30))
    board.blit(text3, (int(WIDTH/15), HEIGHT/30 + HEIGHT/20))
    if WRONG_CLICK:
        error = font.render("Please click in correct spot!", 1, (255, 0, 0))
        board.blit(error, (int(WIDTH/15), int(HEIGHT/15)))


def display_board(window, board, status, color):
    game_status(status, board, color)
    window.blit(board, (0, 0))
    pygame.display.flip()


def menu_display_text(text, y_offset, color, text_size):
    title_font = pygame.font.SysFont("calibri", text_size)
    title_label = title_font.render(text, 1, color)
    WIN.blit(title_label, (WIDTH/2-title_label.get_width()/2,
                           (HEIGHT/2-title_label.get_height()/2) - y_offset))


def isAdjacent(i_sel, j_sel, i, j):
    if i_sel == i and j_sel == j:
        return False
    for direction in DIRECTIONS.keys():
        if DIRECTIONS[direction][0](i_sel, 1) == i and DIRECTIONS[direction][1](j_sel, 1) == j:
            return True
    return False


def draw_move(board, player, GRID):
    for i in range(len(GRID)):
        for j in range(len(GRID[0])):
            if GRID[i][j][1] == '':
                board.fill((150, 150, 100),
                           COLOR_BOX_COORD[find_position(i, j)])
            elif GRID[i][j][1] == HUMAN:
                board.fill((250, 250, 250),
                           COLOR_BOX_COORD[find_position(i, j)])
            elif GRID[i][j][1] == AI:
                board.fill((0, 0, 0), COLOR_BOX_COORD[find_position(i, j)])
            display_score(board, GRID[i][j][0], i, j)


def display_score(board, val, row, col):
    font = pygame.font.SysFont("calibri", int(WIDTH/20))
    text = font.render(f"{val}", 1, (255, 0, 0))
    board.blit(text, ENTRY_POS[find_position(row, col)])


def get_click_coords(GRID, board):
    count = 0
    move = []
    run = True
    while (run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = find_pos(pygame.mouse.get_pos()[
                                    0], pygame.mouse.get_pos()[1])
                if position == 17:
                    display_board(
                        WIN, board, "Please click inside one of the given squares", (255, 100, 0))
                    continue
                i, j = find_coords(position)
                if count == 0 and GRID[i][j][1] == HUMAN:
                    board.fill((255, 182, 193), COLOR_BOX_COORD[position])
                    display_score(board, GRID[i][j][0], i, j)
                    display_board(WIN, board, "Pink box Selected",
                                  PLAYER_COLOR[CURRENT_PLAYER])
                    i_sel = i
                    j_sel = j
                    count += 1
                elif count == 1 and (i_sel == i) and (j_sel == j):
                    board.fill(PLAYER_COLOR[CURRENT_PLAYER],
                               COLOR_BOX_COORD[position])
                    display_score(board, GRID[i][j][0], i, j)
                    display_board(WIN, board, "De-Selected! Try Again",
                                  PLAYER_COLOR[CURRENT_PLAYER])
                    count = 0
                elif count == 1 and GRID[i][j][1] != AI and isAdjacent(i_sel, j_sel, i, j):
                    i_move = i
                    j_move = j
                    count += 1
                elif count == 1 and not isAdjacent(i_sel, j_sel, i, j):
                    display_board(
                        WIN, board, "Select a square adjacent to the pink box", (255, 0, 0))
                if count > 1:
                    run = False
                    break
    return [i_sel, j_sel, i_move, j_move]
