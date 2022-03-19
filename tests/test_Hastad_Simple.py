import unittest
from RSA import *
from exploits.Hastad_Simple import Hastad_BCA_Simple


class MyTestCase(unittest.TestCase):
    def test_Hastad_Simple(self):
        user_list = []
        ciphertext_list = []
        modulus_list = []
        e = 3
        num_users = 3
        message = 1053453435454335435435435425245255210534534354543354354354354252452552105345343545433543543543542525454335435434354354252452552105345343545433543543543542524525525255210534534354543354354354354252452552105345343545433543543543542524525525255210352525252532542624653626262525252525325
        # Generate users
        for _ in range(num_users):
            user_i = gen_user(1024, e)
            user_list.append(user_i)
            print(user_i.N)

        # Encrypt for all recipients and gather modulus
        for user_i in user_list:
            ciphertext = encrypt(message, user_i.e, user_i.N)
            ciphertext_list.append(ciphertext)
            modulus_list.append(user_i.N)

        print("Message: " + str(message) + " is encrypted for all receivers")
        start_time_do_attack = time.time()
        result = Hastad_BCA_Simple(ciphertext_list, modulus_list, e)
        end_time_do_attack = time.time()
        self.assertEqual(message, result)
        print("Message found: " + str(result))
        print("Hastad BCA Simple was successful")
        print("Time elapsed to find message: " + str(end_time_do_attack - start_time_do_attack) + " seconds")

if __name__ == '__main__':
    unittest.main()
