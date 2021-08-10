"""
DSC 430
Adam Klaus
February 22nd, 2021
Video Link: https://www.youtube.com/watch?v=j0-1-oBwGf0
"I have not given or received any unauthorized assistance on this assignment"
"""

import math
import pandas as pd
import os
try:
    FILE_DIR = os.path.abspath(os.path.dirname(__file__))
except:
    FILE_DIR = os.path.join(os.getcwd(),'application','projects')


class WarAndPeacePseudoRandomNumberGenerator:
    """
    Using a text file of War and Peace, create a list of random numbers

    Attributes
    ----------
    seed : int
        seed of where to start in the text file
    position : int
        current location of the cursor in the text file
    step_value: int
        number of characters between each character
    total_chars: int
        number of characters in the text file
    bits_list: list
        values from .5,.25,..etc
    """

    def __init__(self, seed):
        """
        construct the class with these initial attributes
        """
        self.seed = seed
        self.read_file()
        self.position = self.seed
        self.bits_list = self.get_bits_list()
        self.step_value = 50
        self.total_chars = self.get_total_chars()

    def read_file(self):
        """
        read in text file

        Attributes
        ----------
        infile : file
            text file object
        """
        infile = open(os.path.join(FILE_DIR,'war-and-peace.txt'), 'r')
        infile.seek(self.seed)
        self.infile = infile

    def get_random_char(self):
        """
        generate a random character from the text file, if character can't be encoded, pick another one
        update position after character is selected
        """
        try:    #handles encoding error
            char = self.infile.read(1)
        except:
            self.reset_cursor() # determines if the file should be start over again
            char = self.infile.read(1)
        
        self.position += self.step_value #update position of cursor
        self.infile.seek(self.position)
        return char

    def get_bits_list(self):
        """
        create bits list to assist in determining random numbers
        """
        bits_list = []
        start = .5
        for i in range(1,33):
            bits_list.append(start)
            start = start/2

        return bits_list

    def get_pair_list(self):
        """
        get a pair of two random characters and compare them
        append the 0, 1 value to the pair_list
        Attributes
        ----------
        pair_list : list
            list of 0 or 1 depending on whether one character was "greater" than another

        """
        pair_list = []
        for i in range(1,33):
            pair_value = 0
            char_1 = self.get_random_char()
            char_2 = self.get_random_char()

            while char_1 == char_2: #keep selecting a new first char if chars are the same
                char_1 = self.get_random_char()

            if char_1 > char_2:
                pair_value = 1
            
            pair_list.append(pair_value)
        
        self.pair_list = pair_list

    def sum_product_pairs_bits_list(self):
        """
        Determine the sum product between the list of random 0,1s and bits to get a random number

        Attributes
        ----------
        random_number : int
            random number generates from the pair_list and bits_list
        """
    
        self.random_number =  0 #reset random number
        for i in range(0,32):
            self.random_number += self.pair_list[i] * self.bits_list[i]

    def generate_random_number(self):
        """
        sequence the methods necessaary to create a random number

        :return: a random number
        """
    
        if self.position > self.total_chars or abs(self.position - self.total_chars) < 10000: # if file is getting close the end start it over 
            self.reset_cursor()
        self.get_pair_list()
        self.sum_product_pairs_bits_list()
        return self.random_number

    def reset_cursor(self):
        """
        Move the cursor to the beginning of the text file
        """
        self.infile.seek(self.seed)
        self.position = 1
        self.step_value += 1 #increment the step size each time the file repeats, so the random list does not repeat

    def get_total_chars(self):
        """
        Determine the total number of characters in the text file

        :return: total number of characters in the text file
        """
        count = 0
        for line in self.infile.readlines():
            count += len(line)
        return count
    
    def get_list_of_random_numbers(self, n):
        """
        create a list of random numbers n long

        :return: list of random numbers 
        """
        rn_list = []
        for i in range(0,n):
            rn_list.append(self.generate_random_number())
        
        self.rn_list = rn_list
    
    def get_metrics_random_numbers_list(self):
        """
        generate necessary metrics to show class is working properly 
        """
        print('Max :' + str(max(self.rn_list)))
        print('Min :' + str(min(self.rn_list)))
        print('Mean :' + str(sum(self.rn_list)/len(self.rn_list)))



class Point:
    """
    Create a an object with 2d coordinates

    Attributes
    ----------
    x : int
        x coordinate for a point
    y : int
        y coordinate for a point
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y 


#add a method to this class of whether the point is in the ellipse
class Ellipse:
    """
    create an ellipse object with two focal points and a width

    Attributes
    ----------
    p1 : point object
        first focal point of ellipse
    p2 : point object
        second focal point of ellipse
    w : int
        width of ellipse
    """
    def __init__(self, p1, p2, width):
        """
        construct the class with these initial attributes
        """
        self.p1 = p1
        self.p2 = p2
        self.width = width

    def point_in_ellipse(self, input_x, input_y):
        """
        determine a point falls in the ellipse

        Parameters
        ----------
        input_x : int
            x_value from a point

        input_y : int
            y_value from a point

        :return boolean: whether or not a given point is in an ellipse
        """

        in_ellipse = False
        a = math.sqrt((input_x-self.p1.x)**2 + (input_y-self.p1.y)**2)     #find distance from each focal point
        b = math.sqrt((input_x-self.p2.x)**2 + (input_y-self.p2.y)**2)
        if a + b <= self.width: #defines whether or not a point is within an ellipse
            in_ellipse = True
        return in_ellipse
    
    # def check_if_ellipse(self):
    #     (w + x1) + (w - x2) = 2*w


class OverlapOfEllipses:
    """
    Determine if two ellipses overlap one another using random numbers

    Attributes
    ----------
    overlap_points : int
        number of points in both ellipses
    seed : int
        determines the position where the cursor should start reading in characters from the text file
    iters: int 
        number of random numbers to generate
    prngObj : object
        instance of pseudo random number generator from war and peace
    """

    def __init__(self, seed = 50, iters = 10000):
        """
        construct the class with these initial attributes
        """
        self.overlap_points = 0
        self.seed = seed
        self.iters = iters
        self.prngObj = WarAndPeacePseudoRandomNumberGenerator(self.seed)

    def make_box(self):
        """
        sequence methods to determine the size of box that both ellipses fit in
        """
        self.get_max_values()
        self.get_box_points()
        self.get_box_area()
    
    def get_max_values(self):
        """
        get max values from each ellipse and there points
 
        Attributes
        ----------
        x_min : int
            minimum x value of either focal point in both ellipses
        x_max : int
            maximum x value of either focal point in both ellipses
        y_min : int
            minimum y value of either focal point in both ellipses
        y_max : int
            maximum y value of either focal point in both ellipses
        w : int
            max width from ellipses
        """

        self.x_min = min(self.e1.p1.x, self.e1.p2.x, self.e2.p1.x, self.e2.p2.x)
        self.x_max = max(self.e1.p1.x, self.e1.p2.x, self.e2.p1.x, self.e2.p2.x)
        self.y_min = min(self.e1.p1.y, self.e1.p2.y, self.e2.p1.y, self.e2.p2.y)
        self.y_max = max(self.e1.p1.y, self.e1.p2.y, self.e2.p1.y, self.e2.p2.y)

        self.w = max(self.e1.width, self.e2.width)

    def get_box_points(self):
        """
        get coordinates of the box containing the ellipses
 
        Attributes
        ----------
        bottom_left_x : int
            x value for bottom left coordinate of box
        bottom_left_y : int
            y value for bottom left coordinate of box
        bottom_right_x : int
            x value for bottom right coordinate of box
        bottom_right_y : int
            y value for bottom right coordinate of box
        top_left_x : int
            x value for top left coordinate of box
        top_left_y : int
            y value for top left coordinate of box
        top_right_x : int
            x value for top left coordinate of box
        top_right_y : int
            y value for top left coordinate of box
        """

        self.bottom_left_x = self.x_min - self.w
        self.bottom_left_y = self.y_min - self.w
        self.bottom_right_x = self.x_max + self.w
        self.bottom_right_y = self.bottom_left_y
        self.top_left_x = self.bottom_left_x
        self.top_left_y = self.y_max + self.w
        self.top_right_x = self.bottom_right_x
        self.top_right_y = self.top_left_y


    def get_box_area(self):
        """
        get the area of the box containing the ellipses
 
        Attributes
        ----------
        box_length : int
            length of box
        box_height : int
            height of box
        box_area : int
            area of box
        """

        self.box_length = abs(self.bottom_left_x) + abs(self.bottom_right_x) 
        self.box_height = abs(self.top_left_y) + abs(self.bottom_left_y)
        self.box_area = self.box_length * self.box_height

    def scale_random_numbers(self, x_input, y_input):
        """
        scale two random numbers between 0 and 1 to be coordinates in the box containing the ellipses
 
        Parameters
        ----------
        input_x : int
            random number between 0 and 1 representing an x value for a point
        input_y : int
            random number between 0 and 1 representing an y value for a point
        """
        x = x_input*self.box_length + self.bottom_left_x
        y = y_input*self.box_height + self.bottom_left_y
        return x, y

    def point_in_both_ellipses(self, x_input, y_input):
        """
        determine if random point is in an ellipse

        Parameters
        ----------
        input_x : int
            random number between 0 and 1 representing an x value for a point
        input_y : int
            random number between 0 and 1 representing an y value for a point
        """

        in_e1 = self.e1.point_in_ellipse(x_input,y_input)
        in_e2 = self.e2.point_in_ellipse(x_input,y_input)

        if in_e1 and in_e2:
            self.overlap_points += 1
            self.points_df.loc[self.i,'overlap'] = 'Both'
        elif in_e1:
            self.points_df.loc[self.i,'overlap'] = 'Ellipse 1'
        elif in_e2:
            self.points_df.loc[self.i,'overlap'] = 'Ellipse 2'
        else:
            self.points_df.loc[self.i,'overlap'] = 'Neither'

    def get_prng_list(self, iters=10000):
        """
        generate a list of random numbers using the prngObj that is iters number long

        Parameters
        ----------
        iters : int
            length of the random number list

        Attributes
        ----------
        iters : int
            length of the random number list        
        """

        self.prngObj.get_list_of_random_numbers(self.iters)
        # self.prngObj.get_metrics_random_numbers_list() #shows metrics of rn_list
        self.rn_list = self.prngObj.rn_list

    def place_random_numbers_in_box(self):
        """
        create points from random numbers list, scale them to fit in box and see if they land if both ellipses
        """
        self.points_df = pd.DataFrame(columns = ['x','y'])

        for i in range(0,self.iters,2):
            self.i = i
            x = round(self.rn_list[i],3)
            y = round(self.rn_list[i+1],3)

            input_points = self.scale_random_numbers(x, y)
            self.points_df.loc[i,'x'] = x
            self.points_df.loc[i,'y'] = y


            self.point_in_both_ellipses(input_points[0], input_points[1])

    def computeOverlapOfEllipses(self, e1, e2):
        """
        determine the area where two ellipses overlap by sequencing necessary methods

        Parameters / Attributes
        ----------
        e1 : object
            ellipse object with focal points and width
        e2 : object
            ellipse object with focal points and width
        perc_points_box : float
            percent of points in both ellipses
        overlap_area : float
            area of overlapping ellipses        
        """

        self.e1 = e1
        self.e2 = e2
        self.make_box()
        self.get_prng_list()
        self.place_random_numbers_in_box()
        self.perc_points_box = (self.overlap_points/(self.iters/2)) #take half iters because it takes two random numbers to create 1 point
        self.overlap_area = round(self.perc_points_box*self.box_area, 2)
        print('Area of overlapping ellipses: ' + str(self.overlap_area))


#Example 1

# p1 = Point(0,0)
# p2 = Point(0,0)
# p3 = Point(0,0)
# p4 = Point(0,0)
# e1 = Ellipse(p1,p2, 2)
# e2 = Ellipse(p3,p4, 2)

# obj = OverlapOfEllipses(seed = 20, iters = 3500)
# obj.computeOverlapOfEllipses(e1,e2)
# obj.points_df

# #Example 2

# p1 = Point(9,5)
# p2 = Point(4,1)
# e1 = Ellipse(p1, p2, 9)
# p3 = Point(2,6)
# p4 = Point(6,3)
# e2 = Ellipse(p3, p4, 8)

# obj = OverlapOfEllipses(seed = 1000, iters = 2000)
# obj.computeOverlapOfEllipses(e1,e2)


