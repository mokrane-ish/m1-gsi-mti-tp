
# -*- coding: utf-8 -*-

print("Salam Alykom")

# Variables declaration and checking data types
age = 125
print("type of age", type(age))

salaire = 3.14
print("type of salaire", type(salaire))

name = "Ahmed"
print("type of name", type(name))

# String substitution (%s for string, %d for integer)
s2 = "I am %s" % name
s3 = "I am %d old" % age
print(s2, s3)

# Lists: creation, type checking, and appending
liste = [1, 2, 31, 4]
print("type of ls", type(liste))
print(liste)

# Adding an element to the list
liste.append(5)
print(liste)

# Creating a word list
wordlist = ["I", "am", "learning", "english"]
print(wordlist)