__author__ = 'Eame'


import os
import re


class Dlog(object):

    dlog_data = []
    lot_number = 'TT'

    def read_dlog(self, dlog_path):
        with open(dlog_path, 'r') as data:
            self.dlog_data = data.read().splitlines()

    def screen_pass(self):
        data_buffer = []
        pass_dlog = open('PassUnits_%s.txt' % self.lot_number, 'w+')
        new_device = 0
        for line in range(0, len(self.dlog_data)):
            if "Device#:" in self.dlog_data[line]:
                new_device = 1
            if new_device == 1:
                data_buffer.append(self.dlog_data[line])
            if self.dlog_data[line][:73] == '=========================================================================':
                new_device = 0
                if self.dlog_data[line-1][14:25] == '1         1':
                    pass_dlog.writelines(["%s\n" % item for item in data_buffer])
                data_buffer = []
        pass_dlog.close()
