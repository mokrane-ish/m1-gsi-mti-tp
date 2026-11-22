# -*- coding: utf-8 -*-
# A directory in format of list () of dictionaries {}


class model:
    """ data model class"""

    def __init__(self):
        self.directory = [
            {"firstname": 'Ahmed', "familyname": 'Mahdi', 'tel': '0778787887'},
            {"firstname": 'Mohamed', "familyname": 'Mahdi', 'tel': '0778787887'},
            {"firstname": 'Mounir', "familyname": 'Katibi', 'tel': '0778787887'},
            {"firstname": 'Noui', "familyname": 'Brahimi', 'tel': '0778787887'},
        ]

    def search(self, nom):
        """ lookup for a tel by lastname"""
        # found people list
        persons = []
        for persn in self.directory:
            # show all people with the given name
            if persn["familyname"] == nom:
                persons.append(persn)
        # return a list of dictionaries
        return persons


class view:
    def __init__(self):
        pass

    def input(self):
        """ retrieve the name to search for"""
        print("Finding a phone")
        print("Give a name")
        name = input()
        return name

    def output(self, persons):
        """ display information from a list of persons"""
        print("List of found names")
        print(" %d found people " % len(persons))
        for pers in persons:
            print(pers["familyname"], pers["firstname"], pers['tel'])


def controller():
    # This program allows you to search the number
    # in a table by its name, and display
    # read data from the keyboard
    data_model = model()
    myviewer = view()
    # search a name
    name = myviewer.input()
    persons = data_model.search(name)
    myviewer.output(persons)


if __name__ == '__main__':
    controller()