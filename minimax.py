from config import *


def get_adversary(player):
    if player == HUMAN:
        return AI
    else:
        return HUMAN


def isBlocked(GRID, adversary, row, col, direction):
    if (direction == "UP" or direction == "ALL"):
        if row > 0 and GRID[row-1][col][1] != adversary:  # UP
            return False
        elif direction == "UP" or direction != "ALL":
            return True
    if (direction == "UPRIGHT" or direction == "ALL"):
        # UPRIGHT
        if row > 0 and col < len(GRID[0]) - 1 and GRID[row-1][col+1][1] != adversary:
            return False
        elif direction == "UPRIGHT" or direction != "ALL":
            return True
    if (direction == "RIGHT" or direction == "ALL"):
        if col < len(GRID[0]) - 1 and GRID[row][col+1][1] != adversary:  # RIGHT
            return False
        elif direction == "RIGHT" or direction != "ALL":
            return True
    if (direction == "DOWNRIGHT" or direction == "ALL"):
        # DOWNRIGHT
        if row < len(GRID)-1 and col < len(GRID[0]) - 1 and GRID[row+1][col+1][1] != adversary:
            return False
        elif direction == "DOWNRIGHT" or direction != "ALL":
            return True
    if (direction == "DOWN" or direction == "ALL"):
        if row < len(GRID)-1 and GRID[row+1][col][1] != adversary:  # DOWN
            return False
        elif direction == "DOWN" or direction != "ALL":
            return True
    if (direction == "DOWNLEFT" or direction == "ALL"):
        # DOWNLEFT
        if row < len(GRID)-1 and col > 0 and GRID[row+1][col-1][1] != adversary:
            return False
        elif direction == "DOWNLEFT" or direction != "ALL":
            return True
    if (direction == "LEFT" or direction == "ALL"):
        if col > 0 and GRID[row][col-1][1] != adversary:  # LEFT
            return False
        elif direction == "LEFT" or direction != "ALL":
            return True
    if (direction == "UPLEFT" or direction == "ALL"):
        if row > 0 and col > 0 and GRID[row-1][col-1][1] != adversary:  # UPLEFT
            return False
        elif direction == "UPLEFT" or direction != "ALL":
            return True
    return True


def check_win(GRID, curr_player):
    squares_taken = 0
    squares_taken_b = 0
    squares_taken_w = 0
    moves_av_b = 0
    moves_av_w = 0
    blocked = 0
    stones_blocked = 0
    for i in range(len(GRID)):
        for j in range(len(GRID[0])):
            if GRID[i][j][1] == "Black":
                squares_taken_b += 1
                for direction in DIRECTIONS.keys():
                    if free_squares(GRID, i, j, 'Black', direction) > 0:
                        moves_av_b += 1
            elif GRID[i][j][1] == "White":
                squares_taken_w += 1
                for direction in DIRECTIONS.keys():
                    if free_squares(GRID, i, j, 'White', direction) > 0:
                        moves_av_w += 1

    if moves_av_w == 0:
        return 'Black'
    elif moves_av_b == 0:
        return 'White'
    else:
        return str((squares_taken_b + moves_av_b) - (squares_taken_w + moves_av_w))


def free_squares(GRID, i, j, player, direction):
    count = 0
    for _ in range(3):
        if not isBlocked(GRID, get_adversary(player), i, j, direction):
            count += 1
        else:
            break
        i = DIRECTIONS[direction][0](i, 1)
        j = DIRECTIONS[direction][1](j, 1)
    return count


def make_move(GRID, i, j, player, direction, free_sq, curr_stones):
    GRID[i][j] = [0, '']
    k = 1
    stones_distributed = 0
    while(k <= free_sq and curr_stones > stones_distributed):
        i_temp = DIRECTIONS[direction][0](i, k)
        j_temp = DIRECTIONS[direction][1](j, k)
        if k == free_sq:
            GRID[i_temp][j_temp][0] += (curr_stones - stones_distributed)
            GRID[i_temp][j_temp][1] = player
            break
        GRID[i_temp][j_temp][0] += (min(k, curr_stones-stones_distributed))
        GRID[i_temp][j_temp][1] = player
        stones_distributed += k
        k += 1
    return GRID


def MiniMax(GRID, depth, isMaximizing, player, direction, i, j, alpha, beta):
    result = check_win(GRID, player)
    if result == AI or result == HUMAN:
        return SCORE[result], direction, i, j
    elif depth == 0 and result != None:
        return int(result), direction, i, j
    if isMaximizing:
        bestScore = float("-inf")
        bestDirection = direction
        best_i = 0
        best_j = 0
        for i in range(len(GRID)):
            for j in range(len(GRID[0])):
                if GRID[i][j][1] == AI:
                    curr_stones = GRID[i][j][0]
                    for direction in DIRECTIONS.keys():
                        free_sq = free_squares(GRID, i, j, player, direction)
                        if free_sq > 0:
                            grid2 = make_move(copy.deepcopy(
                                GRID), i, j, AI, direction, free_sq, curr_stones)
                            score, direc, l, k = MiniMax(
                                grid2, depth-1, False, HUMAN, direction, i, j, alpha, beta)
                            del grid2
                            del l, k
                            if score > bestScore:
                                best_i = i
                                best_j = j
                                bestScore = score
                                bestDirection = direction
                            alpha = max(alpha, bestScore)
                            if beta <= alpha:
                                return bestScore, bestDirection, best_i, best_j
        return bestScore, bestDirection, best_i, best_j
    else:
        bestScore = float("inf")
        bestDirection = direction
        best_i = 0
        best_j = 0
        for i in range(len(GRID)):
            for j in range(len(GRID[0])):
                if GRID[i][j][1] == HUMAN:
                    curr_stones = GRID[i][j][0]
                    for direction in DIRECTIONS.keys():
                        free_sq = free_squares(GRID, i, j, player, direction)
                        if free_sq > 0:
                            grid2 = make_move(copy.deepcopy(
                                GRID), i, j, HUMAN, direction, free_sq, curr_stones)
                            score, direc, l, k = MiniMax(
                                grid2, depth-1, True, AI, direction, i, j, alpha, beta)
                            del grid2
                            del l, k
                            if score < bestScore:
                                best_i = i
                                best_j = j
                                bestScore = score
                                bestDirection = direction
                            beta = min(beta, bestScore)
                            if beta <= alpha:
                                return bestScore, bestDirection, best_i, best_j
        return bestScore, bestDirection, best_i, best_j
