#Binary Decoder
import sys

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def decode(grouping,binaryString):
    #detect if it is an 8 bit or 7 bit
    #split the string into groups of "grouping", put data in an array
    #initialize a string array
    binaryString = binaryString.replace(" ", "")
    groupings = []
    i = 0
    currentBinaryString = ""
    for char in binaryString:
        if (i != 0 and i % grouping == 0):
            groupings.append(currentBinaryString)
            currentBinaryString = char
        elif (i == len(binaryString)-1):
            currentBinaryString += char
            groupings.append(currentBinaryString)
        else:
            currentBinaryString += char
        i += 1
    #convert each grouping into a character
    decodedMessage = ""
    for binaryGrouping in groupings:
        n = int(binaryGrouping,2)
        if (n == 8):
            decodedMessage = decodedMessage[:len(decodedMessage)-1]
        if (n!=8 and n>0 and n<128):
            decodedMessage += chr(n)
    #return the resulting string
    return decodedMessage

#main

encode_text = sys.stdin.read().rstrip("\n")

candidate_text = decode(8, encode_text)

# Loop decoding until it finds letters
while True:
    for char in candidate_text:
        if char in ALPHABET or char in ALPHABET.upper():
            print(candidate_text)
            exit(0)
    
    candidate_text = decode(8, candidate_text)
    


# for line in sys.stdin:
#     # sys.stdout.write(decode(7,line))
#     # sys.stdout.write("\n")
#     sys.stdout.write(decode(8,line))
#     sys.stdout.write("\n")