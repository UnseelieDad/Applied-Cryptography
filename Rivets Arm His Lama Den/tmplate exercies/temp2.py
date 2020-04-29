# Rivets Arm His Lama Den
# Implements a simplistic RSA algorithm with the following characteristics:
# -expect input to contain the public key on the first line and a comma separated list of numbers representing encrypted values on the second line
# -the input provides n and e
# -write a function that determines if a number is prime
# -write a function that factors a number into the product of two primes
# -write a function that recursively calculates the greatest common divisor of a and b
# -write a function that naively calculates d, the modulo inverse of e
# -write a decrypt function that decrypts ciphertext C with the private key to get M
# -factor n as the product of two primes, p and q
# -calculate z = ((p - 1) * (q - 1)) / gcd(p - 1, q - 1)
# -calculate d as the inverse modulo of e
# -output the public and private keys
# -decrypt each value from the input using the private key to generate a valid ASCII character
# -rebuild the original message

from sys import stdin, stdout, stderr

# determines if a given number is prime
def isPrime(n):
    if (n % 2 == 0):
        return False

    for i in range(3, int(n ** 0.5 + 1), 2):
        if (n % i == 0):
            return False

    return True

# factors a number n into the product of two primes
def factor(n):
    for i in range(3, int(n ** 0.5 + 1), 2):
        if (n % i == 0) and isPrime(i) and isPrime(n/i):
            return i, int(n / i)

    return None

# recursively returns the greatest common divisor of a and b
def gcd(a, b):
    if (b == 0):
        return a
    
    return gcd(b, a % b)

# naively calculates the inverse modulo of e and z
def naiveInverse(e, z):
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
    
    if t < 0:
        t += z

    return t

# decrypts a ciphertext C with a private key K_priv to get M
def decrypt(C, K_priv):
    return (C ** K_priv[0] % K_priv[1])

# MAIN
# get input
ciphertext = stdin.read().rstrip("\n").split("\n")

# grab the public key and ciphertext values
K_pub = eval(ciphertext[0])
C = ciphertext[1].split(",")

# isolate e and n from the public key
e = K_pub[0]
n = K_pub[1]

# factor n into p and q
p, q = factor(n)

# calculate z
z = int((p - 1) * (q - 1) / gcd(p - 1, q - 1))

# calculate d
d = naiveInverse(e, z)

# generate the private key
K_priv = (d, n)

# implement RSA for the specified input Cs
M = ""
for c in C:
    m = decrypt(int(c), K_priv)
    try:
        M += chr(m)
        stdout.write(chr(m))
        stdout.flush()
    except:
        print("ERROR: Invalid Plaintext")
        break

print