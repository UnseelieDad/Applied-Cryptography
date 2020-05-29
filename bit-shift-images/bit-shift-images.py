# XOR ROX

# Seth Martin
# 10252074
# CSC 444
# 5/3/2020
# This program takes an input image and for each pixel generates a random rgb key
# The key is then used to shift the bits of the original image to create three new images
# using and, or, and xor operations.
# Written in Python 3.8.2

from PIL import Image
from random import randint
from sys import stdout, stderr, stdin
from sys import argv


DECRYPT = True
SYMBOLS = "(),"

# the images
INPUT_IMAGE = "view-me.png"
AND_IMAGE = "and.png"
OR_IMAGE = "or.png"
XOR_IMAGE = "xor.png"
ENCRYPTED_IMAGE = "view-me.png"
DECRYPTED_IMAGE = "view-me-decrypted.png"

# strip parentheses, commas, and spaces from rgb values read from input
def strip_characters(rgb_list):
    new_list = []

    for value in rgb_list:
        new_value = value.strip(" ")
        for character in new_value:
            if character in SYMBOLS:
                new_value = new_value.replace(character, "")
        
        new_list.append(new_value)

    return new_list

# get the input image
img = Image.open(INPUT_IMAGE)
pixels = img.load()
rows, cols = img.size
stderr.write("[input.png is loaded]\n")

if DECRYPT:

    # setup decrypted image
    decrypted_img = Image.new("RGB", (rows, cols))
    decrypted_pixels = decrypted_img.load()

    # read key from stdin
    keys = stdin.read().rstrip("\n").split("\n")
    key_index = 0
    
    # For each pixel in the encrypted image
    row = 0
    while row < rows:
        col = 0
        
        while col < cols:
            # get the rgb key at the index corresponding to the current pixel
            key = keys[key_index]
            
            # format the key so it's just a list of values
            key = key.split(",")
            key = strip_characters(key)
            # xor the the rgb values of the current pixel with the key values
            r, g, b = pixels[row, col]
            decrypted_pixels[row, col] = ((r ^ int(key[0])), (g ^ int(key[1])), (b ^ int(key[2])))

            col += 1
            key_index += 1
        
        row += 1

    decrypted_img.save(DECRYPTED_IMAGE)

else:

    # Create and load the pixels for each new image
    and_img = Image.new('RGB', (rows, cols))
    or_img = Image.new('RGB', (rows, cols))
    xor_img = Image.new('RGB', (rows, cols))

    and_pixels = and_img.load()
    or_pixels = or_img.load()
    xor_pixels = xor_img.load()

    # for each pixel
    row = 0
    while row < rows:
        col = 0
        while col < cols:
            # Generate a random key in RGB format
            key = (randint(0,255), randint(0,255), randint(0,255))
            stdout.write(f"{str(key)}\n")
            stdout.flush()

            r, g, b = pixels[row, col]
            # and
            and_pixels[row, col] = ((r & key[0]), (g & key[1]), (b & key[2]))
            # or
            or_pixels[row, col] = ((r | key[0]), (g | key[1]), (b | key[2]))
            # xor
            xor_pixels[row, col] = ((r ^ key[0]), (g ^ key[1]), (b ^ key[2]))

            col += 1
        
        row += 1

    # write new image
    and_img.save(AND_IMAGE)
    or_img.save(OR_IMAGE)
    xor_img.save(XOR_IMAGE)



    stderr.write("[and.png, or.png, xor.png are all stored]\n")
    # If stdout is redirected to a file instead of a terminal
    if not stdout.isatty():
        stderr.write("[the key is stored to the specified file]\n")
