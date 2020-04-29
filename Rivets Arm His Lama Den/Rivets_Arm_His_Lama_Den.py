# Rivets Arm His Lama Den

# Seth Martin
# 10252074
# CSC 444
# 4/15/2020
# This program implements a version of the RSA
# Algorithm that decrypts cipher text given only the n value
# By trying each generated value of e until the plaintext is found.
# Written in Python 3.7.5

# Rivets Arm His Lama Den is an anagram of the name of the thre researches who
# created RSA:
# Rivest, Shamir, and Adleman

from sys import stdin, stdout

# Set to true to use naieve inverse method
NAIEVE = False

# factors a number n into the product of two primes
def factor(n):
    for i in range(3, int(n ** 0.5 + 1), 2):
        if (n % i == 0) and isPrime(i) and isPrime(n/i):
            return i, int(n / i)

    return None

# determines if a given number is prime
def isPrime(n):
    if (n % 2 == 0):
        return False

    for i in range(3, int(n ** 0.5 + 1), 2):
        if (n % i == 0):
            return False

    return True

# recursively returns the greatest common divisor of a and b
def gcd(a, b):
    if (b == 0):
        return a
    return gcd(b, a % b)

# generates all e's and randomly returns one
def genEs(z):
    es = []

    # 1 and 2 are not valid primes for this purpose
    e = 3
    while e < z:
        if (isPrime(e) and gcd(z, e) == 1):
            es.append(e)
        # Increment e so that it is always of the form 2^n-1
        e = (e - 1) * 2 + 1

    return es

# naively calculates the inverse modulo of e and z
def naiveInverse(e, z):
    d = 0

    while (d < z):
        if ((e * d) % z == 1):
            return d
        d += 1

# calculates the inverse modulo of e and z using
# the extended Euclidean algorithm
def euclideanInverse(e, z):
    t = 0
    r = z
    newt = 1
    newr = e

    while newr != 0:
        quotient = r // newr
        
        t, newt = newt, (t - quotient * newt)
        r, newr = newr, (r - quotient * newr)

    if r > 1:
        return "ERROR: e is not invertible"
    
    # make t positive
    if t < 0:
        t += z

    return t

# encrypts a message M with a public key K_pub to get C
def encrypt(M, K_pub):
    return (M ** K_pub[0] % K_pub[1])

# decrypts a ciphertext C with a private key K_priv to get M
def decrypt(C, K_priv):
	return (C ** K_priv[0] % K_priv[1])

## Main ## 

# read from stdin
ciphertext = stdin.read().rstrip("\n").split("\n")

# set n
n = int(ciphertext[0])

# set ciphertext to be decrypted
C = ciphertext[1].split(",")

# factor p and q
p, q = factor(n)
print(f"p={p}, q={q}")
print(f"n={n}")

# calculate z
# Python 3.7.5 adds a .0 on to the end of the number so convert to int
z = int((p - 1) * (q - 1) / gcd(p - 1, q - 1))
print(f"z={z}")

# generate e values
es = genEs(z)

# Test cipher text on each value of e
for e in es:
    print("\n--\n")
    print(f"Trying e={e}")
    
    # calculate d based off current e and z
    # using either naieve method or euclidean
    if NAIEVE is True:
        d = naiveInverse(e, z)
    else:
        d = euclideanInverse(e, z)
    print(f"d={d}")

    # generate keys
    K_pub = (e, n)
    K_priv = (d, n)
    print(f"Public Key: {K_pub}")
    print(f"Private Key: {K_priv}")

    # decrypt message
    M = ""
    for c in C:
        m = decrypt(int(c), K_priv)
        # if m is a number in the ASCII table
        if m in range(0,255):
            M += chr(m)
            stdout.write(chr(m))
            stdout.flush()
        else:
            print("ERROR: Invalid Plaintext")
            break

print
