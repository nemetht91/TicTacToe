from pathlib import Path
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
import pyglet
from PIL import Image, ImageTk
from game_grid import GameGrid

pyglet.options['win32_gdi_font'] = True
font_path = Path(__file__).parent / 'fonts/MouldyCheeseRegular-WyMWG.ttf'
pyglet.font.add_file(str(font_path))

BACKGROUND_COLOR = '#CEDEBD'
FONT_COLOR = '#435334'
BUTTON_COLOR = '#9EB384'
INPUT_COLOR = '#FAF1E4'

GRID_FILE = 'images/converted/grid.png'
CROSS_FILE = 'images/converted/cross.png'
O_FILE = 'images/converted/o.png'

X_CENTER = 282
Y_CENTER = 333


class TicTacToeUi(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Tic Tac Toe')
        self.minsize(width=500, height=300)
        self.config(padx=50, pady=25)
        self.config(background=BACKGROUND_COLOR)
        self.container = self._create_container()
        self.frames = {}
        self._add_frames(self.container)
        self.show_frame(StartPage)

    def _create_container(self):
        container = tk.Frame(self)
        container.grid(row=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        return container

    def _add_frames(self, container):
        for F in (StartPage, PlayersPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.game_grid = self.create_grid()
        self.config(background=BACKGROUND_COLOR)
        self.grid_image = ImageTk.PhotoImage(Image.open(GRID_FILE))
        self.cross_image = ImageTk.PhotoImage(Image.open(CROSS_FILE))
        self.o_image = ImageTk.PhotoImage(Image.open(O_FILE))
        self.marks = []
        self.create_title_label()
        self.canvas = self.create_grid_canvas()
        self.create_buttons(controller)

    def create_title_label(self):
        title_label = tk.Label(self, text='Tic Tac Toe', font=tkfont.Font(family='MouldyCheeseRegular', size=44))
        title_label.config(background=BACKGROUND_COLOR, foreground=FONT_COLOR)
        title_label.grid(row=0, column=1, padx=10, pady=10)

    def create_grid_canvas(self):
        canvas = tk.Canvas(self, width=564, height=666)
        canvas.bind('<ButtonPress>', self.mouse_click)
        canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
        canvas.create_image(X_CENTER, Y_CENTER, image=self.grid_image)
        canvas.grid(row=1, column=0, columnspan=3)
        return canvas

    def create_buttons(self, controller):
        multi_player_button = tk.Button(self, text='Multi Player',
                                        font=tkfont.Font(family='MouldyCheeseRegular', size=15),
                                        command=lambda: controller.show_frame(PlayersPage))
        multi_player_button.config(background=BUTTON_COLOR, foreground=FONT_COLOR)
        multi_player_button.grid(column=0, row=3)

        one_player_button = tk.Button(self, text='Single Player',
                                      font=tkfont.Font(family='MouldyCheeseRegular', size=15),
                                      command=self.clear_grid)
        one_player_button.config(background=BUTTON_COLOR, foreground=FONT_COLOR)
        one_player_button.grid(column=2, row=3)

    def mouse_click(self, e):
        block = self.game_grid.which_block(e.x, e.y)
        if block:
            self.add_cross(block[0], block[1])

    def add_cross(self, row, column):
        x_cord, y_cord = self.game_grid.get_block_center(row, column)
        new_mark = self.canvas.create_image(x_cord, y_cord, image=self.cross_image)
        self.marks.append(new_mark)

    def clear_grid(self):
        for mark in self.marks:
            self.canvas.delete(mark)

    @staticmethod
    def create_grid():
        return GameGrid(
            rows=3,
            columns=3,
            row_offset=0,
            column_offset=50,
            block_width=163,
            block_height=163,
            frame_width=36
        )


class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=BACKGROUND_COLOR)
        self.grid_image = ImageTk.PhotoImage(Image.open(GRID_FILE))
        self.cross_image = ImageTk.PhotoImage(Image.open(CROSS_FILE))
        self.o_image = ImageTk.PhotoImage(Image.open(O_FILE))
        title_label = tk.Label(self, text='Tic Tac Toe', font=tkfont.Font(family='MouldyCheeseRegular', size=44))
        title_label.config(background=BACKGROUND_COLOR, foreground=FONT_COLOR)
        title_label.grid(row=0, column=1, padx=10, pady=10)

        canvas = tk.Canvas(self, width=564, height=666)
        canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
        canvas.create_image(X_CENTER, Y_CENTER, image=self.grid_image)

        canvas.grid(row=1, column=0, columnspan=3)

        multi_player_button = tk.Button(self, text='Multi Player',
                                        font=tkfont.Font(family='MouldyCheeseRegular', size=15),
                                        command=lambda: controller.show_frame(PlayersPage))
        multi_player_button.config(background=BUTTON_COLOR, foreground=FONT_COLOR)
        multi_player_button.grid(column=0, row=3)

        one_player_button = tk.Button(self, text='Single Player',
                                      font=tkfont.Font(family='MouldyCheeseRegular', size=15))
        one_player_button.config(background=BUTTON_COLOR, foreground=FONT_COLOR)
        one_player_button.grid(column=2, row=3)


class PlayersPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(background=BACKGROUND_COLOR)
        title_label = tk.Label(self, text='Tic Tac Toe', font=tkfont.Font(family='MouldyCheeseRegular', size=44))
        title_label.config(background=BACKGROUND_COLOR, foreground=FONT_COLOR)
        title_label.grid(row=0, column=1, padx=10, pady=10)

        player1_label = tk.Label(self, text='Player 1 name: ', font=tkfont.Font(family='MouldyCheeseRegular', size=15))
        player1_label.config(background=BACKGROUND_COLOR, foreground=FONT_COLOR)
        player1_label.grid(row=1, column=0)

        player1_details = tk.Entry(self, width=20, show='Player 1')
        player1_details.grid(row=1, column=1)

        player2_label = tk.Label(self, text='Player 2 name: ',  font=tkfont.Font(family='MouldyCheeseRegular', size=15))
        player2_label.config(background=BACKGROUND_COLOR, foreground=FONT_COLOR)
        player2_label.grid(row=2, column=0)

        player2_details = tk.Entry(self, width=20, show='Player 2')
        player2_details.grid(row=2, column=1)

        back_button = tk.Button(self, text='Back', font=tkfont.Font(family='MouldyCheeseRegular', size=18),
                                command=lambda: controller.show_frame(StartPage))
        back_button.config(background=BUTTON_COLOR, foreground=FONT_COLOR)
        back_button.grid(row=4, column=0)

        start_button = tk.Button(self, text='Start', font=tkfont.Font(family='MouldyCheeseRegular', size=18))
        start_button.config(background=BUTTON_COLOR, foreground=FONT_COLOR)
        start_button.grid(row=4, column=3)


app = TicTacToeUi()
app.mainloop()