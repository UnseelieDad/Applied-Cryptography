# Rivets Arm His Lama Den
# Implements a simplistic RSA algorithm with the following characteristics:
# -let's restrict ourselves to "small" numbers
# -write a function that determines if a number is prime
# -write a function that generates all prime numbers within some given range
# -randomly select two of the primes
# -calculate n = p * q
# -write a function that recursively calculates the greatest common divisor of a and b
# -calculate z = ((p - 1) * (q - 1)) / gcd(p - 1, q - 1)
# -write a recursive gcd function
# -write a function that generates all e's and randomly selects one (using isPrime and gcd)
# -write a function that naively calculates d, the modulo inverse of e
# -output the public and private keys
# -write an encrypt function that encrypts message M with the public key to get C
# -write a decrypt function that decrypts ciphertext C with the private key to get M

from sys import stdin
from random import choice

# Range for primes p and q
MIN_PRIME = 100
MAX_PRIME = 2000
# determines if a given number is prime
def isPrime(n):
    if (n % 2 == 0):
        return False

    for i in range(3, int(n ** 0.5 + 1), 2):
        if (n % i == 0):
            return False

    return True

# returns all prime numbers within a min/max range
def getPrimes(min, max):
    primes = []

    for n in range(min, max):
        if (isPrime(n)):
            primes.append(n)

    return primes

# generates all e's and randomly returns one
def genEs(z):
    es = []

    e = 3
    while e < z:
        if (isPrime(e) and gcd(z, e) == 1):
            es.append(e)
        # Increment e so that it is always of the form 2^n-1
        e = (e - 1) * 2 + 1

    return es
# recursively returns the greatest common divisor of a and b
def gcd(a, b):
    if (b == 0):
        return a
    return gcd(b, a % b)

# naively calculates the inverse modulo of e and z
def naiveInverse(e, z):
    m0 = z
    y = 0
    x = 1

    if z == 1:
        return 0

    while e > 1:
        # q is quotient
        q = e // z
        t = z

        z = e % z
        e = t
        t = y

        y = x - q * y
        x = t

    if x < 0:
        x = x + m0

    return x

# encrypts a message M with a public key K_pub to get C
def encrypt(M, K_pub):
    return (M ** K_pub[0] % K_pub[1])

# decrypts a ciphertext C with a private key K_priv to get M
def decrypt(C, K_priv):
	return (C ** K_priv[0] % K_priv[1])

# MAIN
# get input
M = stdin.read().rstrip("\n").split("\n")

# get the primes
primes = getPrimes(MIN_PRIME, MAX_PRIME)
p = choice(primes)
q = p
while (q == p):
    q = choice(primes)

print(f"p={p}, q={q}")

# calculate n and z
n = p * q
print(f"n = {n}")
z = int(((p - 1) * (q - 1) / gcd(p - 1, q - 1)))
print(f"z={z}")

# get the es and select an e
es = genEs(z)
e = choice(es)
print(f"e={e}")

# calculate d
d = naiveInverse(e, z)
print(f"d={d}")

# generate the public and private keys
K_pub = (e, n)
K_priv = (d, n)
print(f"Public Key: {K_pub}")
print(f"Private Key: {K_priv}")

# implement RSA for the specified input Ms
for m in M:
    print("--")
    m = int(m)
    c = encrypt(m, K_pub)
    print(f"m={m}")
    print(f"c={c}")
    m = decrypt(c, K_priv)
    print(f"m={m}")