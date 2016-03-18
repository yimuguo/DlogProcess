from dlogprocess.dlogprocess import Dlog
import re


class CharDlog(Dlog):
    def __init__(self, dlogpath, temp='25C'):
        super(CharDlog, self).__init__(dlogpath, temp=temp)
        # self.dlog_data = self.screen_pass(write_to_file=0)
        self.char_table = self.find_char_table()

    @staticmethod
    def ln_match_header(str_in):
        if re.match('^(:?\s+[a-zA-Z]+|[a-zA-Z]+)\([a-zA-z]+\)+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+', str_in):
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
        if re.match('^\s+[a-zA-Z]+_[a-zA-z0-9]+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+[-+]?\d*\.\d+\s+', str_in):
            return 1
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
            try:
                next_ln_flg = self.ln_match_header(self.dlog_data[line+1])
            except IndexError:
                continue
            if self.ln_match_eql(self.dlog_data[line]) and next_ln_flg:
                if self.ln_match_eql(self.dlog_data[line+2]) and \
                   self.ln_match_char(self.dlog_data[line+3]):
                    table_type = 'SUMMARY'
                    table_buffer.append(table_type)
                    for x in range(-1, 3):
                        table_buffer.append(self.dlog_data[line+x])
                    i = 3
                    while self.ln_match_char(self.dlog_data[line+i]):
                        table_buffer.append(self.dlog_data[line+i])
                        i += 1
                    char_table.append(table_buffer)
                    line += i
                    table_buffer = []
                elif self.ln_match_header(self.dlog_data[line+2]) and \
                        self.ln_match_eql(self.dlog_data[line+3]) and \
                        self.ln_match_char(self.dlog_data[line+4]):
                    table_type = 'DC'
                    table_buffer.append(table_type)
                    for x in range(-1, 4):
                        table_buffer.append(self.dlog_data[line+x])
                    i = 4
                    while self.ln_match_char(self.dlog_data[line+i]):
                        table_buffer.append(self.dlog_data[line+i])
                        i += 1
                    line += i
                    char_table.append(table_buffer)
                    table_buffer = []
                else:
                    continue
        return char_table

        # def find_char_table(self):
    #     table_start = 0
    #     table_buffer = []
    #     char_table = []
    #     for line in range(0, len(self.dlog_data)):
    #         if re.match('^\s+=+', self.dlog_data[line]):
    #                 if self.ln_match_header(self.dlog_data[line+1]) and \
    #                     (re.match('^\s+=+', self.dlog_data[line+2]) or
    #                      re.match('^\s+=+', self.dlog_data[line+3])) and \
    #                     (self.ln_match_char(self.dlog_data[line+3]) or
    #                      self.ln_match_char(self.dlog_data[line+4])):
    #                     table_start = 1
    #                     table_buffer.append(self.dlog_data[line-1])
    #         if table_start == 1:
    #             table_buffer.append(self.dlog_data[line])
    #             if not (self.ln_match_char(self.dlog_data[line+1]) or
    #                     self.ln_match_header(self.dlog_data[line+1]) or
    #                     re.match('^\s+=+', self.dlog_data[line+1])):
    #                 table_start = 0
    #     return char_table
