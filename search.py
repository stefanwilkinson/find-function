import sys
import os

class SearchFiles():

    def __init__(self):#constructor that is setting up global attributes for use throughout the program
        self.filename = sys.argv[1] #gets the directory to search that is inputted after search.py (my filename) in command line
        self.values = dict() #this will store all of the text found in each file with the file name as the keys
        self.dir = dict() #this will hold the directories for the text files with the file name as the keys
        self.file_opening() #method call to actually iterate through the directories and files and folders
        self.search() #method call to search through the contents found based upon user query

    def file_opening(self):#method that will iterate through the directories and files
        try:
            for directory, subdirectory, files in os.walk(self.filename): #looking through directories using os.walk(which does it recursively I believe) for files and directories and subdirectories
                for f in files: #iterating through each of the files found
                    current = os.path.join(directory, f) #gets the full directory path of the current file f
                    with open(current, 'r') as content: #opens that file up in read mode and can be referenced by content
                        data = content.read().replace('\n', ' ').split(" ") #replacing next line characted with a space and then splitting the words by delimeter of a space
                        data = [x.lower() for x in data] #this is making everything in the data list lowercased
                        data = list(filter(None, data)) #this is getting rid of all of the whitepspaces
                        self.add_index(data,f,current) #method call to make all of the data into indexes and takes three parameters: the data it self, the file name and also the current directory
        except: #if theres an error then it prints out there was an error
            print("sorry we encountered an error! please try again later :D")
    def add_index(self,text,doc_id,cdir):#method that will index all of the data alongside their directories
        self.values[doc_id] = text #adding data list as value to dictionary where the key is the file name
        self.dir[doc_id] = cdir #adding the current directory as value to dictionary where the key is the file name

    def search(self):#search function that based upon the query searches for all occurences or every occurence of the terms put in
        try:
            while True: #infinite so user can enter query after query
                query = input("\nenter query>") #asks the user for a query and stores it
                query = query.lower().strip(' ').split(' ') #takes out extra spaces and then splits it by spaces giving us only words
                count = 0 #will be used to store how many results were found (could have also used len of results array to find how many results)
                results = [] #list that will store the location of the results that were found
                if query[0] == 'and':
                    for keys, values in self.values.items(): #iterates through the items in values
                        if all(val in values for val in query[1:]): #checks to see if everything in the query from position 1 to the end is in values so checks to see if they all occur in same file
                            count+=1 #adds 1 for each result found
                            results.append(" *** " + self.dir[keys]) #appends the directory found to the results to be shown later
                elif query[0] == 'or':
                    for keys,values in self.values.items():
                        if any(val in values for val in query[1:]):# checks to see if something in the query from position 1 to the end is in values so checks to see if just one occurs in the file
                            count += 1 #adds 1 for each result found
                            results.append(" *** " + self.dir[keys]) #appends the directory found to the results to be shown later
                else:
                    print("\ninvalid query! Must use AND or OR to begin query\n")#if user enters something other then and or or then it allows them to try again
                print("\nFound {} results\n".format(count)) #shows how many results were found using the count variable as it stores how much resuts
                for r in results: #prints out each result in the results list to show where the query results was found in terms of directory and file
                    print(r)
        except:
            print("\n\nThanks for using the search function!") #if user hits ctrl+c or del to exit, this message is printed for them (could have used keyboardinputerror exception but decided on just printing this regardless of the error so they can start over
test = SearchFiles() #creating the object so it runs when called from command line