import re
from dlogprocess.dlogprocess import Dlog


class DlyLineDlog(Dlog):
    dly_range1 = []
    dly_range2 = []
    dly_range3 = []

    def __init__(self, dlogpath, temp, lotnumber):
        super(DlyLineDlog, self).__init__(dlogpath)
        self.dlog_data = self.screen_pass(write_to_file=0)
        self.temp = temp
        self.lotnumber = lotnumber

    def df_splt_append_lst(self, lst_in, dev_number, rows, line_offset, test_type, data1=None):
        for row in range(0, rows):
            line_buffer = re.split("\s+", self.dlog_data[line_offset + row])
            lst_in.append([self.lotnumber, self.temp, int(dev_number), line_buffer[1], test_type,
                           float(line_buffer[2]), data1])

    # Data list: [LOT_num, Temp, Dev#, VDD, Test_Instance, Data0, Data1]
    def gen_df_lst(self):
        df_lst = []
        for line in range(0, len(self.dlog_data)):
            if "Device#:" in self.dlog_data[line]:
                dev_num = re.split("\s+", self.dlog_data[line])[2]
            elif "Delay=" in self.dlog_data[line]:
                dly_setting = self.dlog_data[line][11:15]
                self.df_splt_append_lst(df_lst, dev_num, 10, line + 4, "Delay", dly_setting)
            elif "Delay = " in self.dlog_data[line]:
                dly_setting = self.dlog_data[line][12:17]
                dly_setting = dly_setting.replace("(", "")
                if dly_setting != '4000':
                    self.df_splt_append_lst(df_lst, dev_num, 10, line + 4, "Delay", dly_setting)
            elif "Search_VIL_SDA" in self.dlog_data[line]:
                self.df_splt_append_lst(df_lst, dev_num, 10, line + 5, "VIL")
            elif "Search_VIH_SDA" in self.dlog_data[line]:
                self.df_splt_append_lst(df_lst, dev_num, 10, line + 5, "VIH")
            elif "VOL(mV) across Vcc(V)" in self.dlog_data[line]:
                for x in range(3, 13):
                    vdd_buffer = re.split("\s+", self.dlog_data[line + 2])
                    volh_meas_buffer10 = re.split("\s+", self.dlog_data[line + 4])
                    volh_meas_buffer1 = re.split("\s+", self.dlog_data[line + 5])
                    df_lst.append([self.lotnumber, self.temp, int(dev_num), vdd_buffer[x], "VOL",
                           float(volh_meas_buffer10[x]), "10mA"])
                    df_lst.append([self.lotnumber, self.temp, int(dev_num), vdd_buffer[x], "VOL",
                           float(volh_meas_buffer1[x]), "1mA"])
            elif "VOH(V) across Vcc(V)" in self.dlog_data[line]:
                for x in range(3, 13):
                    vdd_buffer = re.split("\s+", self.dlog_data[line + 2])
                    volh_meas_buffer10 = re.split("\s+", self.dlog_data[line + 4])
                    volh_meas_buffer1 = re.split("\s+", self.dlog_data[line + 5])
                    df_lst.append([self.lotnumber, self.temp, int(dev_num), vdd_buffer[x], "VOH",
                           float(volh_meas_buffer10[x]), "10mA"])
                    df_lst.append([self.lotnumber, self.temp, int(dev_num), vdd_buffer[x], "VOH",
                           float(volh_meas_buffer1[x]), "1mA"])
            elif "IDDO(mA) across Vcc(V)" in self.dlog_data[line]:
                for x in range(3, 13):
                    vdd_buffer = re.split("\s+", self.dlog_data[line + 2])
                    idd_meas_buffer = re.split("\s+", self.dlog_data[line + 4])
                    idd_meas_buffer_dyn = re.split("\s+", self.dlog_data[line + 6])
                    df_lst.append([self.lotnumber, self.temp, int(dev_num), vdd_buffer[x], "IDD",
                           float(idd_meas_buffer[x]), "STATIC"])
                    df_lst.append([self.lotnumber, self.temp, int(dev_num), vdd_buffer[x], "IDD",
                           float(idd_meas_buffer_dyn[x]), "DYNAMIC"])
        return df_lst

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
    #
    # def process_val(self):
    #     df = pd.DataFrame(self.dly_range1, [x for x in range(2000, 4100, 100)])
    #     print(df.head())


