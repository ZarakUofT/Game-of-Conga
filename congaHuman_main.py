from config import *
from minimax import *
from user_interface import *
pygame.font.init()
pygame.init()


def get_direction(move):
    i1 = move[0]
    j1 = move[1]
    i2 = move[2]
    j2 = move[3]
    for item in DIRECTIONS.items():
        if item[1][0](i1, 1) == i2 and item[1][1](j1, 1) == j2:
            return item[0]


def human_move(GRID, board):
    coords = get_click_coords(GRID, board)
    direction = get_direction(coords)
    GRID = make_move(GRID, coords[0], coords[1], HUMAN, direction, free_squares(
        GRID, coords[0], coords[1], HUMAN, direction), GRID[coords[0]][coords[1]][0])
    return GRID


def AI_move(GRID):
    depth = 1
    score = 0
    bestScore = 0
    best_i = 0
    best_j = 0
    bestDirection = random.choice(list(DIRECTIONS.keys()))
    maxDepth = 4
    while(depth <= maxDepth):
        score, direction, i, j = MiniMax(copy.deepcopy(
            GRID), depth, True, AI, "", 0, 0, float('-inf'), float('inf'))
        if score > bestScore:
            bestScore = score
            best_i = i
            best_j = j
            bestDirection = direction
        if bestScore == 1000:
            break
        depth += 1

    GRID = make_move(GRID, best_i, best_j, AI, bestDirection, free_squares(
        GRID, best_i, best_j, AI, bestDirection), GRID[best_i][best_j][0])
    return GRID


def handle_click(board, GRID):
    if CURRENT_PLAYER == HUMAN:
        GRID = human_move(GRID, board)
    else:
        GRID = AI_move(GRID)
    draw_move(board, CURRENT_PLAYER, GRID)
    return GRID


def main():
    global CURRENT_PLAYER
    TOTAL_MOVES = 0
    run = True
    board = init_window(WIN)
    GRID = [[[0, ''] for i in range(4)] for j in range(4)]
    GRID[0][0] = [10, 'Black']
    GRID[3][3] = [10, 'White']
    draw_move(board, CURRENT_PLAYER, GRID)
    display_board(WIN, board, f"{CURRENT_PLAYER}'s turn",
                  PLAYER_COLOR[CURRENT_PLAYER])

    while(run):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                quit()
        result = check_win(GRID, CURRENT_PLAYER)
        if CURRENT_PLAYER == HUMAN and (result != AI and result != HUMAN):
            GRID = handle_click(board, GRID)
            CURRENT_PLAYER = AI
        elif CURRENT_PLAYER == AI and (result != AI and result != HUMAN):
            GRID = handle_click(board, GRID)
            TOTAL_MOVES += 1
            CURRENT_PLAYER = HUMAN
        elif result == AI or result == HUMAN:
            display_board(
                WIN, board, f"{check_win(GRID, CURRENT_PLAYER)} has won! Total Moves: {TOTAL_MOVES}", (100, 150, 250))
            run = False
            time.sleep(3)
            return
        display_board(
            WIN, board, f"{CURRENT_PLAYER}'s turn", PLAYER_COLOR[CURRENT_PLAYER])


def main_menu():
    run = True
    text_size = int(WIDTH/16)
    color = (255, 255, 255)
    while run:
        WIN.fill((0, 0, 0))
        menu_display_text("Press Enter to begin the game..",
                          100, color, text_size)
        menu_display_text("Or", 50, color, text_size)
        menu_display_text("Press Esc to Exit", 0, color, text_size)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                main()
    pygame.quit()


main_menu()
