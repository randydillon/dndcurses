import curses
from .application import Application

def main(stdscr):
    app = Application(stdscr)
    app.run()

if __name__ == "__main__":
    curses.wrapper(main)
