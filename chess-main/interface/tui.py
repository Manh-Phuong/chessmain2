# # Chess TUI
# #
# # This file contains a terminal user interface for displaying python-chess boards.
# # Entering moves like this is very tedious, I definitely recommend using the GUI!
# #
# # Note: By default, my terminal in Pycharm did not display the board correctly with Jetbrains default font.
# #   Courier New, Consolas, Lucida Sans Typewriter, everything else works fine.
# #   (File -> Settings -> Editor -> Colors Scheme -> Console Font)
# #

# import chess

# ENABLE_ILLEGAL_MOVES = False


# # game loop
# def play_chess(board, white="player", black="player"):
#     while True:
#         # find out if the game is over
#         outcome = board.outcome()
#         if outcome is None:

#             if board.turn == chess.WHITE and white == "player" \
#                     or board.turn == chess.BLACK and black == "player":

#                 # print chess board to the terminal when it is a players turn
#                 print()
#                 print(board.unicode(invert_color=True))

#                 # prompt the player for a move
#                 legal_moves = list(board.legal_moves)
#                 print("\nAvailable moves:")
#                 for m in legal_moves:
#                     print(m.uci(), end=", ")
#                 if board.turn == chess.WHITE:
#                     uci = input("\n\nWhite's move: ")
#                 else:
#                     uci = input("\n\nBlack's move: ")
#                 move = chess.Move.from_uci(uci)

#                 # attempt to make the move
#                 if move in board.legal_moves or ENABLE_ILLEGAL_MOVES:
#                     board.push(move)

#             else:
#                 # generate and push a move to the board
#                 # generate and push a move to the real chess board
#                 if board.turn == chess.WHITE:
#                     move = white(board)
#                     board.push(move)
#                     print("White's move:", move.uci())
#                 else:
#                     move = black(board)
#                     board.push(move)
#                     print("Black's move:", move.uci())

#         else:
#             print("Game over!")
#             print(outcome)
#             print("\nFinal position:")
#             print(board.unicode(invert_color=True))
#             return outcome
