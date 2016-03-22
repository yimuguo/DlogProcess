from dlogprocess.dlogprocess import Dlog
import re


class CharDlog(Dlog):
    def __init__(self, dlogpath, temp='25C'):
        super(CharDlog, self).__init__(dlogpath, temp=temp)
        # self.dlog_data = self.screen_pass(write_to_file=0)
        self.char_table = self.find_char_table()

    @staticmethod
    def ln_match_header(str_in):
        # Search for " (any_char)VDD|VCC(any_char,w/o ())  +-float  +-float +-float
        if re.match('^\s*[a-zA-Z0-9]*(:?VDD|VCC)[a-zA-Z0-9\(\)]*\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+', str_in):
            return True
        else:
            return False

    @staticmethod
    def ln_match_load(str_in):
        # Search for " (any_char)VDD|VCC(any_char,w/o ())  +-float  +-float +-float
        if re.match('^\s*[a-zA-Z0-9]*(Iload)[a-zA-Z0-9\(\)]*\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+', str_in):
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
                elif self.ln_match_header(self.dlog_data[line+1]) and \
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

    # List [VDD, Test, Pin, Data, Load(forDCOnly)]
    def parse_table(self, char_table):
        dataset = []
        test_line = []
        iload_line = []
        vdd_line = []
        for x in char_table:
            if self.ln_match_header(x):
                vdd_line = x.split()
            elif self.ln_match_char(x):
                test_line.append(x.split())
            elif self.ln_match_load(x):
                iload_line.append(x.split())
        for row in range(0, len(test_line)):
            if char_table[0] == 'DC':
                pinnam = test_line[row][0].split('-')[0]
                test = test_line[row][0].split('-')[1]
                for column in range(1, len(test_line[row])):
                    dataset.append([vdd_line[column], test, pinnam, test_line[row][column], iload_line[column]])
            elif char_table[0] == 'SMB':
                test = test_line[row][0]
                pinnam = 'SMB'
                for column in range(1, len(test_line[row])):
                    dataset.append([vdd_line[column], test, pinnam, test_line[row][column]])
            elif char_table[0] == 'SUMMARY':
                pinnam = test_line[row][0].split('-')[0]
                test = test_line[row][0].split('-')[1]
                for column in range(1, len(test_line[row])):
                    dataset.append([vdd_line[column], test, pinnam, test_line[row][column]])
        return dataset

