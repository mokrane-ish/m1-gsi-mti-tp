# -*- coding: utf-8 -*-
import sys

class model_file:
    """ Data Model class that saves to a file """
    def __init__(self):
        self.directory = []
        try:
            # Requires directory.txt to exist in the same folder
            myfile = open("directory.txt", "r")
        except:
            print("Can't open DataFile. Please create an empty 'directory.txt' file first.")
            sys.exit()
        
        lines = myfile.readlines()
        for line in lines:
            line = line.strip('\n')
            if line: # Skip empty lines
                fields = line.split('\t')
                person = {}
                person["familyname"] = fields[0]
                person["firstname"] = fields[1] 
                person["tel"] = fields[2]
                self.directory.append(person)
        myfile.close()

    def __del__(self):
        """ Destructor: saves data back to the file when the program exits """
        try:
            myfile = open("directory.txt", "w")
        except:
            print("Can't open DataFile to write")
            sys.exit()
            
        for person in self.directory:
            # Join fields with a tab character \t
            line = "\t".join([person['familyname'], person['firstname'], person['tel']])
            line += "\n"
            myfile.write(line)
        myfile.close()

    def search(self, nom):
        persons = []
        for persn in self.directory:
            if persn["familyname"] == nom:
                persons.append(persn)
        return persons

    def get_all(self):
        persons = []
        for persn in self.directory:
            persons.append(persn)
        return persons

    def add(self, name, firstname, tel):
        person = {}
        person["familyname"] = name
        person["firstname"] = firstname
        person["tel"] = tel
        self.directory.append(person)


class view:
    def __init__(self):
        pass

    def input(self):
        print("Finding a phone")
        print("Give a name")
        name = input()
        return name

    def output(self, persons):
        print("List of found names")
        print(" %d found people " % len(persons))
        for pers in persons:
            print(pers["familyname"], pers["firstname"], pers['tel'])

    def input_add(self):
        print("Add a person")
        print("Give a name")
        name = input()
        print("Give a firstname")
        firstname = input()
        print("Give a phone number") # Includes your fix!
        tel = input()
        return (name, firstname, tel)


class controller:
    def __init__(self):
        # We now use model_file instead of the hardcoded model
        self.data_model = model_file()
        self.myviewer = view()

    def search(self):
        name = self.myviewer.input()
        persons = self.data_model.search(name)
        self.myviewer.output(persons)

    def get_all(self):
        persons = self.data_model.get_all()
        self.myviewer.output(persons)

    def add(self):
        name, firstname, tel = self.myviewer.input_add()
        self.data_model.add(name, firstname, tel)
        persons = self.data_model.get_all()
        self.myviewer.output(persons)


if __name__ == '__main__':
    contro = controller()
    
    # Add a person
    contro.add()
    
    # FORCE the destructor to run now, before Python shuts down
    del contro