from dlogprocess.dlogprocess import Dlog
import re


class CharDlog(Dlog):
    def __init__(self, dlogpath, temp):
        super(CharDlog, self).__init__(dlogpath)
        # self.dlog_data = self.screen_pass(write_to_file=0)
        self.temp = temp
        self.char_table = []

    @staticmethod
    def ln_match_header(str_in):
        if re.match('^\s+[a-zA-Z]+\([a-zA-z]\)+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+', str_in):
            return True
        else:
            return False

    @staticmethod
    def ln_match_char(str_in):
        if re.match('^\s+[a-zA-Z]+_[a-zA-z0-9]+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+', str_in):
            return True
        else:
            return False

    def find_char_table(self):
        table_start = 0
        for line in range(0, len(self.dlog_data)):
            if re.match('^\s+=+', self.dlog_data[line]):
                    if self.ln_match_header(self.dlog_data[line+1]) and \
                        (re.match('^\s+=+', self.dlog_data[line+2]) or
                         re.match('^\s+=+', self.dlog_data[line+3])) and \
                        (self.ln_match_char(self.dlog_data[line+3]) or
                         self.ln_match_char(self.dlog_data[line+4])):
                        table_start = 1
                        self.char_table.append(self.dlog_data[line-1])
            if table_start == 1:
                self.char_table.append(self.dlog_data[line])
                if re.match('^\s+$', self.dlog_data[line+1]):
                    table_start = 0

