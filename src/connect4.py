"""
-------------------------------------------------------
connect4.py
A game of Connect 4.
-------------------------------------------------------
Author:  Nathaniel Carr
ID: 160150170
Email:  carr0170@mylaurier.ca
__updated__ = "2018-01-11"
-------------------------------------------------------
"""

CONV_KEY = "ABCDEFG"


def main():
    """
    -------------------------------------------------------
    Main function.
    -------------------------------------------------------
    """

    while True:  # emulating do-while.

        over = False
        # col is first dim, row is second dim
        board = [[' ' for _ in range(0, 6)] for _ in range(0, 7)]

        # draw board.
        draw_board(board)
        print()

        while not over:

            # player 1's turn.
            c, r = play_turn(board, '1', 'O')
            print()

            # draw board.
            draw_board(board)
            print()

            # check if game won. Even number of tiles, so a tie cannot occur after
            # player 1's turn.
            over = check_win(board, c, r)
            if over:
                print("Player 1 wins!")
            else:

                # player 2's turn.
                c, r = play_turn(board, '2', 'X')
                print()

                # draw board.
                draw_board(board)
                print()

                # check if game won/tied.
                over = check_win(board, c, r)
                if over:
                    print("Player 2 wins!")
                else:
                    over = check_tie(board)
                    if over:
                        print("It's a tie!")

        # do-while emulation's condition.
        print()
        if not input("Would you like to play again (Y/N)? ") in "Yy":
            break
        else:
            print()


def draw_board(board):
    """
    -------------------------------------------------------
    Draws a board from a 2d array of char with 7 indices in 
        the first dimension and 6 in the second.
    Use: draw_board(board)
    -------------------------------------------------------
    Preconditions:
        board - a 2d array of char with 7 indices in the first 
            dimension and 6 in the second.
    Postconditions:
        prints - the board.
    -------------------------------------------------------
    """

    # print first (header) row.
    print("A B C D E F G")

    # print rows 0 - 4.
    for r in range(0, 5):

        # print columns 0 - 5.
        for c in range(0, 6):
            print("{}|".format(board[c][r]), end='')

        # print final column.
        print("{}".format(board[6][r]))

        # divider.
        print("-" * 13)

    # print final row.
    for c in range(0, 6):
        print("{}|".format(board[c][5]), end='')

    # print final column.
    print("{}".format(board[6][5]))


def play_turn(board, player_num, player_char):
    """
    -------------------------------------------------------
    Allows a player to enter the column for their char to be entered into.
        Adds the char to the "board" in the desired location.
    Use: c, r = play_turn(board, player_num, player_char)
    -------------------------------------------------------
    Preconditions:
        board - a 2d array of char with 7 indices in the first 
            dimension and 6 in the second.
        player_num - char containing the label by which
            the current player is referred.
        player_char - char containing the symbol representing 
            the current player's ownership of a space.
    Postconditions:
        returns
        c - the column selected by the current player.
        r - the row the player's char was deposited into.
    -------------------------------------------------------
    """

    print("Player {}'s turn. Enter column A-G: ".format(player_num), end='')
    c = list(input(""))[0].upper()  # gets only first char input.
    while not ('A' <= c <= 'G'):
        print("Not a valid column. Enter a column A-G: ", end='')
        c = list(input(""))[0].upper()  # gets only first char input.

    # convert to col number.
    c = CONV_KEY.find(c)

    # determine whether or not col can be used and, if so, which row (r)
    # should be used.
    r = 5
    while r >= 0 and board[c][r] != ' ':
        r -= 1

    while r < 0:
        print("This column is full. Enter another column A-G: ", end='')
        c = list(input(""))[0].upper()  # gets only first char input.
        while not ('A' <= c <= 'G'):
            print("Not a valid column. Enter a column A-G: ", end='')
            c = list(input(""))[0].upper()  # gets only first char input.

        # convert to col number.
        c = CONV_KEY.find(c)

        # determine whether or not col can be used and, if so, which row (r)
        # should be used.
        r = 5
        while r >= 0 and board[c][r] != ' ':
            r -= 1

    # insert char.
    board[c][r] = player_char

    return c, r


def check_tie(board):
    """
    -------------------------------------------------------
    Checks if the board is full (tie).
    Use: tied = check_tie(board)
    -------------------------------------------------------
    Preconditions:
        board - a 2d array of char with 7 indices in the first 
            dimension and 6 in the second.
    Postconditions:
        returns
        True if the board is full, False otherwise.
    -------------------------------------------------------
    """

    tied = True
    for c in range(0, 7):
        for r in range(0, 6):
            if board[c][r] == ' ':
                tied = False
                break

        if not tied:
            break

    return tied


def check_win(board, c, r):
    """
    -------------------------------------------------------
    Checks if the game has been won by inserting a char into
        the space defined by c and r.
    Use: won = check_win(board, c, r)
    -------------------------------------------------------
    Preconditions:
        board - a 2d array of char with 7 indices in the first 
            dimension and 6 in the second.
        c - the newly-selected column.
        r - the newly-selected row.
    Postconditions:
        returns
        True if the game has been won by this move, False 
            otherwise.
    -------------------------------------------------------
    """

    won = check_win_horiz(board, c, r)

    if not won:
        won = check_win_vert(board, c, r)

    if not won:
        won = check_win_diag_left(board, c, r)

    if not won:
        won = check_win_diag_right(board, c, r)

    return won


def check_win_horiz(board, c, r):
    """
    -------------------------------------------------------
    Checks if the game has been won horizontally by 
        inserting a char into the space defined by c and r.
    Use: won = check_win(board, c, r)
    -------------------------------------------------------
    Preconditions:
        board - a 2d array of char with 7 indices in the first 
            dimension and 6 in the second.
        c - the newly-selected column.
        r - the newly-selected row.
    Postconditions:
        returns
        True if the game has been won by this move, False 
            otherwise.
    -------------------------------------------------------
    """

    count = 1  # as a minimum, you have at least one in a row.

    # moving to the left until a non-matching char found.
    i = 1
    while c - i >= 0 and board[c][r] == board[c - i][r]:
        count += 1
        i += 1

    # moving to the right until a non-matching char found and while count not
    # at 4.
    i = 1
    while count < 4 and c + i <= 6 and board[c][r] == board[c + i][r]:
        count += 1
        i += 1

    # return true if won.
    return count >= 4


def check_win_vert(board, c, r):
    """
    -------------------------------------------------------
    Checks if the game has been won vertically by 
        inserting a char into the space defined by c and r.
    Use: won = check_win(board, c, r)
    -------------------------------------------------------
    Preconditions:
        board - a 2d array of char with 7 indices in the first 
            dimension and 6 in the second.
        c - the newly-selected column.
        r - the newly-selected row.
    Postconditions:
        returns
        True if the game has been won by this move, False 
            otherwise.
    -------------------------------------------------------
    """

    count = 1  # as a minimum, you have at least one in a row.

    # moving up until a non-matching char found.
    i = 1
    while r - i >= 0 and board[c][r] == board[c][r - i]:
        count += 1
        i += 1

    # moving to the left until a non-matching char found and while count not
    # at 4.
    i = 1
    while count < 4 and r + i <= 5 and board[c][r] == board[c][r + i]:
        count += 1
        i += 1

    # return true if won.
    return count >= 4


def check_win_diag_right(board, c, r):
    """
    -------------------------------------------------------
    Checks if the game has been won on the right diagonal (\)
        by inserting a char into the space defined by c and r.
    Use: won = check_win(board, c, r)
    -------------------------------------------------------
    Preconditions:
        board - a 2d array of char with 7 indices in the first 
            dimension and 6 in the second.
        c - the newly-selected column.
        r - the newly-selected row.
    Postconditions:
        returns
        True if the game has been won by this move, False 
            otherwise.
    -------------------------------------------------------
    """

    count = 1  # as a minimum, you have at least one in a row.

    # moving up and left until a non-matching char found.
    i = 1
    while r - i >= 0 and c - i >= 0 and board[c][r] == board[c - i][r - i]:
        count += 1
        i += 1

    # moving down and right until a non-matching char found.
    i = 1
    while r + i <= 5 and c + i <= 6 and board[c][r] == board[c + i][r + i]:
        count += 1
        i += 1

    # return true if won.
    return count >= 4


def check_win_diag_left(board, c, r):
    """
    -------------------------------------------------------
    Checks if the game has been won on the left diagonal (/)
        by inserting a char into the space defined by c and r.
    Use: won = check_win(board, c, r)
    -------------------------------------------------------
    Preconditions:
        board - a 2d array of char with 7 indices in the first 
            dimension and 6 in the second.
        c - the newly-selected column.
        r - the newly-selected row.
    Postconditions:
        returns
        True if the game has been won by this move, False 
            otherwise.
    -------------------------------------------------------
    """

    count = 1  # as a minimum, you have at least one in a row.

    # moving up and right until a non-matching char found.
    i = 1
    while r - i >= 0 and c + i <= 6 and board[c][r] == board[c + i][r - i]:
        count += 1
        i += 1

    # moving down and left until a non-matching char found.
    i = 1
    while r + i <= 5 and c - i >= 0 and board[c][r] == board[c - i][r + i]:
        count += 1
        i += 1

    # return true if won.
    return count >= 4


# call main
main()
