import sys      # For sysarg
import os       # To makefilepath valid for any os used
import re       # For regex
import pickle   # For pickling directory

# Step 2
# Taken and modifeid from https://github.com/kjmazidi/NLP/blob/master/Xtra_Python_Material/path%20demo/path_demo.py
def crossPlatformFP(filepath):                                  # Ensures filepath work on user's OS
    with open(os.path.join(os.getcwd(), filepath), 'r') as f:
        fileData = f.read()
    
    return fileData

# Step 3
class Person:
    def __init__(self, last, first, mi, id, phone):
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone
    
    def display(self):
        print("\nEmployee id: ", self.id)
        print("\t", self.first, self.mi, self.last)
        print("\t", self.phone)

def main():
    # Step 2
    if len(sys.argv) > 1:
        path  = sys.argv[1]
        fileData = crossPlatformFP(path)
        
        entries  = fileData.split('\n')         # Allows us to view one entry at a time
        entries.pop(0)                          # Removes header

        personDict = {}                         # Sets up empty dictionary

        for currEntry in entries:               # Processes the directory one person at a time
            data = currEntry.split(',')
            
            procData = processing(data)         # Processes current person
            
            if procData[3] in personDict:                                   # Checks if the current user is already in the directory
                print('\nThere is a conflict with the ID: ', procData[3])   # Does not actually fix conflict, just skips the new conflicting user
            else:                                                           # If it is a new ID it creates and adds a new person to the directory
                newPerson = Person(procData[0],  procData[1], procData[2], procData[3], procData[4])
                personDict[procData[3]] = newPerson
        
        pickle.dump(personDict, open('directory.p', 'wb'))

        printData()

    else:
        sys.exit('No filepath specified.')

# Step 4
def processing(dataIn):                     # Makes sure a person's data is all properly formatted
    currData = dataIn
    currData[0] = currData[0].capitalize()  # Formats last name with the form [A-Z][a-z]*
    currData[1] = currData[1].capitalize()  # Formats first name with the form [A-Z][a-z]*
    if currData[2]:                         # Checks if middle initial exists and makes it uppercase
        currData[2] = currData[2].upper()
    else:                                   # Otherwise defaults to middle initial of 'X'
        currData[2] = 'X'

    currData = idFormat(currData)
    currData = phoneFormat(currData)
    
    return currData

def idFormat(dataIn):                                           # Makes sure a person's ID is valid
    currData = dataIn
    idFlag = True
    while idFlag:                                               # Repeats until the ID is successfully validated
        currData[3] = currData[3].upper()
        regex = re.search("[A-Z][A-Z]\d\d\d\d", currData[3])    # Uses regex to make sure the ID has 2 letters followed by 4 digits
        if len(currData[3]) > 6 or not regex:                   # If the ID does not match regex then it returns None
            print('\nID invalid: ', currData[3])
            print('ID is two letters followed by 4 digits')
            currData[3] = input('Please enter a valid id: ')
        else :                                                  # Confirms valid ID
            idFlag  = False
    
    return currData

def phoneFormat(dataIn):                                            # Makes sure a person's phone number is valid
    currData = dataIn
    phoneFlag = True
    while phoneFlag:                                                # Repeats until the number is successfully validated
        regex = re.search("\d\d\d-\d\d\d-\d\d\d\d", currData[4])    # Uses regex to make sure the number is of form 123-456-7890
        if len(currData[4]) > 12 or not regex:                      # If the number does not match regex then itreturns None
            print('\nPhone ', currData[4], ' is invalid')
            print('Enter phone number in form 123-456-7890')
            currData[4] = input('Enter a phone number: ')
        else :
            phoneFlag  = False                                      # Confirms valid number
    
    return currData

# Step 5
def printData():                                            # Unpickles the binary file to display the formatted directory
    personDict = pickle.load(open('directory.p', 'rb'))
    for currValue in personDict.values():                   # Iterates through the values in the dict
        currValue.display()                                 # Ignores keys since we don't particularly need to check them

if __name__ == "__main__":
   main()
