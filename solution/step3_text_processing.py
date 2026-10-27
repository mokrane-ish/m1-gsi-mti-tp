import re
import sys

def clean_text(text):
    """Remove punctuation from a text."""
    punct = "+.*/?,;\'#!:-"
    for p in punct:
        text = text.replace(p, "")
    return text

def tokenize(text):
    """Convert text into tokens, return a list of tokens (words)."""
    return text.split()

def tokenize2(text):
    """Convert text into tokens using regex."""
    spaces = r'\s+'
    words = re.split(spaces, text)
    return words

def word_freq(words):
    """Counts words and return a dictionary of words with their occurrences."""
    index = {}
    for w in words:
        if w in index:
            index[w] += 1
        else:
            index[w] = 1
    return index

def most_common_word(words_freq_table):
    """Finds and returns the most frequent word in the dictionary."""
    frequent = ""
    frequency = 0
    for word in words_freq_table:
        if words_freq_table[word] > frequency:
            frequent = word
            frequency = words_freq_table[word]
    return frequent

def read_file(filename):
    """Read a text from file."""
    try:
        f1 = open(filename, 'r', encoding='utf-8')
        text = f1.read()
        f1.close()
        return text
    except Exception as e:
        print("Can't open file:", filename)
        sys.exit()

def main():
    text = """
    Surprise steepest recurred landlord mr wandered amounted of.
    past oh shew roof Continuing devonshire but considered its. Rose
    is song neat. Do depend better praise do friend garden an wonder to.
    Intention age nay otherwise but breakfast. Around garden beyond to extent by.
    """
    
    print("--- Cleaning & Tokenizing Inline Text ---")
    cleaned_text = clean_text(text)
    print("Cleaned text:\n", cleaned_text)
    
    words = tokenize(cleaned_text)
    print("\nTokens:\n", words)
    
    words_nb = word_freq(words)
    print("\nWord Frequencies:\n", words_nb)
    
    print("\n--- Reading from data.txt ---")
    file_text = read_file("data.txt")
    file_words = tokenize(clean_text(file_text))
    file_freq = word_freq(file_words)
    print("File Word Frequencies:\n", file_freq)
    
    most_frequent = most_common_word(file_freq)
    print("\nMost frequent word is:", most_frequent, "occurring", file_freq[most_frequent], "times")

if __name__ == "__main__":
    main()