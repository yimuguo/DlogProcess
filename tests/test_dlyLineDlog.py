from unittest import TestCase
from dlogprocess.char.delay_char import DlyLineDlog


class TestDlyLineDlog(TestCase):
    dly = DlyLineDlog(".\\data\\Delay_line\\rising_edge.txt")

    def test_get_dly_range1(self):
        self.dly.get_dly_val()
        print(self.dly.dly_range1[0])
        self.assertEqual(self.dly.dly_range1[0][1], 1.9500)
        self.assertEqual(self.dly.dly_range1[20][5], 3.9800)
        self.assertEqual(len(self.dly.dly_range1[20]), 10)
        self.assertEqual(len(self.dly.dly_range1[0]), 10)

    def test_get_dly_range2(self):
        self.dly.get_dly_val()
        self.assertEqual(len(self.dly.dly_range2[0]), 10)
        self.assertEqual(self.dly.dly_range2[0][1], 3.9000)
        self.assertEqual(self.dly.dly_range2[30][9], 9.940)

    def test_get_dly_range3(self):
        self.dly.get_dly_val()
        self.assertEqual(len(self.dly.dly_range3[0]), 10)
        self.assertEqual(self.dly.dly_range3[0][1], 10.016)
        self.assertEqual(self.dly.dly_range3[49][9], 19.880)
