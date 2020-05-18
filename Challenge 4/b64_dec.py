from sys import stdin
import base64

encoded_text = stdin.read().rstrip("\n")
#encoded_text += "=" * ((4 - len(encoded_text) % 4) % 4)
print(base64.decodebytes(encoded_text.encode("ascii")).decode("ascii"))