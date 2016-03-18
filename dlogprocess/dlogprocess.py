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
        return pass_dlog

    def get_test_pf(self):
        test_line = re.compile(r' \d+\s+\d\s+(:?PASS|FALL)\s+[A-Za-z0-9_]+\s+[A-Za-z0-9_]+\s+\d+\s+[-+]\d+\.\d+ [a-zA-Z]+')
        filtered = filter(test_line.match, self.dlog_data)
        return filtered

    def filter_test_details(self, test_name):
        split_data = []
        filtered = self.get_test_pf()
        test_details = []
        for x in filtered:
            x = re.split("\s+", x)
            del x[0]
            split_data.append(x)
        for test_instance in split_data:
            if test_instance[3] == test_name:
                # return list format: [Pinname, min, measured, max, unit, force, force unit]
                test_details.append([test_instance[4], test_instance[6], test_instance[8], test_instance[10],
                                     test_instance[11], test_instance[12], test_instance[13]])
        return test_details

    def filter_keyword(self, identifier, col, rows=1, offset=0):
        filtered_lst = []
        for line in range(0, len(self.dlog_data)):
            if identifier in self.dlog_data[line]:
                for row in range(0, rows):
                    target_line = re.split("\s+", self.dlog_data[line + row + offset])
                    filtered_lst.append(target_line[col])
        return filtered_lst
