# Le Chiffre

# Seth Martin
# 10252074
# CSC 444
# 4/15/2020
# This program implements a vigenere cipher that creates multiple candidate
# plaintexts from a ciphertext by testing potential keys from a dictionary.
# These plaintexts are tested against a word threshold to find the correct plaintext.
# Written in Python 3.7.5

from sys import stdin

DECRYPT = True
ENCRYPT_KEY = ""

# the alphabet
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/? "
# Alphabet for cipher-text 3 and 4
#ALPHABET = " -,;:!?/.'\"()[]$&#%012345789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxyYzZ"
#ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ,.0123456789"

SYMBOLS = "`~!@#$%^&*()-=_+{}[]\|:;\"<>,.?/"

THRESHOLD = 0.50

KEY = "3.14159265358"

# Decrypts cipher text using a vigenere cipher
def decrypt(cipher_text, key):
    plain_text = ""

    i = 0
    for x in range(len(cipher_text)):
        keyIndex = i % len(key)

        if cipher_text[x] not in ALPHABET:
            new_char = cipher_text[x]
        
        else:
            z = (len(ALPHABET) + ALPHABET.index(cipher_text[x]) - ALPHABET.index(key[keyIndex])) % len(ALPHABET)
            i += 1
            new_char = ALPHABET[z]

        plain_text += new_char

    return plain_text

# Encrypts cipher text using a vigenere cipher
def encrypt(plain_text, key):
    cipher_text = ""

    i = 0
    for x in range(len(plain_text)):
        keyIndex = i % len(key)

        if plain_text[x] not in ALPHABET:
            new_char = plain_text[x]
        
        else:
            z = (ALPHABET.index(plain_text[x]) + ALPHABET.index(key[keyIndex])) % len(ALPHABET)
            i += 1
            new_char = ALPHABET[z]

        cipher_text += new_char

    return cipher_text

# Strip punctuation/symbols from a word
def strip_punctuation(word):
    for character in word:
        if character in SYMBOLS:
            word = word.replace(character, "")
    return word


# Normalizes a list of strings by stripping symbols, converting to
# lower-case, and spliting up words with spaces in them
def normalize(text_list):
    new_list = []
    
    for word in text_list:
        # if a string is multiple words
        if " " in word:
            # remove it from the list and split it into separate words
            split = text_list.pop(text_list.index(word)).split(" ")
            # a new list for the normalized words
            normal_split = []
            
            # strip punctuation and convert to lowercase
            for new_word in split:
                new_word = strip_punctuation(new_word)
                new_word = new_word.lower()
                normal_split.append(new_word)
            
            # add normalized words back to the list
            new_list += normal_split
        
        # strip punctuation and convert to lowercase
        else:
            word = strip_punctuation(word)
            word = word.lower()
            new_list.append(word)
    
    return new_list

# Check that all characters in a word are in the alphabet
def in_alphabet(word):
    for character in word:
        if character not in ALPHABET:
            return False
    return True


## Main ##

# read in dictionary
dict_file = open("dictionary.txt", "r")
dictionary = dict_file.read().rstrip("\n")
dict_file.close()
dictionary = dictionary.split("\n")

# get potential keys from the dictionary
potential_keys = []
for word in dictionary:
    if in_alphabet(word):
        potential_keys.append(word)

# normalize the dicttionary for comparisons
dictionary = normalize(dictionary)

# decrypt cipher text
if DECRYPT is True:
    # read cipher text
    cipher_text = stdin.read().rstrip("\n")

    # try each keys on the cipher text until the correct plain text is found
    for key in potential_keys:
        key = KEY
        # If ciphertext has more than five lines, just test the first 5
        if len(cipher_text.split("\n")) > 5:
            plain_text = decrypt("\n".join(cipher_text.split("\n")[:5]), key)
            test_lines = True
        else:
            plain_text = decrypt(cipher_text, key)
            test_lines = False

        # Turn plain text into a normalized list of words to compare to the dictionary
        plain_list = normalize(plain_text.split("\n"))

        # compare words in plain text to words in dictionary and count the matches
        match_count = 0.0
        for word in plain_list:
            if word in dictionary:
                match_count += 1

        if match_count/len(plain_list) >= THRESHOLD:
            # If just the first 5 lines were decrypted, decrypt the rest and print
            if test_lines is True:
                plain_text = decrypt(cipher_text, key)
                print("KEY={}:\n{}".format(key, plain_text))
            else:
                print("KEY={}:\n{}".format(key, plain_text))
            
            exit(0)

# encrypt plain text with an encrypt key
else:
    plain_text = stdin.read().rstrip("\n")
    cipher_text = encrypt(plain_text, ENCRYPT_KEY)
    print("KEY={}:\n{}".format(ENCRYPT_KEY, cipher_text))