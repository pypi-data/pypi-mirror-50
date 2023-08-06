name = "Atria"
import sys, os
from Atria import brain
from Atria import database
from Atria.brain import Brain
from Atria.database import DataBase

class Main(Brain):
    def __init__(self):
        pass

    def main(self, argv):
        #Initialize an instance of Atria's brain
        atria = Brain()
        #Respond to the user's input
        try:
            if(__name__ == "__main__"):
                #Get the second argument
                _input = sys.argv[1]
            else:
                #Get the first argument
                __input = sys.argv[1]
            print(str(__input))
            #Check if the input is add to database
            if(__input == "--add-to-db"):
                #Create the database
                db = DataBase()
                #Add the value
                db.add_value(sys.argv[2], sys.argv[3], sys.argv[4])
            else:
                #Get the response
                atria.say(__input, output=True)
        except IndexError as error:
            print("To use atria, run: python atria.py [TEXT]")
            print("You can add things to the database by running: python atria.py --add-to-db [KEY] [VALUE] [VALUE_TYPE]")
