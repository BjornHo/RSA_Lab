#! /usr/bin/sage -python

import os
import sys
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import unittest
from RSA import *
from exploits.Hastad import Hastad_BCA
from sage.all import *


class MyTestCase(unittest.TestCase):

    def test_Hastad_BCA(self):
        # Start measuring time
        start_time_setup = time.time()

        # Public linear padding function
        #f(a_i,m,b_i) = a_i * m + b_i
        __tmp__=var("a_i,m_i,b_i");f = symbolic_expression(a_i * m_i + b_i).function(a_i,m_i,b_i)

        user_list = []
        a_list = []
        b_list = []
        n_list = []
        c_list = []
        e_list = []

        # Message can be adjusted, note that for increasing the message or num_users the epsilon
        # in small_roots function in Hastad.py might have to be adjusted to find the message.
        message = 1337
        num_users = 4

        # This is a list of e values that can be used as public exponent, can be adjusted.
        selection_e = [3]

        print("Plaintext message is: ", message)

        # Generate users
        for index in range(num_users):
            user_i = gen_user(1024, secrets.choice(selection_e))
            user_list.append(user_i)
            e_list.append(user_i.e)

        # Generate random padding for each user
        for index in range(len(user_list)):
            a = 0
            b = 0

            # Prevent using zero
            while a == 0 or b == 0:
                a = secrets.randbelow(user_list[index].N)
                b = secrets.randbelow(user_list[index].N)

            # Add to the lists
            a_list.append(a)
            b_list.append(b)

        # Gather modulus of each user
        for user_i in user_list:
            n_list.append(user_i.N)

        # Pad message first and then encrypt message for each user
        i = 0
        for user_i in user_list:
            # Use the linear padding function and pad the message
            padded_message = int(f(a_list[i], message, b_list[i]))
            print("----------------")
            print("User: " + str(i))
            print("Padded msg is: " + str(padded_message))
            print("Encrypting with e = ", user_i.e)
            c = encrypt(padded_message, user_i.e, user_i.N)
            c_list.append(c)
            i += 1

        # End measuring time
        end_time_setup = time.time()

        # Start measuring time
        start_time_attack = time.time()

        # Pass on list of a, b, ciphertexts of each user and modulus of each user and public exponent of each user
        # And perform the Hastad Broadcast Attack
        print()
        print("Starting attack...")
        result = Hastad_BCA(a_list, b_list, c_list, n_list, e_list)

        self.assertEqual(message, result)

        # End measuring time
        end_time_attack = time.time()
        print()
        print("Time elapsed for setup: " + str(end_time_setup - start_time_setup) + " seconds")

        # Time elapsed for attack itself
        elapsed_time = end_time_attack - start_time_attack
        print("Time elapsed for attack itself: " + str(elapsed_time) + " seconds")
        print("Hastad Broadcast Attack Successful")
        print("The secret message is: " + str(result))

        # Returning time, useful for experiments call to run this repeatedly
        return elapsed_time

if __name__ == '__main__':
    unittest.main()
