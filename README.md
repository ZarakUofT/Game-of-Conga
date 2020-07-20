# Game-of-Conga
This implements the game of Conga in Pygame using the MiniMax Algorithm with Alpha Beta Pruning.

The game can be played by downloading congaHuman_main.exe and running the file.

Rules of Game:
      Initially, Player 1 has ten black stones in (1,4) and Player 2 has ten white stones in (4,1).
      The players alternate turns. On each turn, a player chooses a square with some of his
      stones in it, and picks a direction to move them, either horizontally, vertically or
      diagonally. The move is done by removing the stones from the square and placing one
      stone in the following square, two in the next one, and the others into the last one. The
      stones can only be moved in consecutive squares that are not occupied by the opponent;
      if a direction has less than three squares not occupied by the opponent in a row, then all
      remaining stones are placed in the last empty square. If a square has no neighbouring
      squares that are not occupied by the opponent, then the stones in that square cannot be
      moved.

Next Step: Implement transpositional tables to optimize the search.
