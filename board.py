from tkinter import Button, Canvas, Frame, Tk, messagebox

import controller
from constants import CPU, CPU_COLOR, PLAYER, PLAYER_COLOR, WHITE_CELL, BROWN_CELL, CHIP_PRESSED, NUM_COLS, NUM_ROWS
from controller import Controller

class Board():
    """Create a board for the game.

        Atributtes:
            frame (Frame): Main frame of the game
            height (int): The height of the canvas
            width (int): The width of the Canvas
            
        Parameters:
            master: the main window
    """
    def __init__(self, master):
        self.frame = Frame(master)
        self.frame.pack()
        self.height = 600
        self.width = 600
        self.canvas = Canvas(self.frame, height=self.height, width=self.width)
        self.cellwidth = int(self.canvas["width"]) / NUM_COLS
        self.cellheight = int(self.canvas["height"]) / NUM_ROWS
        self.canvas.pack()
        
        
        def handler(event, self=self):
            return self.touch_board(event)
        
        self.canvas.bind('<Button-1>', handler)
        
        
        self.play_button = Button(self.frame, text="Play", command=self.start_game)
        self.play_button.pack(side='left')
        self.give_up_button = Button(self.frame, text="Give up...", command=self.give_up)
        self.give_up_button.pack(side='left')
        
    def draw_grid(self):
        just_draw_white = False
        for row in range(NUM_ROWS):
            just_draw_white = not just_draw_white
            for col in range(NUM_COLS):
                x1 = row * self.cellwidth
                y1 = col * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                if not just_draw_white:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=WHITE_CELL)
                    just_draw_white = True
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=BROWN_CELL)
                    just_draw_white = False
        
    def draw_chip(self, current_player, row, col, waiting=False):
        x = row * self.cellwidth
        y = col * self.cellheight
        if current_player == PLAYER:
            color = PLAYER_COLOR
            if waiting: 
                color = CHIP_PRESSED
            self.canvas.create_oval(x,y,x+self.cellwidth,y+self.cellheight, fill=color)
        else:
            self.canvas.create_oval(x,y,x+self.cellwidth,y+self.cellheight, fill=CPU_COLOR)
    
    def draw_chips(self, state):
        for i in range(len(state)):
            row = state[i]
            for j in range(len(row)):
                val = state[i][j]
                if val == PLAYER:
                    self.draw_chip(PLAYER, i, j)
                elif val == CPU:
                    self.draw_chip(CPU, i, j)
            
    def touch_board(self, event):
        pos = {
            "x": event.x,
            "y": event.y
        }
        controller.touch_board(pos)
        
    def give_up(self):
        if not controller.controller is None:
            controller.controller.game_over()
    
    def start_game(self):
        controller.controller = Controller(self)
        controller.start_game(self)

    def show_player_victory(self):
        messagebox.showinfo("Congratulations!", "I don't know what to do...")
        play_again = messagebox.askyesno("You're leaving me?", "Would you like to play again? I promess i'll smoke you this time.")
        if not play_again:
            controller.controller.game_over()
        else:
            self.start_game()
