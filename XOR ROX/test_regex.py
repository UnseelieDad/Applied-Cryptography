import re
from sys import stdin

pattern = re.compile("\([^\)]*\)")
text = stdin.read().rstrip("\n").split("\n")
for line in text:
    if pattern.match(line):
        print "match"