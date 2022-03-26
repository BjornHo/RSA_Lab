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

        # Generate user
        n_bits = 1024
        e = 65537
        user = gen_user(n_bits, e)

        # Modulus
        N = user.N

        # Let m_1 != m_2
        # m_1 = f(m_2) mod N , for  f = a * x + b in Z_n[x] with b != 0
        # From my test I saw that a > 0, otherwise the gcd later on is not linear...

        m_2 = 1337
        a = 0
        b = 0

        while a == 0 or b == 0:
            a = secrets.randbelow(N)
            b = secrets.randbelow(N)

        # print()
        # print("a = " + str(a))
        # print("b = " + str(b))

        # Create polynomial ring Z mod N
        # R.<x> = Zmod(N)[]
        R = Zmod(N)['x']; (x,) = R._first_ngens(1)

        #f(x) = a * x + b

        # print()
        f = a * x + b
        # print("f(x) = " + str(f))

        # Use int(f(m_2)) to prevent segmentation fault. Sage and Python conversion
        # c_1 = (m_1)^e mod N = f(m_2)^e mod N
        c_1 = encrypt(int(f(m_2)), e, N)
        c_2 = encrypt(m_2, e, N)

        # Start measuring time
        start_time_attack = time.time()

        # Execute the attack
        result = Franklin_Reiter_Attack(c_1, c_2, e, f, N)

        # End measuring time
        end_time_attack = time.time()

        time_elapsed = end_time_attack - start_time_attack

        print(time_elapsed)
        self.assertEqual(m_2, result)
        # print()
        # print("Franklin-Reiter Related Message Attack successful")
        # print("The message m_2 was: " + str(m_2))

        return time_elapsed














if __name__ == '__main__':
    unittest.main()
