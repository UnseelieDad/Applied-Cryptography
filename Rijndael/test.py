from sys import stdin

ciphertext = stdin.read().rstrip("\n")
print stdin.encoding
print ciphertext
print ciphertext.encode("utf-8")
print type(ciphertext)