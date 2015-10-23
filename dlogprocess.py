#!/usr/bin/python
import re
import os
__author__ = 'Eame'


class Dlog(object):

    dlog_data = []
    # lot_number = 'TT'

    def read_dlog(self, dlog_path):
        with open(dlog_path, 'r') as data:
            self.dlog_data = data.read().splitlines()

    def screen_pass(self, lot_number='TT', write_to_file=1):
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
            pass_dlog_txt = open('PassUnits_%s.txt' % lot_number, 'w+')
            pass_dlog_txt.writelines(["%s\n" % item for item in pass_dlog])
            pass_dlog_txt.close()
        return pass_dlog

    def vco_band_monitor_on(self):
        band_info = []
        band_line = []
        for x in range(0, len(self.dlog_data)):
            if 'VCO_Band is' in self.dlog_data[x]:
                band_line = re.split("\s+", self.dlog_data[x])
                band_info.append(band_line[3])
                band_line = []
        return band_info

    def get_vco_band(self):
        band_info = []
        for x in range(0, len(self.dlog_data)):
            if 'Read All VCO band across configs for record:' in self.dlog_data[x]:
                band_info.append(self.dlog_data[x+2][14:16])
                band_info.append(self.dlog_data[x+4][14:16])
                band_info.append(self.dlog_data[x+6][14:16])
                band_info.append(self.dlog_data[x+8][14:15])
        return band_info

    def get_test_limit(self, keyword, tp_txt):
        test = filter(lambda search_for: keyword in search_for, self.dlog_data)
        split_data = []
        for x in test:
            x = re.split("\s+", x)
            split_data.append(x)
        tmin = []
        tmax = []
        for x in split_data:
            if x[2] == '0' and len(x)>12:
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
