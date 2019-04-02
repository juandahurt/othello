"""
    This module contains the main method. That's pretty much it...
    Oh! And it also creates and show a board for othello game.

    author: Juan David Hurtado - <juanhm@unicauca.edu.co>
"""

from board import Board
from tkinter import Tk

def main():
    root = Tk(className="othello!")
    Board(root)
    root.mainloop()

if __name__ == "__main__":
    main()