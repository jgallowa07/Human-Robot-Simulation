#===============================================================================
# P3View.py
# Version 0.2
# Implementation for Spring 2016 CIS 211 Project 2
# Derived in part from Dave Kieras' design and implementation of EECS 381 Proj 4
#===============================================================================
from P4_Utility import *


class View:                                                                                                             #create class view
    # ===============================================================================
    def __init__(self):                                                                                                 #initialize member variables
        self.sim_obj_dic = {}                                                                                           #initializes the sim obj dict that consists of names as keys and locations as values
        self.sim_obj_dic_ji = {}                                                                                        #initializes the dictionary similar to sim obj dic but consists of location in terms of i and j
        self.waypoint_dic = {}
        self.waypoint_dic_ji = {}                                                                                         #initializes the way point dic
        self.__world_size = None                                                                                        #initializes world size
        self.li = None                                                                                                  #initializes the empty list to be turned into the list of lists for the coordinates of grid

    # ===============================================================================

    def create(self,world_size):                                                                                        #method create for setting up the list of lists and setting the member variable world size

        self.li = []                                                                                                    #re-assignes the value to an empty list so a previous list doesnt interfere

        self.__world_size = world_size                                                                                  #ses the world size

        for i in range(self.__world_size + 1):
            self.li.append([])                                                                                          #builds the list of lists

    # ===============================================================================

    def build_loc_dict(self):                                                                                           #helper funtion to build diction locations values in terms of j and i
        """buids a dictionary similar to Sim_obj_dic, but the location values are in terms of (i,j) rather than (x,y)"""

        for i in self.sim_obj_dic:                                                                                      #runs through sim_obj dic
            value_xy = self.sim_obj_dic[i]                                                                              #takes the value
            self.sim_obj_dic_ji[i] = ((5 + (4 * value_xy[0])), (self.__world_size - value_xy[1]))                       #sets value to conversion j = 5 + 4x, i = world_size - y
        for i in self.waypoint_dic:
            value_xy = self.waypoint_dic[i]
            self.waypoint_dic_ji[i] = ((4 + (4 * value_xy[0])), (self.__world_size - value_xy[1]))
        return None                                                                                                     #return none

    def find_keys(self,loc_tup):                                                                                        #runs through the ji dict to find all associated keys.
        keys = []                                                                                                       #initializes empty list for which to put the keys
        for i in self.sim_obj_dic_ji:                                                                                   #runs through dict
            if self.sim_obj_dic_ji[i] == loc_tup:                                                                       #if the value == the location tuple given
                keys.append(i)
        for i in self.waypoint_dic_ji:  # runs through dict
            if self.waypoint_dic_ji[i] == loc_tup:  # if the value == the location tuple given
                keys.append(i)
                                                                                                                            #append that key, i, to the list of keys
        return keys                                                                                                     #return the list to be analyzed by draw()

    # ===============================================================================

    def update_object(self,name,location):                                                                              #def update object that is called on by the model

        indicator = 0                                                                                                   #initialized an ind  var to see if there was a match for name given
        self.build_loc_dict()
        for i in self.sim_obj_dic:                                                                                      #runs through sim_obj_dic to see if it can find a match
            if i == name:
                if location is None:
                    del self.sim_obj_dic[i]
                    del self.sim_obj_dic_ji[i]
                    indicator += 1
                    return None
                else:
                    self.sim_obj_dic[i] = location                                                                          #update the location                                                                                         #flag ind var
                    indicator += 1
                    return None


        if indicator == 0:                                                                                          #if no match was found
            self.sim_obj_dic[name] = location                                                                           #put new object in the list
            return None
        #self.build_loc_dict()
    # ===============================================================================

    def add_landmark(self,name,location):

        self.waypoint_dic[name] = location

    # ===============================================================================

    def draw(self):
        '''
        () -> None

        This funtion draws the world through a process of building long a list of list where the inside lists are the
        rows and everything appended to them is the coloumn, I figured I figured I could convert the grid we see into
        the grid represented by every unit. The (x,y) grid is converted into a (j,i) grid whitch represents the location
        of the iteration of the two nested for loops.
        '''

        if self.__world_size == None:                                                                                   #if a world hasnt been created
            raise BadMsgError('No World to Show')                                                                       #nothing to print
        self.create(self.__world_size)                                                                                  #calls on create to re assign the self.li and rebuild it based on the size

        self.build_loc_dict()                                                                                           #calls helper funtion to build the dic in terms of j,i

        for i in range(len(self.li)):                                                                                   #first for loop represents which row ... or y value
            line_num = str(self.__world_size - i)                                                                       #line_number is backwards from the size of the world

            for j in range((4 * self.__world_size) + 6):                                                                #second for loop represents which row your on

                ji_li = [j, i]                                                                                          # gives current iteration // location in unit grid

                curr_ji_loc = tuple(ji_li)                                                                              #turns it into a tuple to be compared to ji dict

                if (j % 4 == 0) or ((j - 1) % 4 == 0):                                                                  #the only unit rows that will be printed with period or object name letter
                    if (j == 0) or (j == 1):                                                                            #if its the first two columns, you must print a axis label every 5
                        if (self.__world_size-i) % 5 == 0:                                                              #if the line_num is evenly divisable by zero,
                            ddln = line_num.zfill(2)                                                                    #z fill to create leading zeros on singe integers
                            if j == 0:                                                                                  #if its the zeroith unit column, print the first of two digits in the line number
                                self.li[i].append(ddln[0])                                                              #append that single int to the li to be printed
                            elif j == 1:                                                                                #if its the 1th unit column, print the second of the two digits in line number
                                self.li[i].append(ddln[1])                                                              #append that ingle in to the li to be printed
                        else:                                                                                           #if the row is not in mod 5,
                            self.li[i].append(' ')                                                                      #append a space to be printed
                    else:                                                                                               #if its not the zeroith or 1th column...
                        if curr_ji_loc in self.sim_obj_dic_ji.values() or curr_ji_loc in self.waypoint_dic_ji.values():                                                 #check to see whether the iteration (j,i) is in the sim_obj_dic_ji

                            keys = self.find_keys(curr_ji_loc)                                                          #if so, call on find_keys() to find all the objects associated with that value
                            if len(keys) == 1:                                                                          #if there is only one name to that unit location,
                                self.li[i].append(keys[0][0])                                                           #append the first letter to be printed
                            else:                                                                                       #if there is more than one nme to that same location...
                                self.li[i].append('*')                                                                  #append and asterisk to be printed

                        elif j % 4 == 0:                                                                                #but if there is no location that matches the iteration then just print a period
                            self.li[i].append('.')                                                                      #append period

                        else:                                                                                           #if its not the right column, mod 4, and it has no match of object/waypoint...
                            self.li[i].append(' ')                                                                      #append a space cause theres nothing to see
                else:                                                                                                   #if its not in of of the mod4 columns, nothing will be printed
                    self.li[i].append(' ')                                                                              #append a space

        for row in self.li:                                                                                             #this for loop is to run throught the list and print the built string
            string_print = ''                                                                                           #initialize an empty string to be build from the elements in the list of lists
            for element in row:                                                                                         #runs through each element in the list
                string_print += element                                                                                 #and appends that element to be printed in order.

            print(string_print)                                                                                         #print the row
        last = ''                                                                                                       #initialize an empty string to build last row
        first_digit = 0
        second_digit = 0

        for j in range((4 * self.__world_size) + 6):                                                                    #runs as far as the last column through the conversion form unit to x,y
            if j != 0 and (j % 4 == 0 or (j - 1) % 4 == 0):                                                             #only place to print is mod4 except the first two
                column_num = (j // 4) - 1                                                                               #rebuilds the column num in terms of xy
                if column_num % 5 == 0:                                                                                 #if the column if divisible by 5...
                    dddln = str(column_num).zfill(2)                                                                    #make the integer two digits long with leading zeros
                    first_digit = dddln[0]                                                                              #initialize first digit to beprinted first
                    second_digit = dddln[1]                                                                             #initialize second digit to be printed next
                    if j % 4 == 0:                                                                                      #if its mod4 then print first digit
                        last += first_digit                                                                             #by adding it to the string to be printed
                    elif (j - 1) % 4 == 0:                                                                              #if j-1 is mod four then..
                        last += second_digit                                                                            #it is the correct unit colum to print the second digit
                else:                                                                                                   #if the x column is not mod 5 then dont print it
                    last += ' '                                                                                         #by adding a space
            else:                                                                                                       #if its not in appropriate unit column,
                last += ' '                                                                                             #Conctinate an empty string
        print(last)                                                                                                     #print the last row from the string we just built

        return None     
