import math
import secrets

import sympy
from mpmath import *
from sympy import Poly, solveset, GF
from sympy.abc import x
from sympy import monic

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




def common_modulus():
    # Generate primes p and q, each of n/2 bits
    p, q = gen_primes(1024)

    # N has length n bits
    N = p * q

    e_Alice = 3
    e_Bob = 7

    # gcd(e_Alice, e_Bob) = 1
    # e_Alice * s_1 + e_Bob * s_2 = 1

    _, s_1, s_2 = extended_euclidean_v2(e_Alice, e_Bob)

    m = 1234567890
    c_Alice = encrypt(m, e_Alice, N)
    c_Bob = encrypt(m, e_Bob, N)

    # (c_Alice ^ s_1) * (c_Bob ^ s_2) = ((m^e_Alice)^s_1) * ((m^e_Bob)^s_2) = m^(e_Alice * s_1 + e_Bob * s_2) = m
    constructed_m = pow(c_Alice, s_1) * pow(c_Bob, s_2)
    print(int(constructed_m))


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


def Hastad_BC_Attack():
    m = 1337

    # Party 1
    # Generate primes p and q, each of n/2 bits
    p, q = gen_primes(1024)
    n_1 = p * q
    e_party1 = 3
    c_1 = encrypt(m, e_party1, n_1)

    # Party 2
    # Generate primes p and q, each of n/2 bits
    p, q = gen_primes(1024)
    n_2 = p * q
    e_party2 = 3
    c_2 = encrypt(m, e_party2, n_2)

    # Party 3
    # Generate primes p and q, each of n/2 bits
    p, q = gen_primes(1024)
    n_3 = p * q
    e_party3 = 3
    c_3 = encrypt(m, e_party3, n_3)

    # c_1 = m^3 mod N_1
    # c_2 = m^3 mod N_2
    # c_3 = m^3 mod N_3

    # Assume gcd(N_i, N_j) not equal to 1, otherwise factorization is possible
    list_n_i = [n_1, n_2, n_3]
    list_c_i = [c_1, c_2, c_3]

    # Use CRT to determine m^3
    result = CRT(list_n_i, list_c_i)
    print(int(round(result**mpf(1/3))))







def main():
    #common_modulus()
    #Hastad_BC_Attack()
    #CRT_Test()



    #g = Poly(6*x**4 + x, x, modulus=5)
    #print(g+g)

    #print(monic(3*x**2 + 4*x + 2))

    from sympy import roots
    from sympy import solve
    from sympy import symbols
    from sympy import latex

    #x, y = symbols('x y')
    #print(solve(x**2+x, x))




    m = 1337

    # Party 1
    # Generate primes p and q, each of n/2 bits
    p, q = gen_primes(1024)
    n_1 = p * q
    e_party1 = 3

    a_1 = 1
    b_1 = 2

    # Apply padding m_i = a_i * m + b_i
    m_1 = a_1 * m + b_1

    c_1 = encrypt(m_1, e_party1, n_1)


    # Party 2
    # Generate primes p and q, each of n/2 bits
    p, q = gen_primes(1024)
    n_2 = p * q
    e_party2 = 3

    a_2 = 2
    b_2 = 3

    m_2 = a_2 * m + b_2

    c_2 = encrypt(m_2, e_party2, n_2)

    # Party 3
    # Generate primes p and q, each of n/2 bits
    p, q = gen_primes(1024)
    n_3 = p * q
    e_party3 = 3

    a_3 = 3
    b_3 = 4

    m_3 = a_3 * m + b_3

    c_3 = encrypt(m_3, e_party3, n_3)


    # T_i = 1 (mod n_i)
    # T_i = 0 (mod n_j!=i)

    list_n1 = [n_1, n_2, n_3]
    T_1 = CRT(list_n1, [1, 0, 0])

    list_n2 = [n_2, n_1, n_3]
    T_2 = CRT(list_n2, [1, 0, 0])

    list_n3 = [n_3, n_1, n_2]
    T_3 = CRT(list_n3, [1, 0, 0])

    # Construct polynomial g
    g_1 = Poly(T_1 * ((a_1 * x + b_1)**3 - c_1), x, modulus=n_1 * n_2 * n_3)
    g_2 = Poly(T_2 * ((a_2 * x + b_2)**3 - c_2), x, modulus=n_1 * n_2 * n_3)
    g_3 = Poly(T_3 * ((a_3 * x + b_3)**3 - c_3), x, modulus=n_1 * n_2 * n_3)

    g = g_1 + g_2 + g_3

    print(g)
    g = g.monic()
    print(g)
    print(g.all_coeffs())
    print(g(1337))
    """"
    for i in range(n_1):
        if (g(i) == 0):
            print(i)
            break

    """



















if __name__ == "__main__":
    main()
