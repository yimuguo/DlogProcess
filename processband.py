__author__ = 'Eame'


def get_band(dlogfile):
    with open(dlogfile) as data:
        dlog_data = data.read().splitlines()
    band_info = []

    for x in range(0, len(dlog_data)):
        if 'Read All VCO band across configs for record:' in dlog_data[x]:
            band_info.append(dlog_data[x+2][14:16])
            band_info.append(dlog_data[x+4][14:16])
            band_info.append(dlog_data[x+6][14:16])
            band_info.append(dlog_data[x+8][14:15])
    return band_info


FF_band = get_band("PassUnits_FF.txt")
print(FF_band)
print('band 14H has ' + str(FF_band.count('14')/3) + ' units')
print('band 13H has ' + str(FF_band.count('13')/3) + ' units')
print('band 15H has ' + str(FF_band.count('15')/3) + ' units')
print('band CH has ' + str(FF_band.count('C')) + ' units')
print('band BH has ' + str(FF_band.count('B')) + ' units')
print('band DH has ' + str(FF_band.count('D')) + ' units')

SS_band = get_band("PassUnits_SS.txt")
print(SS_band)
print('band 14H has ' + str(SS_band.count('14')/3) + ' units')
print('band 13H has ' + str(SS_band.count('13')/3) + ' units')
print('band 15H has ' + str(SS_band.count('15')/3) + ' units')
print('band CH has ' + str(SS_band.count('C')) + ' units')
print('band BH has ' + str(SS_band.count('B')) + ' units')
print('band DH has ' + str(SS_band.count('D')) + ' units')
