import sys, os
import sqlite3

class DataBase:

    def __init__(self, database="main_db"):
        if(database is "main_db"):
            database = os.path.dirname(os.path.abspath(__file__)) + "/main.db"
        self.__database = database
        #Create a database connection
        self.__connector = sqlite3.connect(self.__database)
        #Get the connector's cursor
        self.__cursor = self.__connector.cursor()
        #Create the database if it does not exist
        self.__cursor.execute("CREATE TABLE IF NOT EXISTS `Atria` (`key` TEXT, `value` TEXT, `value_type` TEXT)")

    def get_cursor(self):
        #Return the cursor
        return self.__cursor

    def add_value(self, key, value, value_type):
        #Insert the value to the database
        self.__cursor.execute("INSERT INTO `Atria` (`key`, `value`, `value_type`) VALUES ('%s', '%s', '%s')" %(key, value, value_type))
        #Commit the action
        self.__connector.commit()
        #Close the database
        self.close()

    def get_value(self, key, alleged_value_type, default_value):
        #Select all values matching the given inputs
        self.__cursor.execute("SELECT `value` FROM `Atria` WHERE `key`='%s' AND `value_type`='%s'" % (key, alleged_value_type))
        #Get all of the results, put them into this list
        __results = list()
        #Loop through all of the items
        for result in self.__cursor.fetchall():
            #Add the result
            __results.append(result)
        #Check if the length of the result is not 0
        if(len(__results) is not 0):
            try:
                #Close the database
                self.close()
                #Return the results
                return __results[0][0]
            except IndexError as error:
                #Do nothing
                pass
        #Return the default value
        return default_value

    def update(self, key, value, value_type):
        #Use the cursor to update the values
        self.__cursor.execute("UPDATE `Atria` SET `value`='%s' WHERE `key`='%s' AND `value_type`='%s'"%(key, value, value_type))

    def close(self):
        self.__cursor.close()
        self.__connector.close()
