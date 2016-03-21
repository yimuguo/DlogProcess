from unittest import TestCase
from dlogprocess.dlogprocess import Dlog
import re


def test_vdd_comment(self):
    test_vdd = []
    re_test_comment = re.compile(r'VDD[A-Z0-9]*\s*=\s*(\d*\.\d+|\d+)')
    for x in self.test_dlog.dlog_data:
        if re_test_comment.search(x):
            test_vdd.append(x)
    print(test_vdd)


class TestDlog(TestCase):
    test_dlog = Dlog('../data/Char/vc3s.txt')

    def test_get_test_details(self):
        test_lst = self.test_dlog.filter_test_details('OutputLeakage')
        self.assertEqual(test_lst[0][4], 'DIFF1')
        self.assertEqual(test_lst[8][8], '55.4343')
        self.assertEqual(test_lst[2][14], '3.6')
        self.assertEqual(test_lst[9][14], '3.6')

