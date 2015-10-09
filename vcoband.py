__author__ = 'yguo'

import re

LineBuffer = []
with open(".\\examples\\21MY_HOT_5P49V5901_FT_754_J750-05_1A", 'r') as data:
    SkewLotsDlog = data.read().splitlines()
PassDlog = open('PassUnits.txt', 'w+')

for line in SkewLotsDlog:
    if "Device#:" in line:
        NewDevice = 1
        continue
    LineBuffer.append(line)
    if line[15:25] == '1         1':
        NewDevice = 0
        PassDlog.writelines(LineBuffer)

