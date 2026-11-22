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

    def get_all(self):
        """ Find a tel by name"""
        # List of found people
        persons = []
        for persn in self.directory:
            # display all people
            persons.append(persn)
        # a table with field names
        return persons

    def add(self, name, firstname, tel):
        """ Add a person """
        person = {}
        person["familyname"] = name
        person["firstname"] = firstname
        person["tel"] = tel
        self.directory.append(person)


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

    def input_add(self):
        """get name to add"""
        print("Add a person")
        print("Give a name")
        name = input()
        print("Give a firstname")
        firstname = input()
        print("Give a firstname")
        tel = input()
        return (name, firstname, tel)


class controller:
    def __init__(self):
        """controller constrctor"""
        # init data model
        self.data_model = model()
        self.myviewer = view()

    def search(self):
        # search a name
        name = self.myviewer.input()
        persons = self.data_model.search(name)
        self.myviewer.output(persons)

    def get_all(self):
        # display all people
        persons = self.data_model.get_all()
        self.myviewer.output(persons)

    def add(self):
        """ Add a new name """
        name, firstname, tel = self.myviewer.input_add()
        self.data_model.add(name, firstname, tel)
        persons = self.data_model.get_all()
        self.myviewer.output(persons)


if __name__ == '__main__':
    contro = controller()
    contro.search()