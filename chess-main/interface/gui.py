# Chess GUI
#
# This file contains a graphical user interface for displaying python-chess boards.
# Everything below is purely visual and has no relation to any of the core algorithms
# involved in the operation of our chess program. I simply thought it might become
# extremely tedious to do everything through the command line.
#
#   - Pearstopher
#
# Helpful references:
#   https://stackoverflow.com/questions/56984542
#   https://stackoverflow.com/questions/68057562
#


import sys
import os
import pygame
import chess
from button import Button
from ChessHelpers import ChessEngineHelper

dep = 4

# constants and configuration
TILE_SIZE = 64
BORDER = 10
INFO_HEIGHT = 100  # informational window below board
BOARD_POS = (BORDER, BORDER)
COLOR_DARK = (181, 136, 99)
COLOR_LIGHT = (240, 217, 181)
COLOR_BG = (22, 21, 18)
COLOR_DRAW_LINE = (22, 21, 18)
COLOR_DRAW_SELECT = (220, 10, 0, 50)
COLOR_DRAW_DRAG = (0, 220, 0, 50)
ENABLE_ILLEGAL_MOVES = False  # allow white to make custom moves (for testing)
IMAGE_PATH = "interface/images/"

BG = pygame.image.load("assets/Background.png")
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)    

# create the board surface by drawing the tiles
def create_board_surface():
    board_surface = pygame.Surface((TILE_SIZE*8, TILE_SIZE*8))
    dark = False
    for y in range(8):
        for x in range(8):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(board_surface, pygame.Color(COLOR_DARK if dark else COLOR_LIGHT), rect)
            dark = not dark
        dark = not dark
    return board_surface


def get_square_under_mouse(board):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - pygame.Vector2(BOARD_POS)
    x, y = [int(v // TILE_SIZE) for v in mouse_pos]
    try:
        if x >= 0 and y >= 0:
            return board[y][x], x, y
    except IndexError:
        pass
    return None, None, None


def create_board_from_fen(fen):
    board = []
    for y in range(8):
        board.append([])
        for x in range(8):
            board[y].append(None)
    col = 0
    row = 0
    for f in fen:
        if f == '/':
            col = col + 1
            row = 0
        elif f in ('1', '2', '3', '4', '5', '6', '7', '8'):
            row = row + int(f)
        elif f in ('K', 'k', 'Q', 'q', 'R', 'r', 'N', 'n', 'B', 'b', 'P', 'p'):
            board[int(col)][row] = get_piece(f)  # why suddenly need to ensure col is int?
            row = row + 1
    return board


def get_piece(f):
    if f == 'K':
        return 'white', 'king'
    elif f == 'k':
        return 'black', 'king'
    elif f == 'Q':
        return 'white', 'queen'
    elif f == 'q':
        return 'black', 'queen'
    elif f == 'R':
        return 'white', 'rook'
    elif f == 'r':
        return 'black', 'rook'
    elif f == 'N':
        return 'white', 'knight'
    elif f == 'n':
        return 'black', 'knight'
    elif f == 'B':
        return 'white', 'bishop'
    elif f == 'b':
        return 'black', 'bishop'
    elif f == 'P':
        return 'white', 'pawn'
    elif f == 'p':
        return 'black', 'pawn'


def draw_pieces(screen, board, font, selected_piece):
    sx, sy = None, None
    if selected_piece:
        piece, sx, sy = selected_piece

    for y in range(8):
        for x in range(8):
            piece = board[y][x]
            if piece:
                selected = x == sx and y == sy
                color, piece_type = piece
                s1 = pygame.image.load(resource_path(IMAGE_PATH + color + "/" + piece_type + ".png")).convert_alpha()
                s2 = pygame.image.load(resource_path(IMAGE_PATH + color + "/" + piece_type + ".png")).convert_alpha()
                if selected:
                    s2.fill((255, 255, 255, 90), None, pygame.BLEND_RGBA_MULT)
                    s1.fill((255, 255, 255, 90), None, pygame.BLEND_RGBA_MULT)
                pos = pygame.Rect(BOARD_POS[0] + x*TILE_SIZE + 1, BOARD_POS[1] + y*TILE_SIZE + 1, TILE_SIZE, TILE_SIZE)
                screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
                screen.blit(s1, s1.get_rect(center=pos.center))


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def draw_selector(screen, piece, x, y):
    if piece is not None:
        rect = (BOARD_POS[0] + x * TILE_SIZE, BOARD_POS[1] + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, COLOR_DRAW_SELECT, rect, 3)


def draw_drag(screen, board, selected_piece, font):
    if selected_piece:
        piece, x, y = get_square_under_mouse(board)
        if x is not None:
            rect = (BOARD_POS[0] + x * TILE_SIZE, BOARD_POS[1] + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, COLOR_DRAW_DRAG, rect, 3)

        color, piece_type = selected_piece[0]
        s1 = pygame.image.load(resource_path(IMAGE_PATH + color + "/" + piece_type + ".png")).convert_alpha()
        s2 = pygame.image.load(resource_path(IMAGE_PATH + color + "/" + piece_type + ".png")).convert_alpha()

        pos = pygame.Vector2(pygame.mouse.get_pos())
        screen.blit(s2, s2.get_rect(center=pos + pygame.Vector2((1, 1))))
        screen.blit(s1, s1.get_rect(center=pos))
        selected_rect = pygame.Rect(BOARD_POS[0] + selected_piece[1] * TILE_SIZE, BOARD_POS[1] +
                                    selected_piece[2] * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.line(screen, pygame.Color(COLOR_DRAW_LINE), selected_rect.center, pos, 2)
        return x, y

pygame.init()
REPLAY_MOUSE_POS = pygame.mouse.get_pos()
REPLAY_BUTTON = Button(image=pygame.image.load("assets/back3.png"), pos=(271, 590), 
                            text_input="REPLAY", font=get_font(15), base_color="#d7fcd4", hovering_color="White")
                    
for button in [REPLAY_BUTTON]:
    button.changeColor(REPLAY_MOUSE_POS)
    #button.update(screen) 

def draw_info(screen, chess_board, font):
    last_move_w = "White: "
    last_move_b = "Black: "
    ply = chess_board.ply()
    turn = chess_board.turn
                    
    #for button in [REPLAY_BUTTON]:
        #button.changeColor(REPLAY_MOUSE_POS)
        #button.update(screen)              
       
    if turn == chess.BLACK:
        last_move_b += chess_board.move_stack[ply - 2].uci()
        last_move_w += chess_board.peek().uci()
    else:
        if ply < 2:
            last_move_w += "None"
            last_move_b += "None"
        else:
            last_move_w += chess_board.move_stack[ply - 2].uci()
            last_move_b += chess_board.peek().uci()

    black_win = white_win = checkmate = ""
    outcome = chess_board.outcome()
    if outcome is not None:
        if outcome.winner is None:
            white_win = "Draw"
            black_win = "Draw"
            button.update(screen)
        elif outcome.winner == chess.WHITE:
            white_win = "White wins!"
            #checkmate = "Checkmate"
            button.update(screen)
        else:
            black_win = "Black wins!"
            #checkmate = "Checkmate"
            button.update(screen)



    s1 = font.render(last_move_w, True, pygame.Color(COLOR_LIGHT))
    s2 = font.render(last_move_b, True, pygame.Color(COLOR_DARK))
    s3 = font.render(white_win, True, pygame.Color(COLOR_DRAW_DRAG))
    s4 = font.render(black_win, True, pygame.Color(COLOR_DRAW_SELECT))
    s5 = font.render(checkmate, True, pygame.Color('white'))

    pos1 = pygame.Rect(BORDER, BORDER*3 + TILE_SIZE*8, TILE_SIZE*8, INFO_HEIGHT)
    pos2 = pygame.Rect(BORDER, BORDER*3 + TILE_SIZE*8, TILE_SIZE*8, INFO_HEIGHT)
    pos3 = pygame.Rect(BORDER, BORDER*3 + TILE_SIZE*8 + 25, TILE_SIZE*8, INFO_HEIGHT)
    pos4 = pygame.Rect(BORDER, BORDER*3 + TILE_SIZE*8 + 25, TILE_SIZE*8, INFO_HEIGHT)
    pos5 = pygame.Rect(BORDER, BORDER*3 + TILE_SIZE*8 + 25, TILE_SIZE*8, INFO_HEIGHT)
    screen.blit(s1, s1.get_rect(topleft=pos1.topleft))
    screen.blit(s2, s2.get_rect(topright=pos2.topright))
    screen.blit(s3, s2.get_rect(topleft=pos3.topleft))
    screen.blit(s4, s2.get_rect(topright=pos4.topright))
    screen.blit(s5, s2.get_rect(midtop=pos5.midtop))


# game loop
# white and black can each be passed a move generator function
# otherwise they both accept player moves through the UI

#BG = pygame.image.load("assets/Background.png")
#def get_font(size): # Returns Press-Start-2P in the desired size
    #return pygame.font.Font("assets/font.ttf", size)    

w = TILE_SIZE*8 + BORDER*2  # width of window
h = w + INFO_HEIGHT
screen = pygame.display.set_mode((w, h))
#screen.fill("white")

'''def options():
    run_option = True
    while run_option:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        board = chess.Board()
        move_generator = ChessEngineHelper.MoveGenerator()
        #screen.fill("white")
        #screen.fill("#3a0325")
        screen.fill("#2b021b")
        
        MENU_TEXT = get_font(50).render("OPTIONS", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(271, 71))

        LEVEL1_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(271, 195), 
                            text_input="Easy", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        LEVEL2_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(271, 324), 
                            text_input="Medium", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        LEVEL3_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(271, 454), 
                            text_input="Hard", font=get_font(35), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)
        OPTIONS_BACK = Button(image=None, pos=(271, 575), 
                            text_input="BACK", font=get_font(50), base_color="white", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for button in [LEVEL1_BUTTON, LEVEL2_BUTTON, LEVEL3_BUTTON]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    run_option = False
                    play_chess(board, black=move_generator.mini_max_move)

        pygame.display.update()'''

def options():
    run_option = True
    while run_option:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        board = chess.Board()
        #move_generator = ChessEngineHelper.MoveGenerator()
        #screen.fill("white")
        #screen.fill("#3a0325")
        screen.fill("#2b021b")
        
        MENU_TEXT = get_font(50).render("OPTIONS", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(271, 71))

        LEVEL1_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(271, 195), 
                            text_input="Easy", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        LEVEL2_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(271, 324), 
                            text_input="Medium", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        LEVEL3_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(271, 454), 
                            text_input="Hard", font=get_font(35), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)
        
        for button in [LEVEL1_BUTTON, LEVEL2_BUTTON, LEVEL3_BUTTON]:
            button.changeColor(OPTIONS_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if LEVEL1_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    dep = 1         
                    play_chess(board, black=ChessEngineHelper.MoveGenerator().mini_max_move)
                    pygame.quit()
                    sys.exit()
                if LEVEL2_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    play_chess(board, black=ChessEngineHelper.MoveGenerator().mini_max_move)
                    pygame.quit()
                    sys.exit()
                if LEVEL3_BUTTON.checkForInput(OPTIONS_MOUSE_POS):
                    play_chess(board, black=ChessEngineHelper.MoveGenerator().mini_max_move)
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def play_chess(chess_board, white="player", black="player"):
    pygame.init()
    font = pygame.font.SysFont('', 32)
    pygame.display.set_caption("Chess UI")
    #w = TILE_SIZE*8 + BORDER*2  # width of window
    #h = w + INFO_HEIGHT
    #screen = pygame.display.set_mode((w, h))
    # convert the real chess board object to custom board array
    board = create_board_from_fen(chess_board.board_fen())
    board_surface = create_board_surface()
    clock = pygame.time.Clock()
    selected_piece = None
    drop_pos = None
    piece = x = y = None
    
    running = False
    runmenu = True
    
    while runmenu and (not running):
        screen.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("CHESS", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(271, 71))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(271, 195), 
                            text_input="PLAY", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(271, 324), 
                            text_input="OPTIONS", font=get_font(35), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(271, 454), 
                            text_input="QUIT", font=get_font(35), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()      
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    running = True
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    #runmenu = False
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
    
    
    while running:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return chess_board.outcome()
        
        # don't try to play if the game is over
        outcome = chess_board.outcome()
        
        if outcome is None:

            if chess_board.turn == chess.WHITE and white == "player" \
                    or chess_board.turn == chess.BLACK and black == "player":
                piece, x, y = get_square_under_mouse(board)
                # events = pygame.event.get()
                for e in events:
                    if e.type == pygame.QUIT:
                        return outcome
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        if piece is not None:
                            selected_piece = piece, x, y
                        if BACK_BUTTON.checkForInput(BACK_MOUSE_POS):
                            play_chess(chess.Board(), black=ChessEngineHelper.MoveGenerator().mini_max_move)
                            pygame.quit()
                            sys.exit()
                        if REPLAY_BUTTON.checkForInput(REPLAY_MOUSE_POS):
                            play_chess(chess.Board(), black=ChessEngineHelper.MoveGenerator().mini_max_move)
                            pygame.quit()
                            sys.exit()
                    if e.type == pygame.MOUSEBUTTONUP:
                        if drop_pos:
                            piece, old_x, old_y = selected_piece
                            new_x, new_y = drop_pos
                            if new_x is not None and new_y is not None:
                                # horrible math to convert board array position to chess.Square
                                # I have to reverses the columns since my array starts at A8 not A1
                                move = chess.Move(((7 - old_y)*8 + old_x), ((7 - new_y)*8 + new_x))
                                move2 = chess.Move(((7 - old_y)*8 + old_x), ((7 - new_y)*8 + new_x), chess.QUEEN)
                                # quick hack to enable pawn promotion
                                if move2 in chess_board.legal_moves:
                                    # push the move to the real chess board
                                    chess_board.push(move2)
                                    # update our array representation
                                    board[int(old_y)][old_x] = None
                                    board[int(new_y)][new_x] = ('white', 'queen')
                                elif move in chess_board.legal_moves or ENABLE_ILLEGAL_MOVES:
                                    # push the move to the real chess board
                                    chess_board.push(move)
                                    # update our array representation
                                    board[int(old_y)][old_x] = None
                                    board[new_y][new_x] = piece
                                # this refresh will reset the board if a piece was dragged somewhere invalid
                                board = create_board_from_fen(chess_board.board_fen())
                        selected_piece = None
                        drop_pos = None
                    
            else:
                # generate and push a move to the real chess board
                if chess_board.turn == chess.WHITE:
                    move = white(chess_board)
                    if move is False:
                        return
                    chess_board.push(move)
                else:
                    move = black(chess_board)
                    if move is False:
                        return
                    chess_board.push(move)
                # update our array representation for the UI
                board = create_board_from_fen(chess_board.board_fen())
                # end of move generation
                

        
        screen.fill(pygame.Color(COLOR_BG))
        screen.blit(board_surface, BOARD_POS)
        BACK_MOUSE_POS = pygame.mouse.get_pos()
        BACK_BUTTON = Button(image=pygame.image.load("assets/back3.png"), pos=(271, 554), 
                            text_input="MENU", font=get_font(15), base_color="#d7fcd4", hovering_color="White")
        for button in [BACK_BUTTON]:
            button.changeColor(BACK_MOUSE_POS)
            button.update(screen)
        
        draw_pieces(screen, board, font, selected_piece)
        
        if drop_pos:
            draw_selector(screen, piece, x, y)
        drop_pos = draw_drag(screen, board, selected_piece, font)
        draw_info(screen, chess_board, font)
             
        pygame.display.flip()
        clock.tick(60)
