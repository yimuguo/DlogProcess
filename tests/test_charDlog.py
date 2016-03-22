import unittest
from dlogprocess.char.char_dlog import CharDlog


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

    # List [VDD, Test, Pin, Data, Load(forDCOnly)]
    def test_parse_table(self):
        smb_data = self.char.parse_table(self.char.char_table[0])
        self.assertEqual(smb_data[0][0], '3.6')
        self.assertEqual(smb_data[0][1], 'tBUF')
        self.assertEqual(smb_data[0][3], '0.220')
        self.assertEqual(smb_data[12][3], '0.180')
        self.assertEqual(smb_data[27][0], '2.3')
        self.assertEqual(smb_data[27][3], '0.890')
        for x in range(2, len(self.char.char_table[0])):
            if self.char.ln_match_char(x):
                test = x.split()
                for y in range(1, len(test)):

