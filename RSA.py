import math
import secrets
import time

# A user that is participating in the RSA game
# (e,N) is the public key pair
# d is the private key
class user:
    def __init__(self, e, d, N):
        self.e = e
        self.d = d
        self.N = N

# Miller Rabin Primality test
# n = prime candidate
# k = number of rounds
# Returns true if probably prime, false for composite number
def miller_rabin(n, k):
    if n == 1 or n == 2 or n == 3:
        return True

    # False if it is an even number
    if n % 2 == 0:
        return False

    # We need the following equation
    # n-1 = 2^r * d
    # (n-1) / 2^r = d with d as non integer
    # Start with r = 0.
    # We want to keep raising r by 1, until we get a non integer at d
    # We can execute this idea very efficiently by bit shifting (n-1) by 1 to the right
    # Of course we have to keep count of r, which will be the amount of bit shifts we have done
    # Without this optimization, the test took too long...
    r = 0
    z = n - 1
    while z % 2 == 0:
        z >>= 1
        r += 1

    d = z

    # Loop which we repeat k times, also called "witness loop"
    for _ in range(k):
        # Pick random integer 2 <= a <= n-2
        a = secrets.randbelow(n - 1)
        if a < 2:
            a = 2

        # x = a^d mod n
        x = pow(a, d, n)
        if x == 1 or x == (n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


# Generates two prime numbers, each of n_bits length
def gen_primes(n_bits):
    prime_counter = 2
    prime_list = []

    # Generate pseudo random numbers and test for primality
    while prime_counter > 0:
        prime_candidate = secrets.randbits(n_bits)
        # Make sure the bit length is correct, if not start from beginning of the while loop
        if prime_candidate.bit_length() != n_bits:
            continue

        # Test primality
        if miller_rabin(prime_candidate, 40):
            prime_counter -= 1
            prime_list.append(prime_candidate)

        # Make sure we have 2 * n_bits as total bit length
        if len(prime_list) == 2:
            N = prime_list[0] * prime_list[1]
            if N.bit_length() != 2 * n_bits:
                prime_counter = 2
                prime_list = []
                # Mission failed, search for two new primes
                continue
    return prime_list

def gen_user(n_bits, e):
    print("-------------------")
    print("Generating user")

    # Start measuring time
    start_time = time.time()

    # Generate primes p and q, each of n/2 bits
    p, q = gen_primes(int(n_bits/2))

    # N has length n bits
    N = p * q

    # Euler's Totient function. It counts the amount of numbers in Z_N (all numbers between 0 and N-1)
    # where the greatest common divisor with N is 1, in other words gcd(x,N) = 1
    phi_n = (p-1) * (q-1)

    # Make sure e and phi(n) are relatively prime/coprime otherwise we cannot encrypt/decrypt properly
    while math.gcd(e, phi_n) != 1:
        #print("gcd(e, phi_n) was not 1, trying again")
        p, q = gen_primes(int(n_bits/2))
        phi_n = (p-1) * (q-1)
        N = p * q
    # print("Found matching primes, problem solved")

    # e * d = 1 mod phi(n)
    # Use extended euclidean algorithm to find d
    _, d, _ = extended_euclidean_v2(e, phi_n)

    print("User generated")
    print("p = " + str(p))
    print("q = " + str(q))
    print("N = " +str(N))
    print("d = " + str(d))

    # End measuring time
    end_time = time.time()

    print("Time elapsed: " + str(end_time - start_time) + " seconds")

    user_x = user(e, d, N)
    return user_x

# Checks if all elements in list_e and phi_n are coprime
# Helper to create users for common modulus attack
def are_coprime(e_list, phi_n):
    for current_e in e_list:
        if math.gcd(current_e, phi_n) != 1:
            return False
    return True

# We want users with the same P and Q to get the same modulus
# This is for the common modulus attack
def gen_users_sameMod(n_bits, number_users, e_list):
    # print("-------------------")
    # print("Generating users with same modulus")
    # Generate primes p and q, each of n/2 bits
    p, q = gen_primes(int(n_bits/2))

    # N has length n bits
    N = p * q

    # Euler's Totient function. It counts the amount of numbers in Z_N (all numbers between 0 and N-1)
    # where the greatest common divisor with N is 1, in other words gcd(x,N) = 1
    phi_n = (p-1) * (q-1)

    # Make sure e and phi(n) are relatively prime/coprime otherwise we cannot encrypt/decrypt properly
    # Small change from gen_user is that all in e_list should have this property
    while not are_coprime(e_list, phi_n):
        # print("gcd(e, phi_n) was not 1, trying again")
        p, q = gen_primes(int(n_bits/2))
        N = p * q
        phi_n = (p-1) * (q-1)

    # print("Found matching primes, problem solved")

    user_list = []

    # Create users with same Modulus
    for i in range(number_users):
        # e * d = 1 mod phi(n)
        # Use extended euclidean algorithm to find d_i
        _, d_i, _ = extended_euclidean_v2(e_list[i], phi_n)
        user_i = user(e_list[i], d_i, N)
        user_list.append(user_i)
        # print("-------------")
        # print("User " + str(i) + " created")
        # print("e = " + str(user_i.e))
        # print("d = " + str(user_i.d))
        # print("N = " + str(user_i.N))

    return user_list

def encrypt(message, e, N):
    ciphertext = pow(message, e, N)
    return ciphertext

def decrypt(ciphertext, d, N):
    message = pow(ciphertext, d, N)
    return message

# Recursive extended euclidean algorithm
# Returns (d,x,y) such that d=gcd(a,b) and d=x * a + y * b
def extended_euclidean(a, b):
    # Base case
    # since a is 0, we know d, x and y
    if a == 0:
        # Returns d, x, y
        return b, 0, 1
    else:
        # We keep calling until we reach the base case
        # Same idea like the normal euclidean algorithm, write b in terms of a
        # b = (b // a) * a + (b % a)
        gcd, x1, y1 = extended_euclidean(b % a, a)

        # Base case triggered, now moving backwards
        # (b % a) = b - (b // a) * a
        # x1 * (b % a ) + y1 * a
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

# Iterative approach
# Returns (d,x,y) such that d=gcd(a,b) and d=x * a + y * b
def extended_euclidean_v2(a, b):
    previous_x = 1
    x = 0
    previous_y = 0
    y = 1

    # b > 0
    while b:
        q = a//b
        # Saving the previous x and y coefficients
        # Python evaluates right side fully before assigning the values to the left
        x, previous_x = previous_x - q * x, x
        y, previous_y = previous_y - q * y, y

        # GCD
        a, b = b, a % b
    return a, previous_x, previous_y

# Chinese Remainder Theorem
# x = b_1 mod n_1
# x = b_2 mod n_2
# x = b_i mod n_i etc.
# Find x.
def CRT(list_n_i, list_b_i):
    # Calculate N which is the product of all elements in list_n_i
    N = 1
    for element in list_n_i:
        N *= element

    # Calculate N_i = N/n_i
    list_N_i = []
    for n_i in list_n_i:
        list_N_i.append(N//n_i)

    # Calculate x_i, which is the inverse of N_i
    list_x_i = []
    j = 0
    for N_i in list_N_i:
        gcd, x_i, _ = extended_euclidean_v2(N_i, list_n_i[j])
        if gcd != 1:
            raise ValueError("There was a problem, the input " + str(N_i) + "," + str(list_n_i[j]) + " was not coprime")
        list_x_i.append(x_i)
        j += 1

    # Calculate x = sum (b_i * N_i * x_i) mod N
    x = 0
    for k in range(len(list_n_i)):
        x += list_b_i[k] * list_N_i[k] * list_x_i[k]

    return x % N
