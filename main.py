import random
import os
import time
from platform import system

all_symbols = ['$', '%', '&', '@', '#', '!', '^', '₴', '?', '+', '=', '/', '~', '<', '(', ')', '*', '№']

def introduction():
    print("              Welcome to PAIRS!")
    print("--------------------RULES---------------------")
    print("| Flip two cards by entering coordinates.    |\n"
          "| If the cards match, they disappear.        |\n"
          "| If not, they flip back over after a while. |\n"
          "| Continue entering coordinates of two cards,|\n"
          "| trying to remember their positions.        |\n"
          "| The game ends when all pairs are matched.  |\n"
          "| Match all pairs with the least moves!      |\n"
          "----------------------------------------------\n"
          "----------------------------------------------")

def gamemode(gm):
    global size
    while gm != "n" and gm != "i":
        gm = input("Please enter n or i: ").lower()
    if gm == "n":
        size = 4
    if gm == "i":
        size = 6

def generate_symbols(n):
    symbols = []
    for i in range(n):
        for j in range(2):
            symbols.append(all_symbols[i])
    random.shuffle(symbols)
    return symbols

def create_board(a):
    pairs = []
    if size == 4:
        pairs = generate_symbols(size * 2)
    if size == 6:
        pairs = generate_symbols(size * 3)
    matrix = [[0] * a for i in range(a)]
    for i in range(a):
        for j in range(a):
            matrix[i][j] = pairs.pop()
    return matrix

def display_board(displayed_matrix):
    os.system('cls')  # Clear the console
    if size == 4:
        column_headers = '  ' + ' '.join('abcd'[:len(displayed_matrix)])
        print(column_headers)
    if size == 6:
        column_headers = '  ' + ' '.join('abcdef'[:len(displayed_matrix)])
        print(column_headers)

    row_index = 1
    for row in displayed_matrix:
        print(f'{row_index} ' + ' '.join(str(x) if x != 0 else '0' for x in row))
        row_index += 1

def check_pair(x1, y1, x2, y2, board):
    return board[x1][y1] == board[x2][y2]

def convert_coord(coord):
    if size == 4:
        coordinates = {'a': 0, 'b': 1, 'c': 2, 'd': 3}
    if size == 6:
        coordinates = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5}
    if len(coord) != 2 or not coord[0].isdigit() or coord[1] not in coordinates:
        print("Invalid input. Please use the format '1a', '2b', etc.")
        time.sleep(2)
        return None, None
    row = int(coord[0]) - 1
    col = coordinates[coord[1]]
    return row, col

def enter_coord(displayed_matrix, board):
    # Get the first card
    coord1 = input("Enter the first card (e.g., 1a): ")
    x1, y1 = convert_coord(coord1)
    if displayed_matrix[x1][y1] == board[x1][y1]:
        print("Card already opened")
        time.sleep(1.5)
        return None, None, None, None
    if x1 == None or y1 == None:
        print("Invalid input. Please use the format '1a', '2b', etc.")
        time.sleep(1.5)
        return None, None, None, None

    displayed_matrix[x1][y1] = board[x1][y1]
    display_board(displayed_matrix)  # Display board after revealing first card

    # Get the second card
    coord2 = input("Enter the second card (e.g., 2b): ")
    x2, y2 = convert_coord(coord2)
    if x2 is None or y2 is None or (x1 == x2 and y1 == y2):
        print("Invalid second card or same card selected.")
        displayed_matrix[x1][y1] = 0  # Reset the first card if invalid
        return None, None, None, None

    displayed_matrix[x2][y2] = board[x2][y2]
    display_board(displayed_matrix)  # Display board after revealing second card

    return x1, x2, y1, y2

def play_game():
    introduction()
    gamemode(input("Please choose gamemode (NORMAL or IMPOSSIBLE): ").lower())
    time.sleep(2)

    turns = 0
    board = create_board(size)
    displayed_matrix = [[0] * size for i in range(size)]

    while any(0 in row for row in displayed_matrix):
        display_board(displayed_matrix)

        x1, x2, y1, y2 = enter_coord(displayed_matrix, board)
        if x1 is None:
            continue

        time.sleep(1)  # Show both cards for 3 seconds

        if check_pair(x1, y1, x2, y2, board):
            print("It's a match!")
            time.sleep(2)
        else:
            print("Try again")
            time.sleep(2)
            displayed_matrix[x1][y1] = 0
            displayed_matrix[x2][y2] = 0  # Flip back if not a match
        turns += 1

    print("Congratulations! You've found all the pairs!")

play_game()