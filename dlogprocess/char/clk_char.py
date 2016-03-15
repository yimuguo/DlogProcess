from dlogprocess.dlogprocess import Dlog
import re


class CharDlog(Dlog):
    def __init__(self, dlogpath, temp):
        super(CharDlog, self).__init__(dlogpath)
        self.dlog_data = self.screen_pass(write_to_file=0)
        self.temp = temp

    def