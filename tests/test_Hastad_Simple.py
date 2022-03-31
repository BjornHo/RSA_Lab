#! /usr/bin/sage -python

import os
import sys
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

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
        message = 1337

        # Generate users
        for _ in range(num_users):
            user_i = gen_user(1024, e)
            user_list.append(user_i)

        # Encrypt for all recipients and gather modulus
        for user_i in user_list:
            ciphertext = encrypt(message, user_i.e, user_i.N)
            ciphertext_list.append(ciphertext)
            modulus_list.append(user_i.N)

        print()
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
