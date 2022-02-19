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

    return prime_list


def main():
    p, q = gen_primes(1024)
    N = p * q

if __name__ == "__main__":
    main()
