# -*- coding: utf-8 -*-
from tkinter import Tk, Label, Button, END, Text, W, E
import sys

# 1. The Model (Same as Part 4)
class model_file:
    def __init__(self):
        self.directory = []
        try:
            myfile = open("directory.txt", "r")
        except:
            print("Can't open DataFile. Please create 'directory.txt'.")
            sys.exit()
        
        lines = myfile.readlines()
        for line in lines:
            line = line.strip('\n')
            if line:
                fields = line.split('\t')
                if len(fields) >= 3:
                    person = {"familyname": fields[0], "firstname": fields[1], "tel": fields[2]}
                    self.directory.append(person)
        myfile.close()

    def __del__(self):
        try:
            myfile = open("directory.txt", "w")
            for person in self.directory:
                line = "\t".join([person['familyname'], person['firstname'], person['tel']])
                line += "\n"
                myfile.write(line)
            myfile.close()
        except:
            pass

    def search(self, nom):
        persons = []
        for persn in self.directory:
            if persn["familyname"] == nom:
                persons.append(persn)
        return persons

    def get_all(self):
        return self.directory

    def add(self, name, firstname, tel):
        person = {"familyname": name, "firstname": firstname, "tel": tel}
        self.directory.append(person)


# 2. The View and Controller Combined (Tkinter GUI)
class view_tk:
    def __init__(self, model):
        master = Tk()
        self.master = master
        self.model = model
        master.title("Directory")
        
        # LABELS
        self.label = Label(master, text="Family Name:")
        self.label_firstname = Label(master, text="First Name:")
        self.label_tel = Label(master, text="Tel:")
        self.output_label = Label(master, text="Output:")
        
        # TEXT ENTRIES
        self.entry = Text(master, height=1, width=20)
        self.entry_firstname = Text(master, height=1, width=20)
        self.entry_tel = Text(master, height=1, width=20)
        
        # OUTPUT BOX
        self.output = Text(master, height=10, width=65)
        
        # BUTTONS
        self.search_button = Button(master, text="Search", command=lambda: self.update("search"))
        self.add_button = Button(master, text="Add", command=lambda: self.update("add"))
        self.all_button = Button(master, text="Get All", command=lambda: self.update("get_all"))
        
        # LAYOUT (Grid)
        self.label.grid(row=0, column=0, sticky=W)
        self.label_firstname.grid(row=0, column=1, sticky=W)
        self.label_tel.grid(row=0, column=2, sticky=W)
        
        self.entry.grid(row=1, column=0, sticky=W+E, padx=2)
        self.entry_firstname.grid(row=1, column=1, sticky=W+E, padx=2)
        self.entry_tel.grid(row=1, column=2, sticky=W+E, padx=2)
        
        self.search_button.grid(row=2, column=0, pady=5)
        self.add_button.grid(row=2, column=1, pady=5)
        self.all_button.grid(row=2, column=2, pady=5)
        
        self.output_label.grid(row=3, column=0, sticky=W)
        self.output.grid(row=4, column=0, columnspan=3, sticky=W+E, padx=2)

    def update(self, method):
        familyname = self.entry.get("1.0", END).strip()
        firstname = self.entry_firstname.get("1.0", END).strip() # Fixed from the manual's typo
        tel = self.entry_tel.get("1.0", END).strip()
        
        self.output.delete("1.0", END) # Clear the output box before displaying new results
        
        if method == "search":
            result = self.search(familyname)
        elif method == "add":
            result = self.add(familyname, firstname, tel)
        elif method == "get_all":
            result = self.get_all()
        else:
            result = ""
            
        self.output.insert(END, str(result))

    def add(self, familyname, firstname, tel):
        self.model.add(familyname, firstname, tel) # Fixed from self.model.ajouter
        return "Added successfully!"

    def search(self, familyname):
        result = self.model.search(familyname) # Fixed from self.model.rechercher
        if result:
            return result
        else:
            return f"'{familyname}' not found"

    def get_all(self):
        return self.model.get_all()

    def run(self):
        self.master.mainloop()

# 3. Main Controller Execution
def controller3():
    data_model = model_file()
    my_viewer = view_tk(data_model)
    my_viewer.run() # Launch GUI

if __name__ == '__main__':
    controller3()