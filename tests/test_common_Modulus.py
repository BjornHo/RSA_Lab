import unittest

from RSA import gen_user, encrypt, decrypt, gen_users_sameMod
from exploits.common_Modulus import common_Modulus_Attack

class MyTestCase(unittest.TestCase):
    def test_common_Modulus(self):
        n_bits = 1024
        num_users = 2
        e_list = [3, 7]
        m = 3424242576285276438598359536456789065464646789954353535335
        user_list = gen_users_sameMod(n_bits, num_users, e_list)

        c_1 = encrypt(m, user_list[0].e, user_list[0].N)
        c_2 = encrypt(m, user_list[1].e, user_list[1].N)

        print(decrypt(c_2, user_list[1].d, user_list[1].N))

        print(common_Modulus_Attack(c_1, c_2, user_list[0].e, user_list[1].e, user_list[0].N))
        








if __name__ == '__main__':
    unittest.main()
