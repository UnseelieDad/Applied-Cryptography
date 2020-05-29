# Abraxas
#
# Seth Martin
# 3/24/20
# CSC 444
# 
# This program takes cipher-text from stdin that has been encrypted with a key cypher and uses a dictionary full of potential keys
# to generate candidate plain-texts. It filters each generated text by checking each word in the plain-text 
# against words in the dicitonary. If 3/4 of the words match that plain-text is selected. 

from sys import stdin
from collections import Counter
import string
# the alphabets
#ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/? "
#ALPHABET =  " -,;:!?/.'\"()[]$&#%012345789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxyYzZ"
#ALPHABET = "7JZv. 964jMLh)5QtAS2PXWaFU8,/cpkY'O(Tqr?dsEmbRwINVKBez1=3+H0GyfxCiD\"lg:!uo"
ALPHABET = "1234567890"

# collection of symbols to strip from words when checkign against the dictionary
SYMBOLS = ".?,\"!()"

# Threshold for how many words in the plaintext should match the dictionary before being selected
# Need to bring down threshold to 5 for cipher-text 4
THRESHOLD = 0.5

# To search the list of keys in reverse for cipher 3
REVERSE_KEYS = False

DECRYPT = True
ENCRYPT_KEY = "27"

# This function decrypts a key cipher given the cipher-text and a key
def decypt(cipher_text, key):

    plain_text = []

    # get new alphabet based on key
    new_alpha = key

    for character in ALPHABET:
        if character not in new_alpha:
            new_alpha += character

    # split multi-line text into component lines to preserve those lines in plain-text form
    cipher_lines = cipher_text.split("\n")

    for line in cipher_lines:
        # split each line into words
        line = line.split(" ")
        plain_line = []
        
        for word in line:
            plain_word = []
            
            # for each character in a a ciphered word, get the index of that character
            # in the new alphabet then get the plain character is the character
            # in the old alphabet at that index
            for character in word:
                if character in ALPHABET:
                    x = new_alpha.index(character)
                    character = ALPHABET[x]
                plain_word.append(character)
            
            # rejoin the words and lines
            plain_word = "".join(plain_word)
            plain_line.append(plain_word)
        
        plain_line = " ".join(plain_line)
        plain_text.append(plain_line)
    
    plain_text = "\n".join(plain_text)

    return plain_text
           

def encrypt(plain_text, key):

    cipher_text = []

    new_alpha = key

    for character in ALPHABET:
        if character not in new_alpha:
            new_alpha += character

    plain_lines = plain_text.split("\n")

    for line in plain_lines:
        line = line.split(" ")
        cipher_lines = []

        for word in line:
            cipher_word = []

            for character in word:
                x = ALPHABET.index(character)
                character = new_alpha[x]
                cipher_word.append(character)

            cipher_word = "".join(cipher_word)
            cipher_lines.append(cipher_word)

        cipher_lines = " ".join(cipher_lines)
        cipher_text.append(cipher_lines)

    cipher_text = "\n".join(cipher_text)

    return cipher_text

# this function checks if all the characters in a string are unique
def unique_characters(text):
    
    # generates a dictionary with the frequency of each letter in the string
    char_freq = Counter(text)

    # if all characters are unique every value in the dictionary should be 1
    for value in char_freq.values():
        if value is not 1:
            return False

    return True

# This function strips punctuation from words in a list
def strip_punctuation(text):
    
    text_list = text.split(" ")
    stripped_list = []

    for word in text_list:

        # if a character is punctation replace it with nothing in the string
        for character in word:
            if character in SYMBOLS:
                word = word.replace(character, "")

        stripped_list.append(word)

    return stripped_list

def in_alphabet(text):

    for character in text:
        if character not in ALPHABET:
            return False
    return True

### MAIN ###

if DECRYPT is True:
    # read dictionary
    dict_file = open("dictionary.txt", "r")
    dictionary = dict_file.read().rstrip("\n")
    dictionary = dictionary.split("\n")

    # get potential keys from dictionary
    # if a word has all unqiue characters then it is a potential key
    potential_keys = []
    for word in dictionary:
        if unique_characters(word) and in_alphabet(word):
            potential_keys.append(word)

    

    # reverse key order for cipher 3
    if REVERSE_KEYS is True:
        potential_keys.reverse()

    # get cipher text
    cipher_text = stdin.read().rstrip("\n")

    for key in potential_keys:
        

        plain_text = decypt(cipher_text, key)

        # print(key)
        # print(plain_text)

        stripped_list = strip_punctuation(plain_text)
        match_count = 0.0

        # see how many words are in the dictionary
        for word in stripped_list:
            if word in dictionary:
                match_count += 1

        # If the ratio of words in the dictionary is at or more than the threshold, use this text
        if match_count/len(stripped_list) >= THRESHOLD:
            print("KEY={}:".format(key))
            print(plain_text)
            exit(0)
        
    print("No candidates have enough matching words for a threshold of {}".format(THRESHOLD))

else:

# get plain text
    plain_text = stdin.read().rstrip("\n")
    cipher_text = encrypt(plain_text, ENCRYPT_KEY)
    print(cipher_text)