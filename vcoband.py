__author__ = 'yguo'


def screen_pass(lotnumber, original_dlog):
    data_buffer = []
    pass_dlog = open('PassUnits_%s.txt' % lotnumber, 'w+')
    new_device = 0
    for line in range(0, len(original_dlog)):
        if "Device#:" in original_dlog[line]:
            new_device = 1
        if new_device == 1:
            data_buffer.append(original_dlog[line])
        if original_dlog[line][:73] == '=========================================================================':
            new_device = 0
            if original_dlog[line-1][14:25] == '1         1':
                pass_dlog.writelines(["%s\n" % item for item in data_buffer])
            data_buffer = []
    pass_dlog.close()

with open(".\\examples\\20MY_HOT_5P49V5901_FT_754_J750-05_1A.txt", 'r') as data:
    SkewLotsDlog = data.read().splitlines()
screen_pass('FF', SkewLotsDlog)
with open(".\\examples\\21MY_HOT_5P49V5901_FT_754_J750-05_1A.txt", 'r') as data:
    SkewLotsDlog = data.read().splitlines()
screen_pass('SS', SkewLotsDlog)
# SkewLotsDlog.clear()
# devices = open('PassUnits_FF.txt', 'r').read()
# print("There are " + str(devices.count('Device#:')) + " units passed dlog in this file")
# devices = open('PassUnits_SS.txt', 'r').read()
# print("There are " + str(devices.count('Device#:')) + " units passed dlog in this file")
