# minesweeper.py

This is the classic minesweeper game, but it includes an automatic solver



$> ./minesweeper.py 
  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
--+-----------------------------------+
0 | - | - | - | - | - | - | - | - | - |
1 | - | - | - | - | - | - | - | - | - |
2 | - | - | - | - | - | - | - | - | - |
3 | - | - | - | - | - | - | - | - | - |
4 | - | - | - | - | - | - | - | - | - |
5 | - | - | - | - | - | - | - | - | - |
6 | - | - | - | - | - | - | - | - | - |
7 | - | - | - | - | - | - | - | - | - |
8 | - | - | - | - | - | - | - | - | - |
--+-----------------------------------+
bombs left: 9
You can say:
 'uncover {row} {col}' to uncover that square
 'mark {row} {col}' to mark a bomb in that square
 'hint' to get a hint
 'init' to start a new game

Enter your command: uncover 4 5
  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
--+-----------------------------------+
0 | - | - | - | - | - | - | - | - | - |
1 | - | - | - | - | - | - | - | - | - |
2 | - | - | - | - | - | - | - | - | - |
3 | - | - | - | - | - | - | - | - | - |
4 | - | - | - | - | - | 1 | - | - | - |
5 | - | - | - | - | - | - | - | - | - |
6 | - | - | - | - | - | - | - | - | - |
7 | - | - | - | - | - | - | - | - | - |
8 | - | - | - | - | - | - | - | - | - |
--+-----------------------------------+
bombs left: 9

Enter your command: hint
Solver says uncover 0 1

Enter your command: uncover 0 1
