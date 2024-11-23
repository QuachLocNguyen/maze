# Tài liệu tham khảo
# A. Artasanchez, P. Joshi, 
# Artificial Intelligence with Python, 
# 2nd Edition, Packt, 2020
# Trang 242

import math
from simpleai.search import SearchProblem, astar
import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
import time

# Define cost of moving around the map
cost_regular = 1.0
cost_diagonal = 1.7

# Create the cost dictionary
COSTS = {
    "up": cost_regular,
    "down": cost_regular,
    "left": cost_regular,
    "right": cost_regular,
}

# Define the map
MAP = """
##############################
#         #              #   #
# ####    ########       #   #
#    #    #              #   #
#    ###     #####  ######   #
#      #   ###   #           #
#      #     #   #  #  #   ###
#     #####    #    #  #     #
#              #       #     #
##############################
"""

# Convert map to a list
MAP = [list(x) for x in MAP.split("\n") if x]
M = 10
N = 30
W = 21
mau_xanh  = np.zeros((W,W,3), np.uint8) + (np.uint8(255), np.uint8(0), np.uint8(0))
mau_trang = np.zeros((W,W,3), np.uint8) + (np.uint8(255), np.uint8(255), np.uint8(255))
image = np.ones((M*W, N*W, 3), np.uint8)*255

for x in range(0, M):
    for y in range(0, N):
        if MAP[x][y] == '#':
            image[x*W:(x+1)*W, y*W:(y+1)*W] = mau_xanh
        elif MAP[x][y] == ' ':
            image[x*W:(x+1)*W, y*W:(y+1)*W] = mau_trang

color_coverted = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
pil_image = Image.fromarray(color_coverted)


# Class containing the methods to solve the maze
class MazeSolver(SearchProblem):
    # Initialize the class 
    def __init__(self, board):
        self.board = board
        self.goal = (0, 0)

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x].lower() == "o":
                    self.initial = (x, y)
                elif self.board[y][x].lower() == "x":
                    self.goal = (x, y)

        super(MazeSolver, self).__init__(initial_state=self.initial)

    # Define the method that takes actions
    # to arrive at the solution
    def actions(self, state):
        actions = []
        for action in COSTS.keys():
            newx, newy = self.result(state, action)
            if self.board[newy][newx] != "#":
                actions.append(action)

        return actions

    # Update the state based on the action
    def result(self, state, action):
        x, y = state

        if action.count("up"):
            y -= 1
        if action.count("down"):
            y += 1
        if action.count("left"):
            x -= 1
        if action.count("right"):
            x += 1

        new_state = (x, y)

        return new_state

    # Check if we have reached the goal
    def is_goal(self, state):
        return state == self.goal

    # Compute the cost of taking an action
    def cost(self, state, action, state2):
        return COSTS[action]

    # Heuristic that we use to arrive at the solution
    def heuristic(self, state):
        x, y = state
        gx, gy = self.goal

        return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)


class App(tk.Tk):
    def	__init__(self):
        super().__init__()
        self.dem = 0
        self.title('Tìm đường trong mê cung')
        self.cvs_me_cung = tk.Canvas(self, width = N*W, height = M*W,
                                relief = tk.SUNKEN, border = 1)

        self.image_tk = ImageTk.PhotoImage(pil_image)
        self.cvs_me_cung.create_image(0, 0, anchor = tk.NW, image = self.image_tk)

        self.cvs_me_cung.bind("<Button-1>", self.xu_ly_mouse)

        lbl_frm_menu = tk.LabelFrame(self)
        btn_start = tk.Button(lbl_frm_menu, text = 'Start', width = 7,
                              command = self.btn_start_click)
        btn_reset = tk.Button(lbl_frm_menu, text = 'Reset', width = 7,
                              command = self.btn_reset_click)
        btn_start.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = tk.N)
        btn_reset.grid(row = 1, column = 0, padx = 5, pady = 5, sticky = tk.N)

        self.cvs_me_cung.grid(row = 0, column = 0, padx = 5, pady = 5)
        lbl_frm_menu.grid(row = 0, column = 1, padx = 5, pady = 7, sticky = tk.NW)

    def xu_ly_mouse(self, event):
        px = event.x
        py = event.y
        x = px // W
        y = py // W
        if MAP[y][x] != '#':
            if self.dem == 0:
                MAP[y][x] = 'o'
                self.cvs_me_cung.create_oval(x*W+2, y*W+2, (x+1)*W-2, (y+1)*W-2, 
                                            outline = '#FF0000', fill = '#FF0000')
                self.dem = self.dem + 1
            elif self.dem == 1:
                MAP[y][x] = 'x'
                self.cvs_me_cung.create_rectangle(x*W+2, y*W+2, (x+1)*W-2, (y+1)*W-2, 
                                            outline = '#FF0000', fill = '#FF0000')
                self.dem = self.dem + 1

    def btn_start_click(self):
        problem = MazeSolver(MAP)
        # Run the solver
        result = astar(problem, graph_search=True)

        # Extract the path
        path = [x[1] for x in result.path()]

        # Print the result
        '''
        print()
        for y in range(len(MAP)):
            for x in range(len(MAP[y])):
                if (x, y) == problem.initial:
                    print('o', end='')
                elif (x, y) == problem.goal:
                    print('x', end='')
                elif (x, y) in path:
                    print('·', end='')
                else:
                    print(MAP[y][x], end='')
            print()
        print(path)
        '''
        L = len(path)
        for i in range(1, L):
            x = path[i][0]
            y = path[i][1]
            self.cvs_me_cung.create_rectangle(x*W+2, y*W+2, (x+1)*W-2, (y+1)*W-2, 
                                         outline = '#FF0000', fill = '#FF0000')
            time.sleep(0.5)
            self.cvs_me_cung.update()

    def btn_reset_click(self):
        self.cvs_me_cung.delete(tk.ALL)
        self.cvs_me_cung.create_image(0, 0, anchor = tk.NW, image = self.image_tk)
        self.dem = 0
        for x in range(0, M):
            for y in range(0, N):
                if MAP[x][y] == 'o' or MAP[x][y] == 'x':
                    MAP[x][y] = ' '

if	__name__ ==	"__main__":
    app	=	App()
    app.mainloop()
