import re
from sys import stdin

pattern = re.compile("([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[,\s]\s*([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])[,\s]\s*([01]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])")
text = stdin.read().rstrip("\n").split("\n")
for line in text:
    if pattern.match(line):
        print "match"