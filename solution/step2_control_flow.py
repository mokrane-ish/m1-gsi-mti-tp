# Flows Control
a = 15
if a > 15:
    print('a is greater than 15')
elif a <= 15 and a >= 10:
    print('a between 10 and 15')
else:
    print('a is less than 10')

# Test if an element belongs to a list
liste = [1, 2, 31, 4, 5]
a = 5
if a in liste:
    print("a exists in list")

# Loops
wordlist = ["I", "am", "learning", "english"]
for word in wordlist:
    print(word)

# Loops and tests: Count occurrences of a character in a string
chaine = """The sky, oh the sky! It stretches above us, vast and endless.
The sky is a canvas, a canvas of blue, blue like the ocean on a clear summer day.
It's a canvas of possibilities, possibilities as vast as the sky itself."""
caractere = "e"
cpt = 0

for c in chaine:
    if c == caractere:
        cpt += 1

print("Char %s exists %d times" % (caractere, cpt))