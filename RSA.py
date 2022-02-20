import math
import secrets


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


e = 35537


def encrypt(message, N):
    b = bytearray()
    b.extend(map(ord, message))
    big_int = int.from_bytes(b, "big")
    ciphertext = pow(big_int, e, N)
    return ciphertext, len(b)


def decrypt(ciphertext, b, d, N):
    message = pow(ciphertext, d, N)
    bytes_val = message.to_bytes(b, "big")
    original_m = bytes_val.decode()
    return original_m


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
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y


def main():
    # Generate primes p and q, each of n/2 bits
    p, q = gen_primes(1024)

    # N has length n bits
    N = p * q

    # Euler's Totient function. It counts the amount of numbers in Z_N (all numbers between 0 and N-1)
    # where the greatest common divisor with N is 1, in other words gcd(x,N) = 1
    phi_n = (p - 1) * (q - 1)

    c, b = encrypt("Hello World!", N)

    # Make sure e and phi(n) are relatively prime/coprime otherwise we cannot encrypt/decrypt properly
    assert math.gcd(e, phi_n) == 1

    # e * d = 1 mod phi(n)
    # Use extended euclidean algorithm to find d
    _, d, _ = extended_euclidean(e, phi_n)

    print(decrypt(c, b, d, N))




if __name__ == "__main__":
    main()
