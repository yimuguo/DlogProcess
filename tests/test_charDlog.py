from unittest import TestCase
from dlogprocess.char.char_dlog import CharDlog


class TestCharDlog(TestCase):
    char = CharDlog(r'../data/Char/03122016.txt', '25C')

    def test_find_char_table(self):
        self.char.find_char_table()
        print(self.char.char_table)
        pass

