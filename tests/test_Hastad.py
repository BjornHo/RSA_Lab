#! /usr/bin/sage -python


import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import unittest
from RSA import *
from exploits import Hastad
from sage.all import *

import random

class MyTestCase(unittest.TestCase):

    def test_Hastad_BCA(self):
        # Linear padding function
        #f(a_i,m,b_i) = a_i * m + b_i
        __tmp__=var("a_i,m_i,b_i");f = symbolic_expression(a_i * m_i + b_i).function(a_i,m_i,b_i)

        user_list = []
        a_list = []
        b_list = []
        n_list = []
        c_list = []

        e = 3
        message = 1337

        # Generate 3 users
        for _ in range(3):
            user_i = gen_user(1024, e)
            user_list.append(user_i)

        # Generate random padding for each user
        for _ in range(len(user_list)):
            a = random.randint(0, 100)
            b = random.randint(0, 100)
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
            print("Encrypting...")
            c = encrypt(padded_message, e, user_i.N)
            c_list.append(c)
            i += 1





if __name__ == '__main__':
    unittest.main()
