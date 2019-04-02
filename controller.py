import alpha_beta
from constants import PLAYER, CPU, EMPTY_SPACE, INITIAL_STATE, NUM_COLS, NUM_ROWS
from alpha_beta import AlphaBeta
from othello import Othello

controller = None

def start_game(board):
    controller.start_game()

def touch_board(pos):
    if not controller is None:
        controller.touch_board(pos)

class Controller:
    """Create a controller that's in charge of the board's behaviour.

        Atributtes:
            state (list): The actual state of the game. It's a representation of the board.
            board (Board): The board. This controller is in charge of it.
            waiting_movement (bool): Is the board waiting for the player to move?
            initial_pos (tuple): The initial position for any move.
            player (int): Representation of the current player.

        Args:
            board (Board): The board of the game.
    """
    def __init__(self, board):
        self.state = INITIAL_STATE
        self.board = board
        self.game = Othello()
        self.waiting_movement = False
        self.initial_pos = (-1,-1)
        self.player = PLAYER


    def touch_board(self, pos):
        """It's called every time the player clicks on the board.

            Atributtes:
                pos (dict): The coordinates where the player clicked on the board.
                    keys = "x", "y".
        """
        row = int((pos["x"] / self.board.cellwidth))
        col = int((pos["y"] / self.board.cellheight))
        print("{0} {1}".format(row,col))
        if row < 0 or row >= NUM_ROWS or col < 0 or col >= NUM_COLS:
            raise Exception
        if self.player == PLAYER:
            if self.state[row][col] == PLAYER:
                if not self.waiting_movement:
                    self.board.draw_chip(PLAYER, row, col, True)
                    self.waiting_movement = True
                    self.initial_pos = (row,col)
            if self.state[row][col] == EMPTY_SPACE and self.waiting_movement:
                final_pos = (row, col)
                if self.__try_to_move(final_pos):
                    self.player = CPU
            if self.state[row][col] == CPU or self.state[row][col] == PLAYER:
                if self.waiting_movement and self.initial_pos != (row,col):
                    self.waiting_movement = False
        else:
            alpha_beta = AlphaBeta(self.game, 3)
            cpu_action = alpha_beta.alpha_beta_search(self.state)
            if cpu_action is None:
                # the machine doesn't know what to do!
                self.__player_won()
            else:
                self.state = cpu_action
            self.player = PLAYER
        if not self.waiting_movement:
            self.board.draw_chips(self.state)

    def __try_to_move(self, final_pos):
        """Find out whether if it's possible for the player to move or not.

            Returns: 
                True if it's possible to move.
        """
        initial_x = self.initial_pos[0]
        initial_y = self.initial_pos[1]
        final_x = final_pos[0]
        final_y = final_pos[1]
        is_possible_to_move = False
        if self.state[final_x][final_y] == EMPTY_SPACE:
            # horizontal movements
            if initial_y == final_y:
                # x+ axis
                if final_x - initial_x == 2:
                    if initial_x + 1 < self.board.width:
                        if self.state[initial_x + 1][initial_y] == CPU:
                            self.state[initial_x + 1][initial_y] = PLAYER
                            self.state[final_x][final_y] = PLAYER
                            is_possible_to_move = True
                # x- axis
                if final_x - initial_x == -2:
                    if initial_x - 1 >= 0:
                        if self.state[initial_x - 1][initial_y] == CPU:
                            self.state[initial_x - 1][initial_y] = PLAYER
                            self.state[final_x][final_y] = PLAYER
                            is_possible_to_move = True
            # vertical movements
            if initial_x == final_x:
                # y+ axis
                if final_y - initial_y == 2:
                    if initial_y + 1 < self.board.width:
                        if self.state[initial_x][initial_y + 1] == CPU:
                            self.state[initial_x][initial_y + 1] = PLAYER
                            self.state[final_x][final_y] = PLAYER
                            is_possible_to_move = True
                # y- axis
                if final_y - initial_y == -2:
                    if initial_y - 1 >= 0:
                        if self.state[initial_x][initial_y - 1] == CPU:
                            self.state[initial_x][initial_y - 1] = PLAYER
                            self.state[final_x][final_y] = PLAYER
                            is_possible_to_move = True
            # diagonal movements
            # upper right diagonal
            if final_x == initial_x + 2 and final_y == initial_y - 2:
                self.state[initial_x + 1][initial_y - 1] = PLAYER
                self.state[final_x][final_y] = PLAYER
                is_possible_to_move = True
            # upper left diagonal
            if final_x == initial_x - 2 and final_y == initial_y - 2:
                self.state[initial_x - 1][initial_y - 1] = PLAYER
                self.state[final_x][final_y] = PLAYER
                is_possible_to_move = True
            # lower right diagonal
            if final_x == initial_x + 2 and final_y == initial_y + 2:
                self.state[initial_x + 1][initial_y + 1] = PLAYER
                self.state[final_x][final_y] = PLAYER
                is_possible_to_move = True
            # lower left diagonal
            if final_x == initial_x - 2 and final_y == initial_y + 2:
                self.state[initial_x - 1][initial_y + 1] = PLAYER
                self.state[final_x][final_y] = PLAYER
                is_possible_to_move = True
        self.initial_pos = (-1,-1)
        self.waiting_movement = False
        return is_possible_to_move

    def __player_won(self):
        self.board.show_player_victory()

    def start_game(self):
        self.board.draw_grid()
        self.board.draw_chips(self.state)

    def game_over(self):
        exit()
