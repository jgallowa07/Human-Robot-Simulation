#==============================================================
# P4Controller.py
# Version 0.2
# Implementation for Spring 2016 CIS 211 Project 2
# Derived in part from Dave Kieras' design and implementation of EECS 381 Proj 4
# ===============================================================================
'''
This Is a simple simulation that takes advantage of model view controller design
and gives the user (or file) the ability to create a world, humans, robots, fires, and way
points. The Units of time are handled when the user issues a "go" command
The user may move the humans and robots on linear paths by waypoint, fires or x,y
coordinates. robots can attack and extinguish fires in five units of time.
Have fun!
'''
import sys                                                                                                              # for argv
import P4_Model                                                                                                          # import the model file
import P4_View                                                                                                           # import the view file
from P4_Utility import *

# ===============================================================================
def main():                                                                                                             # def main function

    ya_boi = Controller()                                                                                               # instanciate an object of class controller in order to call on it's run method at end of code
    ya_boi.run()                                                                                                        # run dis

# ===============================================================================
class Controller:                                                                                                       # create class controller
    # ===============================================================================
    '''
    The controller object handles user keyboard input and provides textual to
    the console.  It follows the model view-controller software design pattern.
    '''

    # ===========================================================================
    def __init__(self):                                                                                                 # def init method

        self.current_input_mode = 'file'                                                                                # initialze current input mode as a switch
        self.__input_filename = 'commands.txt'                                                                          # initialize current reading of filename
        self.myfile = None                                                                                              # initialize my_file to represent the name
        self.__the_model = P4_Model.Model()                                                                              # instanciate the model object to the private member variable __the_model
        P4_Model.the_model = self.__the_model                                                                            # set the global variable inside of model file to the same model object
        self.__view = P4_View.View()                                                                                     # instanciate the view object to the private member variable __view
        self.__the_model.attach_view(self.__view)                                                                       # call on the models object attach_view() method to attach the view object tot he model

    # ===========================================================================
    def run(self):                                                                                                      # define run method
        # ===========================================================================
        '''
        () -> None.
        Process the command lines for the human-robot simulation.
        '''
        print("Starting Human-Robot Interaction Simulation")                                                           # opening print statement

                                                                                                                        # Attempt to open an input file for an initial set of commands
        self.open_initial_input_file()                                                                                  # calls on open_initial_input_file() basically to check whether or not the arg file is valid and change __input_Filename if it is

        # =======================================================================
        # Command loop
        while True:                                                                                                     # runs an infinite loop

                                                                                                                        # Get the next line of input whether it is from the user or a file.
            try:

                line = self.get_next_input_line()                                                                       # calls get_next_input_line to grab arguments from user/file
                line_list = line.split()                                                                                # splits the input into a parsable list

                if len(line_list) == 0:
                    continue

                else:                                                                                                   # if line list not empty, make the first word the cmd
                    cmd = line_list[0].lower()

                #print(line_list)

                if cmd == 'show':                                                                                       # check to see if user/file would like to show the draw grid
                    self.do_show_command()                                                                              # calls do show command that calls the draw method through the view object

                elif cmd == 'create':                                                                                   # check to see if the use/file wants to create something in/or the world
                    self.__the_model.create_sim_object(line_list[1:])                                                   # calls create sim object to do that

                elif cmd == 'status':                                                                                   # check to see if user/file would like to see the status of the word and its objects.
                    self.__the_model.describe_all()                                                                     # calls discribe_all to do that

                elif cmd == 'open' and len(line_list) == 2:                                                             # Checks to see whether or not you would like to open a certain file
                    self.current_input_mode = 'file'                                                                    # re_assignes the value to file type
                    self.__input_filename = line_list[1]                                                                # re_assignes the vale of current working file to that of the argument
                    self.open_input_file()                                                                              # calls open_input_file to do that

                elif self.__the_model.get_object(cmd):
                    self.do_human_robot_command(line_list)

                elif cmd == 'quit':                                                                            # if user/file wants to quit
                    if self.quit_help():
                        continue

                elif cmd == 'go':
                    self.__the_model.update()

                else:
                    raise BadLineError(' '.join(line_list))

            except BadLineError as error_string:

                print('Unrecognized command:',error_string)
                continue

            except BadMsgError as error_string:

                print('Error:',error_string)
                continue

        return None                                                                                                     # return None

    # ===========================================================================
    # Manage the command line input file
    # ===========================================================================

    def quit_help(self):

        time = self.__the_model.get_time()

        if self.current_input_mode == 'cmd_line_arg':                                                                   # checks to see if its a user
            sure_quit = input('Are you sure you want to quit? (Y/N)')                                                   # sur you wanna quit?

            if sure_quit.upper() == 'Y':                                                                                # yup
                quit()                                                                                                  # QUIT
            else:
                return True                                                                                             # Second guessed thesleves
        else:                                                                                                           # must be a file

            sure_quit = self.myfile.readline()                                                                          # sure you wanna quit?
            print('Are you sure you want to quit? (Y/N) Time',time,'FILE>', sure_quit)                                              # print statement
            sure_quit = sure_quit.upper().strip().split()                                                               # strips the newline charictar and splits it into a list

            if (len(sure_quit) > 0) and (sure_quit[0] == 'Y'):                                                          # yup
                self.myfile.close()                                                                                     # closes the file
                # print('Closing File')
                quit()                                                                                                  # QUIT
            else:
                return True

    def get_next_input_line(self):                                                                                      # define next line method
        '''
        ( ) -> string
        • Displays the prompt.
        • Returns the next line to be processed, or '' if there is no line.
        • Gets the next line of text either from an input file or from the user,
          depending on the current setting of current_input_mode.
        • When reading from an input file, and either a blank line or an end of file
          is encountered, close the input file and set the file object var to None.

        if self.current_input_mode == 'file':
            if self.__input_filename == None
            return the_model.__input_filename.readline().strip()

        else:
            return user_input

        '''
        if self.current_input_mode == 'file':                                                                           # Checks to see if its a file
            if self.myfile == None:                                                                                     # if self.myfile is == None, -> it hasnt been assigned a value yet
                self.open_input_file()                                                                                  # opens file
                if self.current_input_mode == 'cmd_line_arg':                                                           # if its from user
                    return self.get_next_input_line()                                                                   # return the function call again to catch condition

            con = self.myfile.readline().strip('\n')                                                                    # gets content of line
            if con == '':                                                                                               # if there is nothing to read, it's empty
                self.myfile.close()                                                                                     # close file
                print('Closing File.')                                                                                  # print to confirm close
                self.current_input_mode = 'cmd_line_arg'                                                                # re_assign current mode to user
                return self.get_next_input_line()                                                                       # return call on itself
            else:
                print('Time %d FILE> %s' %(self.__the_model.get_time(),con))                                                                                     # prints arg from file to user
                return con                                                                                              # returns the cintent of the file input



        else:                                                                                                           # is it a user
            U_I = input('Time %d >' %(self.__the_model.get_time()))                                                                                            # display command prompt
            return U_I                                                                                                  # retutn the input arg

    # ===========================================================================
    def open_initial_input_file(self):
        '''
        Attempt to open a file for an initial set of commands.
        ( ) -> None
        If a filename was entered as a command line argument, overwrite the
          controller's member variable with that new filename.
        '''

        if len(sys.argv) > 1:                                                                                           # checks for command line arg
            self.__input_filename = sys.argv[1]                                                                         # if so, new fileame is the 1 index md line

        return None                                                                                                     # return none

    # ===========================================================================
    def open_input_file(self):                                                                                          # Define open method
        '''
        ( ) -> None
        Attempts to open the filename in the input file member variable to
          execute a set of commands.
        '''

        try:
            self.myfile = open(self.__input_filename)                                                                   # open it
            print('Reading file:', self.__input_filename)                                                               # print statment

        except (FileNotFoundError, PermissionError):
            print('Error: Could not open and read input file:', self.__input_filename)                                  # could not open file
            self.current_input_mode = 'cmd_line_arg'                                                                    # change inpt mode to user

        return None                                                                                                     # return None

    # ===========================================================================

    def do_human_robot_command(self, args):                                                                             # def human method
        '''
        Parameters: args, a list of arguments that is already confirmed to be
                          nonempty with the first argument a human in the model.
        Returns:    None (All errors are reported within, so no need to return
                          an error flag.)

        Processes the remainder of the arguments to insure that they at least
        represent valid locations on the map.  If they are valid,
        call the appropriate function calls in the model to build them.
        '''
        obj = self.__the_model.get_object(args[0])                                                                      # gets the object

        string = ''                                                                                                     # builds the string to be printed if there is an error
        for i in args:
            string += i + ' '

        if len(args) >= 2:

            cmd = args[1]

            if cmd == 'move':

                obj.journey_to(args[2:])

            elif cmd == 'stop':

                obj._destination_list = []
                obj._moving = False

            elif obj.get_class_name() == 'Robot' and cmd == 'attack' and len(args) == 3 and self.__the_model.get_fire(args[2]):
                fire_obj = self.__the_model.get_fire(args[2])
                robot_name = obj.get_name()
                fire_name = fire_obj.get_name()
                if self.__the_model.get_fire(args[2]).get_location() == obj.get_location():
                    #fire_obj = self.__the_model.get_fire(args[2])
                    location = str(obj.get_location())
                    obj.fight_fire(fire_obj)
                    print('Robot %s at location %s extinguishing fire %s' %(robot_name,location,fire_name))
                else:

                    raise BadMsgError('Robot %s is not in the same location as fire %s' %(robot_name, fire_name))
            else:
                raise BadMsgError('Invalid %s command' %(obj.get_class_name().lower()))
        else:
            raise BadLineError(string)
                                                                                                                        # checks to make sure the arg is valid format

    # ===========================================================================

    def do_show_command(self):                                                                                          # calls on appropriate show command

        self.__view.draw()                                                                                              # ^^^ method draw() through view object


# ===============================================================================
main()  # call main
# ===============================================================================
