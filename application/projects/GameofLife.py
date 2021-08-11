"""
DSC 430
Adam Klaus
March 8th, 2021
Video Link: https://youtu.be/9Om-TLvBMRM
"I have not given or received any unauthorized assistance on this assignment"
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
os.chdir(os.getcwd())

# Failed test case of p = 1. Only corners should survive on second turn. This was not the case for your code.

class GameOfLife:

    """
    Attributes
    s: int
        size of the board by length
    p: float
        probability threshold to set up inital board of whether or not a cell is alive or dead
    grids: list of np.array
        list of each iteration of the board, will be used to display board progression
    b: np.array
        current iteration of the board
    fig: plot object
        figure to display the results on the board
    """

    def __init__(self, s, p=.1):
        self.s = s
        self.p = p
        self.grids = []
        self.b = self.conway(self.s, self.p)

    def conway(self, s, p=.1):
        """
        generate a conway board, whcih is a square 2d array size s by s
        :param s: int size of the board
        :param p: probability
        """
        b = np.random.random((s,s)) #create s by s board
        b  = np.where(b < p, 1, 0) #where values are less than
        self.grids.append(b)

        return b

    def advance(self,t):
        """
        using conway board b, advance the outcomes of the board by t steps

        :param b: conway board object
        :param t: number of steps to advance the board
        """
        self.steps = t
        for i in range(t):
            new_b = self.b.copy() #get size of board
            self.new_grid(new_b)

    def new_grid(self, new_b):
        """
        advance the grid one time t=1 based on the current state of the grid

        :param new_b: copy of existing board that will be updated with the new outcomes and become the new board
        """
        for x in range(self.s):
            for y in range(self.s):
                value = self.b[x, y]
                neigh_sum = self.alive_neighbor_count(self.b, x, y)
                updated_value = self.dead_or_alive(value, neigh_sum)
                new_b[x,y] = updated_value
        self.b = new_b
        self.grids.append(new_b) #add frame to plot list
    

    def dead_or_alive(self, value, neigh_sum):
        """
        determine whether or not each cell should survive based on the rules of the game

        :param value: int whether or not the cell is currently alive or dead
        :param neigh_sum: int sum of the neighbor of alive neighbors for the cell

        :return: int updated value for the new interation of the board
        """
        if value == 1 and neigh_sum <2:
            return 0
        elif value == 1 and neigh_sum >3:
            return 0
        elif value == 1 and neigh_sum >=2 and neigh_sum<=3:
            return 1
        elif value == 0 and neigh_sum == 3:
            return 1
        return value
 

    def alive_neighbor_count(self, b, x, y):
        """
        Using the dictionary of the values of the neighbors around a particular cell, determine how many are alive

        :param b: np.array current board
        :param x: int x coordinate for a given cell on the board
        :param y: int y coordinate for a given cell on the board
        :return: neigh_sum, int sum of the neighbors around the cell that represents the number that are alive  
        """
        neighbors = self.neighbor_dict(b, x, y)
        neigh_sum = self.get_neighbor_sum(b, neighbors)
        return neigh_sum

    def neighbor_dict(self, b, x, y):
        """
        create a dictionary to represent the neighbors around a given cell. Keys are locations around the cell and values are a list with [x,y] coordinates

        :param b: np.array current board
        :param x: int x coordinate for a given cell on the board
        :param y: int y coordinate for a given cell on the board
        :return: dictionary of the neighbors coordinates for a given cell
        """
        neighbors_dict = {}
        neighbors_dict['bottom_left'] = [x-1, y-1]
        neighbors_dict['mid_left'] = [x-1, y]
        neighbors_dict['top_left'] = [x-1, y+1]
        neighbors_dict['bottom_mid'] = [x, y-1]
        neighbors_dict['top_mid'] = [x, y+1]
        neighbors_dict['bottom_right'] = [x+1, y-1]
        neighbors_dict['mid_right'] = [x+1, y]
        neighbors_dict['top_right'] = [x+1, y+1]
        return neighbors_dict

    def get_neighbor_sum(self, b, neighbors_dict):
        """
        calculate the number of alive neighbors around a given cell by taking into account the wrapping around of the boards boundaries
        
        :param b: np.array current board
        :param neighbors_dict: dictionary of the neighbors coordinates for a given cell
        :return: neigh_sum, int sum of the neighbors around the cell that represents the number that are alive  
        """
        neigh_sum = 0
        for tup in neighbors_dict.values():
            if tup[0] > self.s-1:
                tup[0] = 0

            if tup[1] > self.s-1:
                tup[1] = 0

            neigh_sum += b[tup[0],tup[1]]
        return neigh_sum
    
    def display(self):
        """
        using matplot libs animation functionality, create a graphic to show the board with each advancement of time t
        """

        self.fig = plt.figure() 
        frames = [] #create list of plot objects for each np.array grid that has been created

        # Remove the axes for aesthetics
        plt.axis('off')

        for grid in self.grids: #iterate through all grids created and create matplotlib instance
            frames.append((plt.imshow(grid, cmap='Blues'),))
        
        # Create the animation based on all matplotlib instances
        ani_obj = animation.ArtistAnimation(self.fig, frames, interval=700,repeat_delay=1000, blit=True)

        # write animation to gif
        ani_obj.save(os.getcwd() + '/animation.gif', writer="PillowWriter")

        # display the animation of the progression of the board
        self.fig.show()

    def end_display(self):
        """
        close the active matplotlib figure
        """
        plt.close(self.fig)


# GameObj = GameOfLife(6, .5)
# universe = np.zeros((6, 6))
# beacon = [[1, 1, 0, 0],
#           [1, 1, 0, 0],
#           [0, 0, 1, 1],
#           [0, 0, 1, 1]]
# universe[1:5, 1:5] = beacon
# GameObj.b = universe

# # GameObj.grids[0] = universe

# GameObj.advance(30)
# GameObj.display()
# GameObj.end_display()

# df = pd.DataFrame(columns = list(range(GameObj.s)) + ['step'])


# for i in range(GameObj.steps):
#     temp_df = pd.DataFrame(data=GameObj.grids[i])
#     temp_df['step'] = i
#     df = pd.concat([df,temp_df])



