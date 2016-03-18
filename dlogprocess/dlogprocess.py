#!/usr/bin/python
import re
import os
__author__ = 'Eamul'


class Dlog(object):

    dlog_data_site0 = []
    dlog_data_site1 = []
    dlog_data_site2 = []
    dlog_data_site3 = []

    def __init__(self, dlog_path, lotnumber='TT', temp='25C'):
        with open(dlog_path, 'r') as data:
            self.dlog_data = data.read().splitlines()
        self.lotnumber = lotnumber
        self.temp = temp

    def define_site(self, site):
        if site == 0:
            self.dlog_data = self.dlog_data_site0
        elif site == 1:
            self.dlog_data = self.dlog_data_site1
        elif site == 2:
            self.dlog_data = self.dlog_data_site2
        elif site == 3:
            self.dlog_data = self.dlog_data_site3
        else:
            os.error("SITE NOT ACTIVE")

    def screen_pass(self, write_to_file=1):
        data_buffer = []
        pass_dlog = []
        new_device = 0
        for line in range(0, len(self.dlog_data)):
            if "Device#:" in self.dlog_data[line]:
                new_device = 1
            if new_device == 1:
                data_buffer.append(self.dlog_data[line])
            if self.dlog_data[line][:73] == '=========================================================================':
                new_device = 0
                if self.dlog_data[line-1][14:25] == '1         1':
                    # for x in data_buffer:
                    pass_dlog.extend(data_buffer)
                data_buffer = []
        if write_to_file == 1:
            pass_dlog_txt = open('PassUnits_%s.txt' % self.lotnumber, 'w+')
            pass_dlog_txt.writelines(["%s\n" % item for item in pass_dlog])
            pass_dlog_txt.close()
        return pass_dlog

    def get_test_limit(self, keyword, tp_txt):
        test = filter(lambda search_for: keyword in search_for, self.dlog_data)
        split_data = []
        for x in test:
            x = re.split("\s+", x)
            split_data.append(x)
        tmin = []
        tmax = []
        for x in split_data:
            if x[2] == '0' and len(x) > 12:
                if x[4] != ('OutputLeakage' or 'InputLeakage') and (x[8] == 'uA' or x[8] == 'mV'):
                    x[7] = str(float(x[7])/1000)
                tmin.append(x[7])
                if x[4] != ('OutputLeakage' or 'InputLeakage') and (x[12] == 'uA' or x[12] == 'mV'):
                    x[11] = str(float(x[11])/1000)
                tmax.append(x[11])
            elif len(x) <= 17:
                tmin.append('')
                tmax.append('')
        del re
        i = 0
        for x in range(0, len(tmin)):
            if not (tmin[i] == tmin[i-1] and tmax[i] == tmax[i-1]):
                tp_txt.write(tmin[i]+'\t'+tmax[i]+'\n')
            i += 1

    def filter_keyword(self, identifier, col, rows=1, offset=0):
        filtered_lst = []
        for line in range(0, len(self.dlog_data)):
            if identifier in self.dlog_data[line]:
                for row in range(0, rows):
                    target_line = re.split("\s+", self.dlog_data[line + row + offset])
                    filtered_lst.append(target_line[col])
        return filtered_lst
