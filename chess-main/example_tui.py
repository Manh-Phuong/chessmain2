# Chess Program
#
# Basic requirements:
# > pip install python-chess
# > pip install pygame
#

import chess
from ChessHelpers import ChessEngineHelper

CHECKMATE = 1000
STALEMATE = 0

GUI = False  # choose between graphical or terminal interface
if GUI:
    from interface.gui import play_chess
else:
    from interface.tui import play_chess


def main():
    # Let's make the move generator play ten games against itself

    # create an array to hold the game outcomes
    outcomes = []

    for _ in range(10):
        # create a chess board object
        board = chess.Board()

        # run the game loop to display the board UI
        # parameters:
        #   a chess board
        #   a move generation function for white (optional, defaults to player)
        #   a move generation function for black (optional, defaults to player)
        #
        # return value:
        #   the outcome of the game
        #
        # If you run this file as-is, our random move generator (white)
        #   will play ten games against our greedy next best move algorithm (black)
        move_generator = ChessEngineHelper.MoveGenerator()
        outcome = play_chess(board, white=move_generator.random_move,
                             black=move_generator.greedy_best_next_move)
        outcomes.append(outcome)

    # display all the game results
    print("\n\nResults:")
    for o in outcomes:
        print(o)


if __name__ == '__main__':
    main()
