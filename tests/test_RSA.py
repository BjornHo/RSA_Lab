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

    def test_RSA_gen_party(self):
        print("Running test_RSA_gen_party")
        print("------------------")
        bits = 1024
        e = 3
        party_1 = gen_Party(bits, e)
        message = 4584848489
        c = encrypt(message, party_1.e, party_1.N)
        self.assertEqual(message, decrypt(c, party_1.d, party_1.N))
        print("------------------")

    def test_RSA_integrated(self):
        print("Running RSA integrated test")
        print("------------------")

        bits = 1024
        e = 65537
        message = 99887766

        print("Party 1")
        print("Using " + str(bits) + " bits for p and q")
        print("e = " + str(e))

        party_1 = gen_Party(bits, e)
        print("d = " + str(party_1.d))
        print("message = " + str(message))

        print("Encrypting message " + str(message))
        c = encrypt(message, party_1.e, party_1.N)

        print("Ciphertext = " + str(c))
        decrypted_m = decrypt(c, party_1.d, party_1.N)

        print("Decrypted text = " + str(decrypted_m))

        self.assertEqual(message, decrypted_m)

    def test_RSA_CRT(self):
        # x = 3 mod 5
        # x = 1 mod 7
        # x = 6 mod 8
        list_n_i = [5, 7, 8]
        list_b_i = [3, 1, 6]
        self.assertEqual(78, CRT(list_n_i, list_b_i))

if __name__ == '__main__':
    unittest.main()
