import unittest

from RSA import gen_user, encrypt, decrypt, gen_users_sameMod
from exploits.common_Modulus import common_Modulus_Attack

class MyTestCase(unittest.TestCase):
    def test_common_Modulus(self):
        n_bits = 1024
        num_users = 2
        e_list = [3, 7]
        m = 342424257628527643859835953645678906546464678995435353533545454
        user_list = gen_users_sameMod(n_bits, num_users, e_list)

        c_1 = encrypt(m, user_list[0].e, user_list[0].N)
        c_2 = encrypt(m, user_list[1].e, user_list[1].N)

        # Perform common modulus attack, given c_1, c_2, e_1, e_2 and N
        result = common_Modulus_Attack(c_1, c_2, user_list[0].e, user_list[1].e, user_list[0].N)

        self.assertEqual(m, result)
        print("Message found: " + str(result))
        print("Common Modulus Attack was Successful")







if __name__ == '__main__':
    unittest.main()
