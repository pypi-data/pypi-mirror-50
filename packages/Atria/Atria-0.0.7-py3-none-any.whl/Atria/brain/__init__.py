import sys, os
from Atria import database
from Atria.database import DataBase

class Brain(DataBase):

    def __init__(self):
        #Initialize a database
        self.__database = DataBase()

    def say(self, input, output=True):
        #Get the response
        response = str(self.__database.get_value(input, "response", "I haven't the slightest clue"))
        #Check if the developer / user wants output
        if(output is True):
            #Print the response
            print(response)
        #Return the response
        return response
