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
from sys import stdout, stderr
from sys import argv

# the images
INPUT_IMAGE = "input.png"
AND_IMAGE = "and.png"
OR_IMAGE = "or.png"
XOR_IMAGE = "xor.png"

# get the input image
img = Image.open(INPUT_IMAGE)
pixels = img.load()
rows, cols = img.size
stderr.write("[input.png is loaded]\n")

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
