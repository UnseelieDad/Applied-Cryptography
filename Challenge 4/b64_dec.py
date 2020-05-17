from sys import stdin
from base64 import b64decode

encoded_text = stdin.read().rstrip("\n")
print(b64decode(encoded_text).decode("utf-8"))