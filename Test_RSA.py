import unittest
from RSA import *

class MyTestCase(unittest.TestCase):
    def test_RSA_encrypt(self):
        m = 1234
        e = 3
        p = 3
        q = 7
        N = p * q
        result = encrypt(m, e, N)
        self.assertEqual(pow(m, e, N), result)

    def test_RSA_extended_euc(self):
        p = 11
        q = 5
        n = 55
        phi_n = (p-1) * (q-1)
        e = 7
        gcd, x, y = extended_euclidean(e, phi_n)
        self.assertEqual(1, gcd)
        self.assertEqual(23, x % phi_n)
        self.assertEqual(3, y % phi_n)

    def test_RSA_extended_euc_v2(self):
        p = 11
        q = 5
        phi_n = (p-1) * (q-1)
        e = 7
        gcd, x, y = extended_euclidean_v2(e, phi_n)
        self.assertEqual(1, gcd)
        self.assertEqual(23, x % phi_n)
        self.assertEqual(3, y % phi_n)

    def test_RSA_decrypt(self):
        m = 7
        e = 65537
        p = 11
        q = 3
        N = p * q
        phi_n = (p-1) * (q-1)
        _, d, _ = extended_euclidean_v2(e, phi_n)
        c = encrypt(m, e, N)
        result = decrypt(c, d, N)
        self.assertEqual(m, result)

    def test_RSA_miller_rabin(self):
        rounds = 40
        self.assertEqual(True, miller_rabin(7, rounds))
        self.assertEqual(True, miller_rabin(11, rounds))
        self.assertEqual(False, miller_rabin(8, rounds))
        self.assertEqual(False, miller_rabin(100, rounds))
        self.assertEqual(False, miller_rabin(455555555553543535346346362, rounds))
        self.assertEqual(True, miller_rabin(65537, rounds))
        self.assertEqual(True, miller_rabin(7919, rounds))
        self.assertEqual(True, miller_rabin(5210644015679228794060694325390955853335898483908056458352183851018372555735221, rounds))
        self.assertEqual(True, miller_rabin(6864797660130609714981900799081393217269435300143305409394463459185543183397656052122559640661454554977296311391480858037121987999716643812574028291115057151, rounds))

    def test_RSA_gen_primes(self):
        bits = 1024
        rounds = 40
        prime_list = gen_primes(1024)
        self.assertEqual(1024, prime_list[0].bit_length())
        self.assertEqual(1024, prime_list[1].bit_length())
        self.assertEqual(True, miller_rabin(prime_list[0], rounds))
        self.assertEqual(True, miller_rabin(prime_list[1], rounds))

    def test_RSA_integrated(self):
        print("Running RSA integrated test")

        # Generate primes p and q, each of n/2 bits
        p, q = gen_primes(1024)

        # N has length n bits
        N = p * q

        e = 35537

        # Euler's Totient function. It counts the amount of numbers in Z_N (all numbers between 0 and N-1)
        # where the greatest common divisor with N is 1, in other words gcd(x,N) = 1
        phi_n = (p - 1) * (q - 1)

        print("p = " + str(p))
        print("q = " + str(q))
        print("N = " + str(N))
        print("phi(n) = " + str(phi_n))

        m = 888899990

        print("m = " + str(m))
        print("Encrypting...")


        c = encrypt(m, e, N)

        print("c = " + str(c))

        # Make sure e and phi(n) are relatively prime/coprime otherwise we cannot encrypt/decrypt properly
        self.assertEqual(1, math.gcd(e, phi_n))

        # e * d = 1 mod phi(n)
        # Use extended euclidean algorithm to find d
        _, d, _ = extended_euclidean_v2(e, phi_n)

        print("d = " + str(d))
        print("Decrypting...")

        original_m = decrypt(c, d, N)

        print("m = " + str(original_m))

        self.assertEqual(m, original_m)

    def test_RSA_CRT(self):
        # x = 3 mod 5
        # x = 1 mod 7
        # x = 6 mod 8
        list_n_i = [5, 7, 8]
        list_b_i = [3, 1, 6]
        self.assertEqual(78, CRT(list_n_i, list_b_i))

if __name__ == '__main__':
    unittest.main()
