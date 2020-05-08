# Rijndael

# Seth Martin
# 10252074
# CSC 444
# 5/3/2020
# This program takes ciphertext encoded using the AES algorithm and tries keys using a provided
# dictionary to generate candidate plaintexts. The plaintexts are compared against a threshold or tag
# to discover the real plaintext and key that generated it.
# Written in Python 3.8.2

from sys import stdin, stdout, stderr
from hashlib import sha256
from Crypto import Random
from Crypto.Cipher import AES
import re

DECRYPT = True
ENCRYPT_KEY = ""
# the AES block size to use
BLOCK_SIZE = 16
# the padding character to use to make the plaintext a multiple of BLOCK_SIZE in length
PAD_WITH = "#"
# Dictionary to read in
DICTIONARY = "dictionary.txt"
# Reverse dictionary processing if using ciphertext 5
REVERSE = False
# Filter for ciphertext 4 using "J" and "j"
FILTER = ["p", "P"]
# Search for specfici tags, use for ciphertext 5
TAG = "%PDF-1.4"
USE_TAG = False
# Threshold for english words in plaintext
THRESHOLD = 0.10
# Symbols to strip from words during normalization
SYMBOLS = "`~!@#$%^&*()-=_+{}[]\|:;\"<>,.?/"
# Search for RGB values
RGB = True

# decrypts a ciphertext with a key
def decrypt(ciphertext, key):
	# hash the key (SHA-256) to ensure that it is 32 bytes long
	key = sha256(key).digest()
	# get the 16-byte IV from the ciphertext
	# by default, we put the IV at the beginning of the ciphertext
	iv = ciphertext[:16]

	# decrypt the ciphertext with the key using CBC block cipher mode
	cipher = AES.new(key, AES.MODE_CBC, iv)
	# the ciphertext is after the IV (so, skip 16 bytes)
	plaintext = cipher.decrypt(ciphertext[16:])

	# remove potential padding at the end of the plaintext
	# figure this one out...

	return plaintext

# encrypts a plaintext with a key
def encrypt(plaintext, key):
	# hash the key (SHA-256) to ensure that it is 32 bytes long
	key = sha256(key).digest()
	# generate a random 16-byte IV
	iv = Random.new().read(BLOCK_SIZE)

	# encrypt the ciphertext with the key using CBC block cipher mode
	cipher = AES.new(key, AES.MODE_CBC, iv)
	# if necessary, pad the plaintext so that it is a multiple of BLOCK SIZE in length
	plaintext += (BLOCK_SIZE - len(plaintext) % BLOCK_SIZE) * PAD_WITH
	# add the IV to the beginning of the ciphertext
	# IV is at [:16]; ciphertext is at [16:]
	ciphertext = iv + cipher.encrypt(plaintext)

	return ciphertext

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

# MAIN

if RGB:
    pattern = re.compile("([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[,\s]\s*([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[,\s]\s*([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])")


# read in dictionary
dict_file = open(DICTIONARY, "r")
dictionary = dict_file.read().rstrip("\n").split("\n")
dict_file.close()
# strip punctuation and make all words lowercase for comparison
norm_dict = normalize(dictionary)

# If filter is active the potential keys are the filtered words from the dictionaty
# else just search the whole dictionary
potential_keys = []
for word in dictionary:
	if len(FILTER) > 0:
		if word[0] in FILTER:
			potential_keys.append(word)
	else:
		potential_keys = dictionary

if REVERSE:
    potential_keys.reverse()

ciphertext = stdin.read().rstrip("\n")

print potential_keys

for key in potential_keys:
    
	plaintext = decrypt(ciphertext, key)
	
	# If searching for a tag the correct plaintext is the one with the tag.
	if USE_TAG:
		plain_list = plaintext.split("\n")
		for text in plain_list:
			if text == TAG:
				stderr.write("KEY={}\n".format(key))
				print plaintext
				exit(0)

	elif RGB:
		plain_list = plaintext.split("\n")
		for text in plain_list:
			if pattern.match(text):
				print("KEY={}".format(key))
				print plaintext
				exit(0)


	else:
		# Turn plain text into a normalized list of words to compare to the dictionary
		plain_list = normalize(plaintext.split("\n"))

		# compare words in plain text to words in dictionary and count the matches
		match_count = 0.0
		for word in plain_list:
			if word in norm_dict:
				match_count += 1

		# if match ratio is greater than the threshold print as chosen plaintext
		if match_count/len(plain_list) >= THRESHOLD:
			#stderr.write("KEY={}\n".format(key))
			print "KEY={}".format(key)
			print plaintext
			#exit(0)