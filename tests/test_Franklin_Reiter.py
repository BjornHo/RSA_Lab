import os,sys,inspect
import secrets

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from RSA import *
from sage.all import *
from exploits.Franklin_Reiter import Franklin_Reiter_Attack
import unittest


class MyTestCase(unittest.TestCase):
    def test_Franklin_Reiter(self):

        # Generate users with the same modulus
        n_bits = 1024
        num_users = 2
        e_list = [3, 3]
        user_list = gen_users_sameMod(n_bits, num_users, e_list)

        # Modulus
        N = user_list[0].N

        # Let m_1 != m_2
        # m_1 = f(m_2) mod N , for  f = a * x + b in Z_n[x] with b != 0
        # From my test I saw that a > 0, otherwise the gcd later on is not linear...

        m_2 = 1337
        a = 0
        b = 0

        while a == 0 or b == 0:
            a = secrets.randbelow(N)
            b = secrets.randbelow(N)

        print()
        print("a = " + str(a))
        print("b = " + str(b))

        # Create polynomial ring Z mod N
        # R.<x> = Zmod(N)[]
        R = Zmod(N)['x']; (x,) = R._first_ngens(1)

        #f(x) = a * x + b
        print()
        f = a * x + b
        print("f(x) = " + str(f))

        # Use int(f(m_2)) to prevent segmentation fault. Sage and Python conversion
        # c_1 = (m_1)^e mod N = f(m_2)^e mod N
        c_1 = encrypt(int(f(m_2)), user_list[0].e, N)
        c_2 = encrypt(m_2, user_list[1].e, N)

        # Execute the attack
        result = Franklin_Reiter_Attack(c_1, c_2, user_list[0].e, user_list[1].e, f, N)

        self.assertEqual(m_2, result)
        print()
        print("Franklin-Reiter Related Message Attack successful")
        print("The message m_2 was: " + str(m_2))














if __name__ == '__main__':
    unittest.main()
