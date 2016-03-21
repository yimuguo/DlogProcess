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

    def screen_pass(self):
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
        re_test_inst = re.compile(
            r' \d+\s+\d\s+(:?PASS|FALL)\s+[A-Za-z0-9_]+\s+[A-Za-z0-9_]+\s+\d+\s+[-+]?\d+\.\d+ [a-zA-Z]+')
        re_test_comment = re.compile(r'VDD[A-Za-z0-9]*\s*=\s*(\d*\.\d+|\d+)')
        # filtered = filter(test_line.match, self.dlog_data)
        test_ln = []
        # new_inst = ''
        vdd_val = 'Unknown'
        line = 0
        while line < len(self.dlog_data):
            if re_test_comment.search(self.dlog_data[line]):
                vdd_val = re_test_comment.search(self.dlog_data[line]).group(1)
                line += 1
                continue
            if re_test_inst.match(self.dlog_data[line]):
                # if re_test_comment.search(self.dlog_data[line-1]):
                #     vdd_val = re_test_comment.search(self.dlog_data[line-1]).group(1)
                #     split_test = []
                #     i = 0
                #     while re_test_inst.match(self.dlog_data[line+i]):
                #         split_test = re.split('\s+', self.dlog_data[line+i])
                #         split_test = split_test[1:-2]
                #         split_test.append(vdd_val)
                #         test_ln.append(split_test)
                # i += 1
                # new_inst = split_test[3]
                # line += i
                # continue
                split_test = re.split('\s+', self.dlog_data[line])
                split_test = split_test[1:-2]
                # if split_test[3] == new_inst:
                split_test.append(vdd_val)
                test_ln.append(split_test)
            line += 1
        return test_ln

    def filter_test_details(self, test_name):
        test_details = self.get_test_pf()
        filtered = []
        for test_instance in test_details:
            if test_instance[3] == test_name:
                # return list format: [Pin name, min, measured, max, unit, force, force unit]
                filtered.append(test_instance)
        return filtered

    def filter_keyword(self, identifier, col, rows=1, offset=0):
        filtered_lst = []
        for line in range(0, len(self.dlog_data)):
            if identifier in self.dlog_data[line]:
                for row in range(0, rows):
                    target_line = re.split("\s+", self.dlog_data[line + row + offset])
                    filtered_lst.append(target_line[col])
        return filtered_lst
