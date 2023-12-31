from pathlib import Path
import tkinter as tk
import tkinter.font as tkfont
import pyglet
from PIL import Image, ImageTk
from game_grid import GameGrid
from player import Player, GpuPlayer
from mark import Mark
from game_logic import GameLogic
import time

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
        self.mode = 0
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
        for F in (StartPage, PlayersPage, GamePage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.event_generate("<<ShowFrame>>")
        frame.tkraise()

    def set_single_player(self):
        self.mode = 1

    def set_multiplayer(self):
        self.mode = 2


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
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
        welcome_label = tk.Label(self, text="Welcome! Please select a mode.",
                                 font=tkfont.Font(family='MouldyCheeseRegular', size=18))
        welcome_label.config(background=BACKGROUND_COLOR, foreground=FONT_COLOR)
        welcome_label.grid(row=1, column=1, padx=10, pady=10)

    def create_grid_canvas(self):
        canvas = tk.Canvas(self, width=564, height=666)
        canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
        canvas.create_image(X_CENTER, Y_CENTER, image=self.grid_image)
        canvas.grid(row=2, column=0, columnspan=3)
        return canvas

    def create_buttons(self, controller):
        multi_player_button = tk.Button(self, text='Multi Player',
                                        font=tkfont.Font(family='MouldyCheeseRegular', size=15),
                                        command=lambda: self.multi_player(controller))
        multi_player_button.config(background=BUTTON_COLOR, foreground=FONT_COLOR)
        multi_player_button.grid(column=0, row=3)

        one_player_button = tk.Button(self, text='Single Player',
                                      font=tkfont.Font(family='MouldyCheeseRegular', size=15),
                                      command=lambda: self.single_player(controller))
        one_player_button.config(background=BUTTON_COLOR, foreground=FONT_COLOR)
        one_player_button.grid(column=2, row=3)

    def single_player(self, controller):
        controller.set_single_player()
        controller.show_frame(GamePage)

    def multi_player(self, controller):
        controller.set_multiplayer()
        controller.show_frame(GamePage)


class GamePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.game_grid = self.create_grid()
        self.config(background=BACKGROUND_COLOR)
        self.grid_image = ImageTk.PhotoImage(Image.open(GRID_FILE))
        self.cross_image = ImageTk.PhotoImage(Image.open(CROSS_FILE))
        self.o_image = ImageTk.PhotoImage(Image.open(O_FILE))
        self.cross_mark = Mark(1, self.cross_image)
        self.o_mark = Mark(2, self.o_image)
        self.game = GameLogic(3)
        self.player1 = Player("Player 1", self.cross_mark)
        self.player2 = self.create_player2()
        self.current_player = self.player1
        self.marks = []
        self.create_title_label()
        self.player1_label = self.create_player1_label()
        self.player2_label = self.create_player2_label()
        self.current_player_label = self.create_current_player_label()
        self.canvas = self.create_grid_canvas()
        self.create_buttons(controller)
        self.game_over = False
        self.bind("<<ShowFrame>>", self.on_show_page)

    def on_show_page(self, event):
        self.init_game()

    def create_player2(self):
        if self.controller.mode == 1:
            return GpuPlayer(mark=self.o_mark, game=self.game)
        return Player("Player 2", self.o_mark)

    def create_title_label(self):
        title_label = tk.Label(self, text='Tic Tac Toe', font=tkfont.Font(family='MouldyCheeseRegular', size=44))
        title_label.config(background=BACKGROUND_COLOR, foreground=FONT_COLOR)
        title_label.grid(row=0, column=1, padx=10, pady=10)

    def create_player1_label(self):
        player1_label = tk.Label(self, text=f"{self.player1.name}: {self.player1.score}",
                                 font=tkfont.Font(family='MouldyCheeseRegular', size=18))
        player1_label.config(background=BACKGROUND_COLOR, foreground=FONT_COLOR)
        player1_label.grid(row=1, column=0, padx=10, pady=10)
        return player1_label

    def create_player2_label(self):
        player2_label = tk.Label(self, text=f"{self.player2.name}: {self.player2.score}",
                                 font=tkfont.Font(family='MouldyCheeseRegular', size=18))
        player2_label.config(background=BACKGROUND_COLOR, foreground=FONT_COLOR)
        player2_label.grid(row=1, column=2, padx=10, pady=10)
        return player2_label

    def create_current_player_label(self):
        current_player_label = tk.Label(self, text=f"{self.current_player.name}",
                                        font=tkfont.Font(family='MouldyCheeseRegular', size=18))
        current_player_label.config(background=BACKGROUND_COLOR, foreground=FONT_COLOR)
        current_player_label.grid(row=3, column=1)
        return current_player_label

    def create_grid_canvas(self):
        canvas = tk.Canvas(self, width=564, height=666)
        canvas.bind('<ButtonPress>', self.mouse_click)
        canvas.config(background=BACKGROUND_COLOR, highlightthickness=0)
        canvas.create_image(X_CENTER, Y_CENTER, image=self.grid_image)
        canvas.grid(row=2, column=0, columnspan=3, padx=10)
        return canvas

    def create_buttons(self, controller):
        back_button = tk.Button(self, text='Back',
                                font=tkfont.Font(family='MouldyCheeseRegular', size=15),
                                command=lambda: self.back_to_home(controller))
        back_button.config(background=BUTTON_COLOR, foreground=FONT_COLOR)
        back_button.grid(column=0, row=3)

        new_game_button = tk.Button(self, text='New Game',
                                    font=tkfont.Font(family='MouldyCheeseRegular', size=15),
                                    command=self.new_game)
        new_game_button.config(background=BUTTON_COLOR, foreground=FONT_COLOR)
        new_game_button.grid(column=2, row=3)

    def mouse_click(self, e):
        if self.game_over:
            return
        block = self.game_grid.which_block(e.x, e.y)
        if not block:
            return
        print(f"Player mark:{block[0], block[1]}")
        is_valid = self.add_mark(block[0], block[1])
        if not is_valid:
            return
        self.check_game_over()
        if self.controller.mode == 1:
            self.computer_turn()

    def computer_turn(self):
        if not self.game_over:
            # time.sleep(1)
            cpu_mark = self.player2.place_mark()
            print(f"Cpu mark : {cpu_mark}")
            self.add_mark(cpu_mark[0], cpu_mark[1])
            self.check_game_over()
            self.game.print_grid()

    def add_mark(self, row, column):
        is_valid = self.game.add_mark(self.current_player.mark.value, row, column)
        if not is_valid:
            return False
        x_cord, y_cord = self.game_grid.get_block_center(row, column)
        new_mark = self.canvas.create_image(x_cord, y_cord, image=self.current_player.mark.image)
        self.marks.append(new_mark)
        return True

    def clear_grid(self):
        for mark in self.marks:
            self.canvas.delete(mark)

    def change_current_player(self):
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
        self.update_labels()

    def check_game_over(self):
        if self.game.is_won():
            self.current_player.increment_score()
            self.current_player_label.config(text=f"{self.current_player.name} won")
            self.game_over = True
        elif self.game.is_grid_full():
            self.current_player_label.config(text=f"It's a draw")
            self.game_over = True
        else:
            self.change_current_player()

    def init_game(self):
        self.player2 = self.create_player2()
        self.update_labels()
        self.clear_grid()
        self.game.reset_grid()
        self.game_over = False

    def new_game(self):
        self.clear_grid()
        self.game.reset_grid()
        self.update_labels()
        self.game_over = False
        self.change_current_player()
        if self.controller.mode == 1 and self.current_player == self.player2:
            self.computer_turn()

    def update_labels(self):
        self.player1_label.config(text=f"{self.player1.name}: {self.player1.score}")
        self.player2_label.config(text=f"{self.player2.name}: {self.player2.score}")
        self.current_player_label.config(text=f"{self.current_player.name}")

    def back_to_home(self, controller):
        self.reset_frame()
        controller.show_frame(StartPage)

    def reset_frame(self):
        self.new_game()
        self.player1.score = 0
        self.player2.score = 0
        self.current_player = self.player1
        self.update_labels()

    @staticmethod
    def create_grid():
        return GameGrid(
            rows=3,
            columns=3,
            row_offset=50,
            column_offset=0,
            block_width=163,
            block_height=163,
            frame_width=36
        )


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

        player2_label = tk.Label(self, text='Player 2 name: ', font=tkfont.Font(family='MouldyCheeseRegular', size=15))
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
