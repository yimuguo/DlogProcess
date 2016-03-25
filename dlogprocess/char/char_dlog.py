from dlogprocess.dlogprocess import Dlog
import re
import pandas as pd
import warnings
from collections import Counter


class CharDlog(Dlog):
    def __init__(self, dlogpath, temp='25C', lotnum='TT', unitnum=1):
        super(CharDlog, self).__init__(dlogpath, temp=temp, lotnumber=lotnum)
        # self.dlog_data = self.screen_pass(write_to_file=0)
        self.char_table = self.find_char_table()
        self.unit = unitnum

    @staticmethod
    def ln_match_header(str_in):
        # Search for " (any_char)VDD|VCC(any_char,w/o ())  +-float  +-float +-float
        if re.match('^\s*[a-zA-Z0-9_]*(:?VDD|VCC)[a-zA-Z0-9/_\(\)]*\s+'
                    '[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+', str_in):
            return True
        else:
            return False

    @staticmethod
    def ln_match_load(str_in):
        # Search for " (any_char)VDD|VCC(any_char,w/o ())  +-float  +-float +-float
        if re.match('^\s*[a-zA-Z0-9]*(Iload)[a-zA-Z0-9\(\)]*\s+'
                    '[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+', str_in):
            return True
        else:
            return False

    @staticmethod
    def ln_match_shmoo(str_in):
        if re.match('^(:?\s+\d*\.\d+|\d*\.\d+)\s+[-+]?\d*\.\d+\s+\d\s+\d\s+', str_in):
            return True
        else:
            return False

    @staticmethod
    def ln_match_char(str_in):
        # Search for " any_char|num|_-anychar|num_  float  float  float
        if re.match('^\s+[a-zA-Z0-9_]+-[a-zA-z0-9_]+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+', str_in):
            return 1
        # Search for " any_char{w/o _:} float float float "
        if re.match('^\s+[a-zA-Z0-9:_]+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+', str_in):
            return 2   # SMB is the only one without pin name
        else:
            return False

    @staticmethod
    def ln_match_comment(str_in):
        comment_ln = re.compile(r'^\s*(\d+\.)?\s*([a-zA-Z0-9/ ]+)\(([a-zA-Z]+)\)')
        return comment_ln.search(str_in)

    @staticmethod
    def ln_match_eql(str_in):
        return re.match(r'^(:?\s+=+|=+)', str_in)

    def find_char_table(self):
        table_buffer = []
        char_table = []
        for line in range(0, len(self.dlog_data)):
            if self.ln_match_eql(self.dlog_data[line-1]) and self.ln_match_header(self.dlog_data[line]):
                if self.ln_match_eql(self.dlog_data[line+1]) and \
                   self.ln_match_char(self.dlog_data[line+2]):
                    table_type = 'SUMMARY'
                    if self.ln_match_char(self.dlog_data[line+2]) == 2:
                        table_type = 'SMB'
                    table_buffer.append(table_type)
                    for x in range(-2, 2):
                        table_buffer.append(self.dlog_data[line+x])
                    i = 2
                    while self.ln_match_char(self.dlog_data[line+i]):
                        table_buffer.append(self.dlog_data[line+i])
                        i += 1
                    char_table.append(table_buffer)
                    line += i
                    table_buffer = []
                elif self.ln_match_load(self.dlog_data[line+1]) and \
                        self.ln_match_eql(self.dlog_data[line+2]) and \
                        self.ln_match_char(self.dlog_data[line+3]):
                    table_type = 'DC'
                    table_buffer.append(table_type)
                    for x in range(-2, 3):
                        table_buffer.append(self.dlog_data[line+x])
                    i = 3
                    while self.ln_match_char(self.dlog_data[line+i]):
                        table_buffer.append(self.dlog_data[line+i])
                        i += 1
                    line += i
                    char_table.append(table_buffer)
                    table_buffer = []
                else:
                    continue
        return char_table

    @staticmethod
    def re_vco_freq_ln(str_in):
        # Search for " Fmax VCO (for PLL some_char) float/int some_char "
        re_vco = re.compile(r'\s*Fmax\s+VCO\s*(for)?\s*(PLL\d*)?\s*[a-zA-Z]*\s*(\d*\.\d+|\d+)\s*([a-zA-Z]*)?')
        return re_vco.search(str_in)

    # List [VDD, "VCO_max", PLL*, Data]
    def get_vco_max(self):
        vdd_val = 'Unknown'
        vco_table = []
        plln = 'PLL'
        unit = 'Unknown'
        for x in self.dlog_data:
            if self.re_vdd_comment(x):
                vdd_val = self.re_vdd_comment(x).group(1)
            elif self.re_vco_freq_ln(x):
                max_vco = self.re_vco_freq_ln(x).group(3)
                if self.re_vco_freq_ln(x).group(2):
                    plln = self.re_vco_freq_ln(x).group(2)
                if self.re_vco_freq_ln(x).group(4):
                    unit = self.re_vco_freq_ln(x).group(4)
                vco_table.append([vdd_val, 'VCO_max', plln, max_vco, unit])
        return vco_table

    # List [VDD, Test, Pin, Data, unit, Load(forDCOnly)]
    def parse_table(self, char_table):
        dataset = []
        test_line = []
        iload_line = []
        vdd_line = []
        unit = 'Unknown'
        for x in char_table:
            if self.ln_match_header(x):
                vdd_line = x.split()
            elif self.ln_match_char(x):
                test_line.append(x.split())
            elif self.ln_match_load(x):
                iload_line.extend(x.split())
            elif self.ln_match_comment(x):
                unit = self.ln_match_comment(x).group(3)
        # Auto_Fill missing VDD Column Headers!!!
        vdd_len = 0
        for i in test_line:
            if (len(i) > len(vdd_line)) & (len(i) > vdd_len):
                vdd_len = len(i)
                vdd_delta = round(float(vdd_line[-2]) - float(vdd_line[-1]), 3)
                while vdd_len > len(vdd_line):
                    vdd_line.append(str(round(float(vdd_line[-1]) - vdd_delta, 3)))
                warnings.simplefilter('once', UserWarning)
                warnings.warn("VDD Line Should be Matching Test Instances")
        # Warning finished, and auto filled missing VDD cols

        for row in range(0, len(test_line)):
            if char_table[0] == 'DC':
                pinnam = test_line[row][0].split('-')[1]
                test = test_line[row][0].split('-')[0]
                for column in range(1, len(test_line[row])):
                    dataset.append([vdd_line[column], test, pinnam, test_line[row][column], unit, iload_line[column]])
            elif char_table[0] == 'SMB':
                test = test_line[row][0]
                pinnam = 'SMB'
                for column in range(1, len(test_line[row])):
                    dataset.append([vdd_line[column], test, pinnam, test_line[row][column], unit])
            elif char_table[0] == 'SUMMARY':
                pinnam = test_line[row][0].split('-')[1]
                test = test_line[row][0].split('-')[0]
                for column in range(1, len(test_line[row])):
                    dataset.append([vdd_line[column], test, pinnam, test_line[row][column], unit])
        return dataset

    # List [VDD, "OutputLeakage", Pin, Data, ForceV]
    def get_test_table(self, test_name):
        lkg_table = []
        out_lkg = self.filter_test_details(test_name)
        for x in range(0, len(out_lkg)):
            lkg_table.append([out_lkg[x][14], test_name, out_lkg[x][4], out_lkg[x][8], out_lkg[x][9], out_lkg[x][12]])
        return lkg_table

    # Units: IDD:mA, DC(VOLH/ROLH):V, SMB:us,
    def gen_df(self):
        all_dataset = []
        for x in self.char_table:
            all_dataset.extend(self.parse_table(x))
        all_dataset.extend(self.get_vco_max())
        all_dataset.extend(self.get_test_table("OutputLeakage"))
        all_dataset.extend(self.get_test_table("InputLeakage"))
        df = pd.DataFrame(all_dataset, columns=['VDD', 'Test', 'Pin', 'Data', 'unit', 'Force'])
        df['Lot'] = self.lotnumber
        df['Temp'] = self.temp
        df['UnitNum'] = self.unit
        return df

    def gen_summary_test(self):
        data = self.gen_df()
        tests = Counter(data.Test).keys()
        pins = Counter(data.Pin).keys()

        print(tests)
