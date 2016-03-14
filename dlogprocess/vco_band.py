from dlogprocess.dlogprocess import Dlog
from collections import Counter
import re


class DlogVCO(Dlog):
    def __init__(self, dlogpath):
        super(DlogVCO, self).__init__(dlogpath)

    def get_target_vco_band(self, vco_freq):
        vco_freq_band = []
        for line in range(0, len(self.dlog_data)):
            if self.dlog_data[line][23:27] == str(vco_freq):
                for x in range(5, 13):
                    if self.dlog_data[line+x][1:4] == 'VCO' and \
                                    self.dlog_data[line+x][14:16] != '0H':
                        vco_freq_band.append(self.dlog_data[line+x][14:16])
        return vco_freq_band

    def print_vco_band_detail(self, start_freq=2500, stop_freq=3000, step=25):
        for vco in range(start_freq, stop_freq+step, step):
            spec_band = self.get_target_vco_band(vco)
            if vco == start_freq:
                print("Total Record:" + str(len(spec_band)))
            print("\nLot " + self.lotnumber + " VCO Frequency: " + str(vco) + 'Mhz')
            # print(spec_band)
            # Number of bands appeared during calibration
            print(str(len(Counter(spec_band).keys())) + ' possible bands')
            for keys in Counter(spec_band):
                print(str(vco) + " {0:.2f}".format(int(Counter(spec_band)[keys])/len(spec_band)*100) +
                      "% of the units calibrated to Band" + keys + " " + str(Counter(spec_band)[keys]))
                # print(str(vco*25) + 'Mhz')
                # print(keys)
                # print(Counter(spec_band)[keys])

            # print(Counter(spec_band).keys())
            # print(Counter(spec_band).values())

    def vco_band_monitor_on(self):
        band_info = []
        band_line = []
        for x in range(0, len(self.dlog_data)):
            if 'VCO_Band is' in self.dlog_data[x]:
                band_line = re.split("\s+", self.dlog_data[x])
                band_info.append(band_line[3])
                band_line.clear()
        return band_info

    def get_vco_band(self, site=0):
        band_info = []

        for x in range(0, len(self.dlog_data)):
            if 'Read All VCO band across configs for record:' in self.dlog_data[x]:
                band_info.append(self.dlog_data[x+2][14:16])
                band_info.append(self.dlog_data[x+4][14:16])
                band_info.append(self.dlog_data[x+6][14:16])
                band_info.append(self.dlog_data[x+8][14:15])
        return band_info