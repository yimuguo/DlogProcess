import re
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from dlogprocess import Dlog


class DlyLineDlog(Dlog):
    dly_range1 = []
    dly_range2 = []
    dly_range3 = []

    def __init__(self, dlogpath):
        super(DlyLineDlog, self).__init__(dlogpath)
        self.dlog_data = self.screen_pass(write_to_file=0)

    def get_dly_val(self):
        for x in range(2000, 4100, 100):
            dly_val = self.filter_keyword("Delay= %d(us). " % x, 2, 10, offset=4)
            dly_val = [float(i) for i in dly_val]
            self.dly_range1.append(dly_val)
        for x in range(4000, 10200, 200):
            dly_val = self.filter_keyword("Delay = %d(us). " % x, 2, 10, offset=4)
            dly_val = [float(i) for i in dly_val]
            self.dly_range2.append(dly_val)
        for x in range(10200, 20200, 200):
            dly_val = self.filter_keyword("Delay = %d(us). " % x, 2, 10, offset=4)
            dly_val = [float(i) for i in dly_val]
            self.dly_range3.append(dly_val)

    def process_val(self):
        df = pd.DataFrame(self.dly_range1, [x for x in range(2000, 4100, 100)])
        print(df.head())