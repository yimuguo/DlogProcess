from dlogprocess import *

__author__ = 'Eame'


VCOBandDatang = Dlog()
BandInfo = []
BandBuffer = []
for unit in range(1, 99):
    VCOBandDatang.read_dlog(
        '.\\examples\\VCOCal\\U' + str(unit) + '.txt')
    for x in range(0, len(VCOBandDatang.dlog_data)):
        if 'Turn Off Test_VCO_band and Calibrate VCO Band' in VCOBandDatang.dlog_data[x]:
            BandBuffer.append(VCOBandDatang.dlog_data[x+4][14:16])
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
    BandBuffer = []
Band98 = []
for line in range(0, len(BandInfo)):
    Band98.append(BandInfo[line][0])
print("Band Ch has %s units" % str(Band98.count('CH')))
print("Band Bh has %s units" % str(Band98.count('BH')))
