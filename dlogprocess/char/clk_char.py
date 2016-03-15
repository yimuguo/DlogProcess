from dlogprocess.dlogprocess import Dlog
import re


class CharDlog(Dlog):
    def __init__(self, dlogpath, temp):
        super(CharDlog, self).__init__(dlogpath)
        self.dlog_data = self.screen_pass(write_to_file=0)
        self.temp = temp

    @staticmethod
    def ln_match_char(str_in):
        if re.match('^\s+[a-zA-Z]+_[a-zA-z0-9]+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+', str_in):
            return True
        else:
            return False

    def find_char_table(self):
        for line in range(0, len(self.dlog_data)):
            if re.match('\s+=+', self.dlog_data[line]):
                table_str = 1
