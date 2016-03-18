from unittest import TestCase
from dlogprocess.dlogprocess import Dlog


class TestDlog(TestCase):
    test_dlog = Dlog('../data/Char/03122016.txt')

    def test_get_test_details(self):
        test_lst = self.test_dlog.filter_test_details('OutputLeakage')
        self.assertEqual(test_lst[0][0], 'DIFF1')
        self.assertEqual(test_lst[8][2], '57.1023')
