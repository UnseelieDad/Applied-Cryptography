from hashlib import sha512
from sys import stdin

encrypted_pass = stdin.read().rstrip("\n")

dict_file = open("dictionary.txt", "r")
dictionary = dict_file.read().rstrip("\n")
dict_file.close()
dictionary = dictionary.split("\n")

for word in dictionary:
    if sha512(word.encode("utf-8")).hexdigest() == encrypted_pass:
        print(word)
        exit(0)
