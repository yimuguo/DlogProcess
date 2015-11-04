from dlogprocess import *

VCOLot1 = Dlog()
VCOLot1.read_dlog('.\\data\\VC5_exp\\61CL122129_VC5_Dlog.txt')
Band2500 = []
Band2525 = []


def target_vco_band(vco_freq):
    vco_freq_band = []
    for line in range(0, len(VCOLot1.dlog_data)):
        if VCOLot1.dlog_data[line][23:27] == str(vco_freq):
            for x in range(5, 13):
                if VCOLot1.dlog_data[line+x][1:4] == 'VCO' and VCOLot1.dlog_data[line+x][14:16] != '0H':
                    vco_freq_band.append(VCOLot1.dlog_data[line+x][14:16])
    return vco_freq_band

for vco in range(100, 121):
    spec_band = target_vco_band(vco*25)
    print("\n VCO Frequency: " + str(vco*25) + 'Mhz')
    print(spec_band)
    print("Total Units:" + str(len(spec_band)))
