# Project name
KR-X-and-0-Game

# Description
Implemented a X and 0 inspired game that has the next features:
- it is turn based
- the player is X and the computer is 0
- you can set the time and the level of difficulty 
- the board is a 10x10 grid; for the initial board check initial_board.jpg from project
- you can place only two symbols at once that can be next to each other(orizantal move) or one above the other (vertical move)
- the move must have among its "neighbours" at least one X and one 0; exemple of some valid moves at valid_moves.jpg
- you earn one point when you form a diagonal from three of your symbols, visible in the file diagonal.jpg
- the game ends when the time is up, or when there aren't any valid moves on the board

# Features
The game has a console interface, as well as a graphic one, implemented using pygame.

At the end of the game, you get the statistics of your game, such as: the minimum, maximum, mean and median of the computer's "thinking" times, the number of moves for each player, the time of playing. The winner (or draw) is also announced.

