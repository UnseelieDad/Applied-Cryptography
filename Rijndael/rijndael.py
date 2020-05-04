# Rijndael
# Sample template to show how to implement AES in Python

from sys import stdin, stdout, stderr
from hashlib import sha256
from Crypto import Random
from Crypto.Cipher import AES
import codecs

DECRYPT = True
ENCRYPT_KEY = ""
# the AES block size to use
BLOCK_SIZE = 16
# the padding character to use to make the plaintext a multiple of BLOCK_SIZE in length
PAD_WITH = "#"
# the key to use in the cipher
KEY = "rijndael"
# Dictionary to read in
DICTIONARY = "dictionary1-3.txt"
# Reverse dictionary processing?
REVERSE = False
# Filter out words in the dictionary?
FILTER = []
# Search for specfici tags
TAG = "%PDF-1.4"
USE_TAG = False
# Threshold for english words in plaintext
THRESHOLD = 0.75
# Minimum length for english words
MIN_WORD_LENGTH = 4
# Symbols to strip from words during normalization
SYMBOLS = "`~!@#$%^&*()-=_+{}[]\|:;\"<>,.?/"

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

# read in dictionary
dict_file = open(DICTIONARY, "r")
dictionary = dict_file.read().rstrip("\n")
dict_file.close()
dictionary = dictionary.split("\n")
norm_dict = normalize(dictionary)

ciphertext = stdin.read().rstrip("\n")

for key in dictionary:
    
	plaintext = decrypt(ciphertext, key)
	# Turn plain text into a normalized list of words to compare to the dictionary
	plain_list = normalize(plaintext.split("\n"))

	# compare words in plain text to words in dictionary and count the matches
	match_count = 0.0
	for word in plain_list:
		if word in norm_dict:
			match_count += 1

	if match_count/len(plain_list) >= THRESHOLD:
		stderr.write("KEY={}\n".format(key))
		print plaintext