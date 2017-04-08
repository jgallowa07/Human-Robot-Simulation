#===============================================================================s
# P3Model.py
# Version 0.1
# Implementation for Spring 2016 CIS 211 Project 2
# Derived in part from Dave Kieras' design and implementation of EECS 381 Proj 4
#===============================================================================
global the_model
from P4_Utility import *

class Model:                                                                                                            #Creating the class Model()
    '''
    The Model object keeps track of everything in the simulated world.
    Only one Model should be created in each run of the simulation.
    '''

    #===========================================================================
    def __init__(self):                                                                                                 #Defining the initialize method

        self.__view = None                                                                                              #Initializing private member variable for the list of human objects
        self._world_size = None
        self.__sim_obj = {'human':[],'robot':[],'fire':[],'waypoint':[]}
        self._time = 0
        self._obj_order = []

    #===========================================================================


    def delete_fire(self, name):

        the_model.notify_location(name, None, 'fire')

        index = 0
        for i in range(len(self.__sim_obj['fire'])):
            if self.__sim_obj['fire'][i].get_name() == name:
                index = i
        del self.__sim_obj['fire'][index]

        for i in self._obj_order:
            if i.get_name() == name:

                self._obj_order.remove(i)

        for i in self.__sim_obj['robot']:
            if i._extinguishing_fire is None:
                continue
            else:
                i._extinguishing_fire = None

        return None

    def __str__(self): #Defining __str__ Method

        return '%s' % (self._world_size)                                                                                #Returing the layout of print format

    #===========================================================================
    def attach_view(self, v):

        self.__view = v                                                                                                  #attches the __view member variable to the view object implemented in the controller
        return None
    #===========================================================================
    def notify_location(self, name, location, type):

        if type.lower() != 'waypoint':
            self.__view.update_object(name, location)
        else:
            self.__view.add_landmark(name,location)
                                                                                                                        #updates the location in the view
        return None

    #===========================================================================
    def get_world_size(self):                                                                                           #defing Method to access the size of the world through through any object in the class Model()
        return self._world_size                                                                                         # return the size of the world

    #===========================================================================
    def get_valid_location(self, arg1, arg2=None):                                                                      #Defineing get_valid_location()) method.
        '''
        Determine if a location is in the world.  If yes, returns a tuple of ints.
        This function is made polymorphic by using "switch on type".

        Parameters: arg1 and arg2 are ints, OR
                    arg1 and arg2 are strings, OR
                    arg1 is a tuple of two ints, and no arg2 is provided, OR
                    arg1 is a tuple of two strings, and no arg2 is provided
        Returns:    a tuple of ints if the location is in the world
                    None otherwise.

        Examples of use if the world is of size 30:
        self.get_valid_location(10, 20) -> (10, 20)
        self.get_valid_location('10', '20') -> (10, 20)
        self.get_valid_location((10, 20)) -> (10, 20)
        self.get_valid_location('a', '20') -> None
        self.get_valid_location(1.0, 20) -> None
        '''

        W_S = self.get_world_size()                                                                                     #Initializing the local variable W_S with value of the world size

        V_L = []                                                                                                        #Initializing an empty list to append the values to and turn to a tuple.

        if arg2 != None:                                                                                                #First if there is a secong argument given.

            if (type(arg1) == int) and (type(arg2) == int):                                                             #If both inputs are both integers They re ready to be compared and appended

                if arg1 <= W_S and arg2 <= W_S:                                                                         #check to make sure both inputs are within the world
                    V_L.append(arg1)                                                                                    #Append arg one
                    V_L.append(arg2)                                                                                    #Append arg two

                    return tuple(V_L)


            elif (type(arg1) != float) and (type(arg2) != float):                                                       #If its not an in or a string it'll be a string

                if arg1.isnumeric() and arg2.isnumeric():                                                               #checks to make sure the value in the string is a valid Location input '(int)'

                    if int(arg1) <= W_S and int(arg2) <= W_S:                                                           #check to make sure both inputs are within the world
                        V_L.append(int(arg1))                                                                           #Append arg one
                        V_L.append(int(arg2))                                                                           #Append arg two

                        return tuple(V_L)                                                                               #return the Value_list as a Tuple to be stored as an attribute to any human object

                else:                                                                                                   #if not valid string return none

                    return None                                                                                         #return none
            else:                                                                                                       #Must be type float,
                return None                                                                                             #return None


        elif arg2 == None:                                                                                              #case if only one parameter is passed

            if (type(arg1[0]) == int) and (type(arg1[1]) == int):                                                       #IF both parameter are ints, ready to be compared and appended

                if arg1[0] <= W_S and arg1[1] <= W_S:                                                                   #checking to make sure the human is within the world
                    V_L.append(arg1[0])                                                                                 #append first element of the only arg1
                    V_L.append(arg1[1])                                                                                 #append second element of the only arg1

                    return tuple(V_L)                                                                                   #retutn the value list as a tuple

            elif (type(arg1[0]) != float) and (type(arg1[1]) != float):                                                 #if not int and not float, then string case

                if arg1[0].isnumeric() and arg1[1].isnumeric():                                                         #checks to make sure th value between quotation in the string is valid input

                    if int(arg1[0]) <= W_S and int(arg1[1]) <= W_S:                                                     #checks the value against the size of the world
                        V_L.append(int(arg1[0]))                                                                        #append first element of the only arg1
                        V_L.append(int(arg1[1]))                                                                        #append second element of the only arg1

                    return tuple(V_L)                                                                                   #retunrs the value list as a tuple

                else:                                                                                                   #if not valid value between the string then return none

                    return None                                                                                         # return None
            else:                                                                                                       #if it's a float

                return None                                                                                             #return None
    #===========================================================================



    #===========================================================================
    def create_sim_object(self, arg_list):
        '''
        Create a simulation object based on the contents of the arg_list.
        Parameters: arg_list, list of strings entered after "create" command
        Returns:    True for if the line cannot be parsed, False if it can be.

        The only assumption that can be made about the arg_list when entering
        this function is that there was at least one string in the command line
        after "create".
        '''

        MIN_WORLD_SIZE = 5 #Initialize local variable minimum size for the world
        MAX_WORLD_SIZE = 30 #Initialize local variable maximum size for the world
        sim_list = ['human','robot','fire']#,'waypoint']


        if len(arg_list) > 1:
            object_type = arg_list[0].lower()
        else:
            raise BadLineError('create '+' '.join(arg_list))

        if object_type == 'world':                                                                                      #first condition to see if the user/file would loke to create a world

            if self._world_size == None:                                                                                #check to see if a world has already been created
                #print(type(arg_list[1]))
                if (len(arg_list) == 2) and arg_list[1].isnumeric():                                                    #check to see if the argument list is in correct length format

                    if int(arg_list[1]) >= MIN_WORLD_SIZE and int(arg_list[1]) <= MAX_WORLD_SIZE:                       #checks to see that the values are within world
                        self._world_size = int(arg_list[1])                                                             #re-assignes the value form none -> Arg_list[1]
                        self.__view.create(self._world_size)
                        print('Creating world of size %s' %(self._world_size))                                         #Print statement for creating a world
                        return False                                                                                    #returning false because line could be parsed
                    else:                                                                                               #else
                        raise BadMsgError('World size is out of range')
                else:
                    raise BadLineError('create ' + ' '.join(arg_list))
            else:                                                                                                       #else
                raise BadMsgError('World already Exists')                                                               #return tru to verify failure

        elif object_type == 'waypoint' and len(arg_list) == 4:
            if self._world_size != None:                                                                                # checks to make sure that a world has been created first
                name = arg_list[1]                                                                                      # initalizes the local variable name to the third elemt of the line input
                name = name.capitalize()
                x = arg_list[2]  # set location arg 1
                y = arg_list[3]  # set locationg arg 2
                location = self.get_valid_location(x, y)

                if len(name) == 1 and name.isalpha():
                    if location != None:

                        for i in self.__sim_obj['waypoint']:
                            #locat_p = str(self.get_waypoint_location(name))
                            if i.get_name() == name:
                                locat_p = str(self.get_waypoint_location(name))
                                raise BadMsgError('Waypoint %s already exists at location %s' % (name, locat_p))
                            elif i.get_location() == location:
                                ob_name = i.get_name()
                                locat_p = i.get_location()
                                raise BadMsgError('Waypoint %s already exists at location %s' % (ob_name, locat_p))
                            else:
                                continue

                        # if self.get_waypoint_location(name):
                        #     locat_p = str(self.get_waypoint_location(name))
                        #     raise BadMsgError('Waypoint %s already exists at location %s' % (name, locat_p))

                        new_obj = Waypoint(name, location)

                        self.__sim_obj[object_type].append(new_obj)  # appends that human to a list
                        self.notify_location(name.capitalize(), location, object_type)
                        self._obj_order.append(new_obj)
                        print('Creating %s %s at location %s' % (object_type, name, location))


        elif object_type in sim_list and len(arg_list) == 4:                                                                                  #check to see if user wants to create a human
            if self._world_size != None:                                                                                #checks to make sure that a world has been created first
                name = arg_list[1]                                                                                      #initalizes the local variable name to the third elemt of the line input
                name = name.capitalize()

                if self.get_object(name) != None:
                    obj = self.get_object(name)
                    typ = obj.get_class_name()
                    raise BadMsgError('%s already exists with that name' % (typ))

                #if len(arg_list) == 3 or 4:                                                                             #checks to see whether the argument should pas four arguments off to get_valid_location
                # if len(arg_list) == 3:
                #     location = self.get_valid_location(arg_list[2])                                                     # initializes location of given argument
                else:
                    x = arg_list[2]                                                                                     #set location arg 1
                    y = arg_list[3]                                                                                     #set locationg arg 2
                    location = self.get_valid_location(x,y)                                                             #creates the tuple, valid location

                if name.isalnum():                                                                                      #checks to see whethe given name is alphanumeric
                    if location != None:                                                                                #checks to see if location was valid
                        if object_type == 'human':
                            new_obj = Human(name,location)                                                              #instanciates a new human object
                        elif object_type == 'robot':
                            new_obj = Robot(name, location)
                        # elif object_type == 'fire':
                        else:
                            new_obj = Fire(name, location)
                        # else:
                        #
                        #     for i in self.__sim_obj['waypoint']:
                        #         if i.get_location() == location:
                        #             raise BadMsgError('Waypoint already exists in that location')
                        #
                        #     if len(name) > 1:
                        #         raise BadMsgError('Waypoint name must be one letter')
                        #
                        #     new_obj = Waypoint(name, location)

                        self.__sim_obj[object_type].append(new_obj)                                                     #appends that human to a list
                        self.notify_location(name.capitalize(), location, object_type)
                        self._obj_order.append(new_obj)
                        print('Creating %s %s at location %s' %(object_type,name,location))                            #print statement for creating a human

                        return False                                                                                    #retunrn false as a green flag
                    else:
                        raise BadMsgError("Invalid location")                                                          #else                                                                                 #retunr true as red flag
                else:
                    raise BadMsgError('Name must be alphanumeric')                                                     #else
            else:
                raise BadMsgError('A world must be created before any other objects')                                                      #else
        else:
            raise BadLineError('create'+' '+' '.join(arg_list))



    #===========================================================================


    def get_object(self, name):                                                                                         # define get_human
        '''
        # Takes a name string.  Looks for a human with that name.  If one exists,
        #   returns that human.  If one does not, returns None.

        Parameters: name, a string
        Returns:    Either a pointer to a human object, or None

        '''
        for obj in self.__sim_obj['human']:
            if obj.get_name() == name.capitalize():  # if a human matches a name then,
                return obj

        for obj in self.__sim_obj['robot']:
            if obj.get_name() == name.capitalize():  # if a human matches a name then,
                return obj

        return None                                                                                                     # return none


    def get_waypoint_location(self,name):
        for obj in self.__sim_obj['waypoint']:
            if obj.get_name() == name.capitalize():  # if a human matches a name then,
                location = obj.get_location()
                return location
        return None

    def get_human(self,name):                                                                                           #looks for human object with the name
        for obj in self.__sim_obj['human']:
            if obj.get_name() == name.capitalize():  # if a human matches a name then,
                return obj                                                                                              #returns it
        return None

    def get_robot(self,name):                                                                                           #looks for a robot with that name
        for obj in self.__sim_obj['robot']:
            if obj.get_name() == name.capitalize():  # if a human matches a name then,
                return obj #returns it
        return None

    def get_fire(self,name):
        for obj in self.__sim_obj['fire']:
            if obj.get_name() == name.capitalize():  # if a human matches a name then,
                return obj
        return None

    #===========================================================================
    def describe_all(self):                                                                                             #define describe function
        '''
        Each of the simulation objects describes itself in text.
        ( ) -> None
        '''

        print('The contents of the world are as follows:')                                                              #opening print statement
        if self._world_size != None:                                                                                    #checks to see if there is a world to print
            print('The world is of size %s' %(self._world_size))                                                       #if so, print world size

            for obj in self.__sim_obj['waypoint']:                                                                      #runs through each obj in dictionay and prints them in order
                    print(obj.__str__())

            for obj in self.__sim_obj['human']:
                    print(obj.__str__())

            for obj in self.__sim_obj['robot']:
                    print(obj.__str__())

            for obj in self.__sim_obj['fire']:
                    print(obj.__str__())

        return None            #return none

    # ===========================================================================

    def get_time(self):

        return self._time

    # ===========================================================================

    def update(self):

        self._time += 1

        for i in self._obj_order:
            if (i.get_class_name() == 'Human') or (i.get_class_name() == 'Robot') or (i.get_class_name() == 'Fire'):
                i.update()

    # ===========================================================================

    def fire_at_location(self,location):

        for obj in self.__sim_obj['fire']:  # runs through dict
            if obj.get_location() == location:  # if the value == the location tuple given
                return obj

        return None

    # ===========================================================================


#===============================================================================
class SimObject:                                                                                                        #create class SimObject
    '''
    A human in the simulation.
    '''

    def __init__(self, name, location):                                                                                 #initilize private member variables
        self._name = name                                                                                               #initialize name
        self._location = location                                                                                       #initialize location

    def __str__(self):                                                                                                  #def method for string
        return '%s at location %s' %(self._name,self._location)                                                         #return print format

    def get_name(self):                                                                                                 #def Get_name method
        return self._name                                                                                               #retun the objects name

    def get_class_name(self):                                                                                           #retunrn the class of a sim_object
        str_class = str(type(self))
        index = str_class.find('.')
        class_name = str_class[index + 1:-2]
        return class_name

    def get_location(self):                                                                                             #get location method
        return self._location                                                                                           #return the location of the Sim object


#===============================================================================
class Traveler(SimObject):                                                                                              #create travelor class that inherits from simObject

    def __init__(self, name, location):
        super().__init__(name,location)
        #SimObject.__init__(self,name,location)
        self._destination_list = []
        self._moving = bool

    # ===============================================================================

    def journey_to(self,destination_list):

        pre = None
        # self._destination_list = []
        valid_destination = []
        for i in range(len(destination_list)):

            if i == 0:
                pre = self.get_location()

            loc = destination_list[i]
            loc = loc.split(',')

            # p_loc = ''
            # for e in loc:
            #     p_loc += e +','

            if (len(loc) == 1) or (len(loc) == 2):
                if the_model.get_waypoint_location(loc[0]):
                    location = the_model.get_waypoint_location(loc[0])
                elif (len(loc) == 2):
                    if the_model.get_valid_location(loc[0], loc[1]):
                        location = the_model.get_valid_location(loc[0], loc[1])
                    else:
                        # print(destination_list[i])
                        raise BadMsgError("'%s' is not a valid location for this 'move'" %(destination_list[i]))
                else:
                    raise BadMsgError("'%s' is not a valid location for this 'move'" %(destination_list[i]))
            else:
                raise BadMsgError("'%s' is not a valid location for this 'move'" %(destination_list[i]))

            if (pre[0] == location[0]) or (pre[1] == location[1]):
                        valid_destination.append(location)
                        # self._destination_list.append(location)
                        self._moving = True
                        pre = location

                        if self.get_class_name() == 'Robot':
                            self._extinguishing_fire = None

            else:
                raise BadMsgError("'%s' is not a valid location for this 'move'" %(destination_list[i]))

        if len(valid_destination) > 0:
            self._destination_list = []

            for i in valid_destination:
                self._destination_list.append(i)

        des_string = ''
        for i in range(len(self._destination_list)):
            if i != (len(self._destination_list)-1):
                des_string += str(self._destination_list[i]) + ','+' '
            else:
                des_string += str(self._destination_list[i]) + ' '

        print('%s %s at location '%(self.get_class_name(),self.get_name())+str(self.get_location())+' moving to '+des_string)

    # ===============================================================================

    def get_next_moving_location(self):

        next_dest = self._destination_list[0]
        curr_loc = self.get_location()

        next_x = next_dest[0]
        next_y = next_dest[1]

        curr_x = curr_loc[0]
        curr_y = curr_loc[1]

        next_loc_li = []

        if next_x == curr_x:
            if curr_y < next_y:
                next_loc_li.append(curr_x)
                next_loc_li.append(curr_y + 1)
            else:
                next_loc_li.append(curr_x)
                next_loc_li.append(curr_y - 1)

        else:
            if curr_x < next_x:
                next_loc_li.append(curr_x + 1)
                next_loc_li.append(curr_y)
            else:
                next_loc_li.append(curr_x - 1)
                next_loc_li.append(curr_y)

        return tuple(next_loc_li)

    # ===============================================================================


    def move_to(self, location):                                                                                        #def move_to method
        next_dest = self._destination_list[0]

        if location == next_dest:
            self._destination_list.pop(0)

        name = self.get_name()                                                                                          #gets nam of object to pass to notify_location()
        type = self.get_class_name()
        self._location = location                                                                                       #Re-assign the vale to location as command intended
        the_model.notify_location(name,location,type)                                                                   #calls the notify_location method through the model object to notify the view
        if len(self._destination_list) == 0:
            self._moving = False
            print('%s %s arrived at location %s' %(type,name,location))
        # else:
        #     print('%s %s moved to location %s.' %(type,name,location))                                                      #print statement for when the object has moved locaitons



#===============================================================================
class Human(Traveler):                                                                                                  #create class human which inherits from the traveler class

    # def __str__(self):                                                                                                  #extend the __str__ method
    #     return 'Human ' + super().__str__()
    def __str__(self):
        if len(self._destination_list) > 0:
            # print(self._destination_list)
            des_string = ''
            for i in self._destination_list:
                des_string += str(i) + ' '  # extend the __str__ method
            return 'Human ' + super().__str__() + ' moving to' + ' ' + des_string
        else:
            return 'Human ' + super().__str__()

        # ===============================================================================

    def update(self):
        if len(self._destination_list) > 0:
            next_loc = self.get_next_moving_location()
            poss_fire = the_model.fire_at_location(next_loc)

            if poss_fire != None:

                self._moving = False
                self._destination_list = []
                print('Human %s stopping short of fire %s' %(self.get_name(),poss_fire.get_name()))

            else:

                self._moving = True
                self.move_to(next_loc)

        return None

    # ===============================================================================


# ===============================================================================
class Robot(Traveler):                                          #create the robot class inheriting from travelor

    def __init__(self, name, location):
        super().__init__(name, location)
        # SimObject.__init__(self,name,location)
        self._extinguishing_fire = None

    def __str__(self):
        # return 'Robot ' + super().__str__()             #extend the __str__ method
        if len(self._destination_list) > 0:
            # print(self._destination_list)
            des_string = ''
            for i in self._destination_list:
                des_string += str(i) + ' '  # extend the __str__ method
            return 'Robot ' + super().__str__() + ' moving to' + ' ' + des_string
        elif self._extinguishing_fire:
            fire_name = self._extinguishing_fire.get_name()

            return 'Robot ' + super().__str__() + ' extinguishing fire '+fire_name

        else:
            return 'Robot ' + super().__str__()

    def fight_fire(self,fire_obj):

        self._extinguishing_fire = fire_obj
        self._destination_list = []
        self._moving = False

    def update(self):
        if len(self._destination_list) > 0:
            next_loc = self.get_next_moving_location()
            self.move_to(next_loc)
            self._moving = True

        elif self._extinguishing_fire:
            self._extinguishing_fire.reduce_strength()
            if self._extinguishing_fire:
                if self._extinguishing_fire._strength == 0:
                    del self._extinguishing_fire
                    self._extinguishing_fire = None

        else:
            return None

#===============================================================================

class Waypoint(SimObject):                                                                                              #create the waypont class inheriting from the simobject class

    def __str__(self):
        return 'Waypoint ' + super().__str__()                                                                          #extend the __str__ method

# ===============================================================================

class Fire(SimObject):                                                                                                  #create fire class inheriting from the  simobject class

    def __str__(self):
        return 'Fire ' + super().__str__()  +' of strength ' + str(self._strength)                                                                            #extend the __str__ method

    def __init__(self, name, location):
        super().__init__(name, location)
        # SimObject.__init__(self,name,location)
        self._strength = 5

    def __del__(self):

        print('Fire %s has disappeared from the simulation' % (self.get_name()))


    def get_strength(self):

        return self._strength


    def reduce_strength(self):

        self._strength -= 1
        if self._strength == 0:
            name = self.get_name()

            the_model.delete_fire(name)


    def update(self):

        pass
