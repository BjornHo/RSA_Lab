import unittest
from RSA import *
from exploits.Hastad_Simple import Hastad_BC_Simple


class MyTestCase(unittest.TestCase):
    def test_Hastad_Simple(self):
        user_list = []
        ciphertext_list = []
        modulus_list = []
        e = 3
        message = 10534534354543354354354354252452552

        # Generate 3 users
        for _ in range(3):
            user_i = gen_user(1024, e)
            user_list.append(user_i)

        # Encrypt for 3 recipients and gather modulus
        for user_i in user_list:
            ciphertext = encrypt(message, user_i.e, user_i.N)
            ciphertext_list.append(ciphertext)
            modulus_list.append(user_i.N)

        print("Message: " + str(message) + " is encrypted for all receivers")
        result = Hastad_BC_Simple(ciphertext_list, modulus_list, e)
        self.assertEqual(message, result)
        print("Message found: " + str(result))
        print("Hastad BCA Simple was successful")

if __name__ == '__main__':
    unittest.main()
