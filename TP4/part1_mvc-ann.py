#!/usr/bin/env python
# -*- coding: utf-8 -*-
# mvc-ann.py
# A directory in format of list [] of dictionaries {}
directory = [
    {"firstname": 'Ahmed', "familyname": 'Mahdi', 'tel': '0778787887'},
    {"firstname": 'Mohamed', "familyname": 'Mahdi', 'tel': '0778787887'},
    {"firstname": 'Mounir', "familyname": 'Katibi', 'tel': '0778787887'},
    {"firstname": 'Noui', "familyname": 'Brahimi', 'tel': '0778787887'},
]


def main():
    print("Finding a telephone")
    print("Give a name")
    familyname = input()
    # found elements number
    nb_found = 0
    # browse names
    for person in directory:
        # show all people with the given name
        if person['familyname'] == familyname:
            print(familyname, person['firstname'], person['tel'])
            nb_found += 1
    if not nb_found:
        print("This familyname %s doesn't exist " % familyname)


if __name__ == '__main__':
    main()