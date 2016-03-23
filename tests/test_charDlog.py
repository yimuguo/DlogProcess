import unittest
from dlogprocess.char.char_dlog import CharDlog
import pandas as pd


class TestCharDlog(unittest.TestCase):
    char = CharDlog(r'../data/Char/vc3s.txt', '25C')

    def test_find_char_table(self):
        self.char.find_char_table()
        with open('test_char_table.txt', 'w+') as wtest:
            for x in self.char.char_table:
                for y in x:
                    wtest.write(y + '\n')
        pass

    def test_re_vc_freq_ln(self):
        test_fmax = self.char.re_vco_freq_ln(' Fmax VCO  for PLL3     1.33 Ghz')
        self.assertEqual(test_fmax.group(3), '1.33')
        self.assertEqual(test_fmax.group(2), 'PLL3')
        self.assertEqual(test_fmax.group(4), 'Ghz')
        test_fmax = self.char.re_vco_freq_ln('  Fmax VCO  PLL1 is  0.92 Ghz')
        self.assertEqual(test_fmax.group(3), '0.92')
        self.assertEqual(test_fmax.group(2), 'PLL1')

    def test_get_vco_max(self):
        vco_table = self.char.get_vco_max()
        self.assertEqual(vco_table[0][0], '3')
        self.assertEqual(vco_table[0][2], 'PLL2')
        self.assertEqual(vco_table[0][3], '1.6')

    # List [VDD, Test, Pin, Data, Load(forDCOnly)]
    def test_parse_table(self):
        smb_data = self.char.parse_table(self.char.char_table[0])
        for x in range(5, len(self.char.char_table[0])):
            if self.char.ln_match_char(self.char.char_table[0][x]):
                test = self.char.char_table[0][x].split()
                for y in range(1, len(test)):
                    self.assertEqual(test[y], smb_data[(x-5)*14+y-1][3])
        # vihvil_data = self.char.parse_table(self.char.char_table[1])
        # for x in range(5, len(self.char.char_table[1])):
        #     if self.char.ln_match_char(self.char.char_table[1][x]):
        #         test = self.char.char_table[1][x].split()
        #         for y in range(1, len(test)):
        #             self.assertEqual(test[y], vihvil_data[(x-5)*14+y-1][3])

    def test_get_test_table(self):
        test_lkg = self.char.get_test_table("OutputLeakage")
        self.assertEqual(test_lkg[0][0], '3.6')
        self.assertEqual(test_lkg[0][3], '-5.4484')

    def test_gen_df(self):
        test_df = self.char.gen_df()
        test_df.to_csv('raw_data.csv')
