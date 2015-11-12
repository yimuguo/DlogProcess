# from dlogprocess import *

__author__ = 'Eame'


def read_dlog(dlog_path):
    with open(dlog_path, 'r') as data:
        dlog_data = data.read().splitlines()
    return dlog_data
# VCOBandDatang = Dlog()
BandInfo = []
BandBuffer = []
for unit in range(2, 21):
    dlog_data = read_dlog('.\\data\\Roland_Data\\50C\\U' + str(unit) + '.txt')
    for x in range(0, len(dlog_data)):
        if 'Turn Off Test_VCO_band and Calibrate VCO Band' in dlog_data[x]:
            BandBuffer.append(dlog_data[x+4][14:16])
    BandInfo.append(BandBuffer)
    for i in range(0, 10):
        if BandBuffer[i] != BandBuffer[i+1]:
            print("Unit " + str(unit) + " multiple band values during calibration")
            print(BandBuffer)
            break
        if i == 9 and BandBuffer[i] == 'CH':
            print("Unit " + str(unit) + " calibrated to Band Ch")
        elif i == 9 and BandBuffer[i] == "BH":
            print("Unit " + str(unit) + " calibrated to Band Bh")
    print(BandBuffer)
    BandBuffer = []
Band98 = []
for line in range(0, len(BandInfo)):
    Band98.append(BandInfo[line][10])
print("Band Eh has %s units" % str(Band98.count('EH')))
print("Band Dh has %s units" % str(Band98.count('DH')))
