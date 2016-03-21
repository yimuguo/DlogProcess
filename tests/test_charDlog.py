import unittest
from dlogprocess.char.char_dlog import CharDlog


class TestCharDlog(unittest.TestCase):
    char = CharDlog(r'../data/Char/vc3s.txt', '25C')

    def test_find_char_table(self):
        self.char.find_char_table()
        print(self.char.char_table)
        pass

    def test_re_vc_freq_ln(self):
        test_fmax = self.char.re_vco_freq_ln(' Fmax VCO  for PLL3     1.33 Ghz')
        self.assertEqual(test_fmax.group(3), '1.33')
        self.assertEqual(test_fmax.group(2), 'PLL3')
        self.assertEqual(test_fmax.group(4), 'Ghz')
        test_fmax = self.char.re_vco_freq_ln('  Fmax VCO  PLL1 is  0.92 Ghz')
        self.assertEqual(test_fmax.group(3), '0.92')
        self.assertEqual(test_fmax.group(2), 'PLL1')
