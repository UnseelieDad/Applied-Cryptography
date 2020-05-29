# Et tu, Brute?
# Program written in Python3
# Seth Martin
# CSC 444
# 3/17/20
# This program takes in cypertext from stdin and generates candidate cyphers
# It then prints out the most likely candidate with the shift

import fileinput
import collections
import base64
import binascii

# the alphabet
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/? "

# Alternate alphabet for third cipher
#ALPHABET = " -,;:!?/.'\"()[]$&#%012345789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxyYzZ"

SYMBOLS = ".?,\"!()"

THRESHOLD = 75

DECRYPT = True

# get words from the dictioanry
file = open("dictionary.txt", "r")
dictionary = file.readlines()
file.close()

# decrypt multiple lines of cipher text
def decryptLines(cipher_text, key):
    plain_text= []
    
    # decrypt the text line by line
    for line in cipher_text:
        plain_line = []

        # Iterate through each character in the text
        for character in line:
            if character in ALPHABET:
                x = ALPHABET.index(character)
                # get index of character in ciphered alphabet
                x = (x - key) % len(ALPHABET)
                # use new index in the original alphabet to get the decrypted character
                character = ALPHABET[x]
            plain_line.append(character)

        plain_line = "".join(plain_line)
        plain_text.append(plain_line)
    
    # create plain string
    plain_text = "\n".join(plain_text)

    return plain_text

def encryptLines(plain_text, key):
    
    cipher_text = []

    for line in plain_text:
        cipher_line = []

        for character in line:
            x = ALPHABET.index(character)
            x = (x+key) % len(ALPHABET)
            character = ALPHABET[x]
            cipher_line.append(character)
        cipher_line = "".join(cipher_line)
        cipher_text.append(cipher_line)
    cipher_text = "\n".join(cipher_text)

    return cipher_text

# see if word is in the dictionary
def checkDictionary(text):

    for word in dictionary:        
        # if the passed in word is a word in the dictionary return true, else return false
        if text == word.strip("\n"):
            return True
    return False


if DECRYPT is True:
    cipher_text = []

    # Read  cipher text from stdin
    for line in fileinput.input():
        line = line.rstrip("\n")
        cipher_text.append(line)

    # make a string to get letter frequencies from
    cipher_string = "\n".join(cipher_text)

    # Get letter frequencies and prioritize shifts based off the most frequent letters
    # generates a list of tuples with the letter and the number of times it occurs in order of most frequent to least
    frequencies = collections.Counter(cipher_string).most_common()

    # Generate candidates using the indicies of the most frequent letters as keys
    candidates = []
    used_keys = []
    for frequency in frequencies:

        # if character is not a new line
        if frequency[0] is not "\n":
            letter = frequency[0]

        if letter in ALPHABET:
            key = ALPHABET.index(letter)
            used_keys.append(key)
            # decrypt cipher text
            plain_text = decryptLines(cipher_text, key)

            # add string to candidates
            candidates.append((plain_text, key))

    # generate the rest of the candidates by trying a shift at each unused character in the alphabet
    for key in range(len(ALPHABET)):
        # ignore a shift of 0 or keys that have already been used
        if key == 0 or key in set(used_keys): 
            continue
        
        # decrypt cipher text
        plain_text = decryptLines(cipher_text, key)

        # add string to candidates
        candidates.append((plain_text, key))

    # Compare words in candidates to words in dictionary

    for candidate in candidates:

        # Get text from candidate and split it by spaces into words
        text = candidate[0]

        # print("Key={}".format(candidate[1]))
        # try:
        #     decode = base64.decodestring(text)
        #     print(decode)
        # except binascii.Error:
        #     print("no correct base64")

        # print("\n")

        # potential keys : 27

        text_list = text.split(" ")

        # count the number of words in the text that match words in the dictionary
        count = 0
        for word in text_list:
            if checkDictionary(word.strip(",!.?\"\n")) is True:
                count += 1
        
        # If more than 75% of the words match words in the dictionary use it as the plain text
        match_percentage = count/len(text_list)*100
        if match_percentage >= THRESHOLD:
            print("SHIFT={}:".format(candidate[1]))
            print(candidate[0])
            break

else:

    plain_text = []

    # Read  cipher text from stdin
    for line in fileinput.input():
        line = line.rstrip("\n")
        plain_text.append(line)

    print(plain_text)
    cipher_text = encryptLines(plain_text, 34)
    print(cipher_text)


