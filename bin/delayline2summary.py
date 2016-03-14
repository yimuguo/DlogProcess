from dlogprocess.char.delay_char import DlyLineDlog
import sys
import os
import numpy as np
import pandas as pd
import matplotlib
from collections import Counter


def data2df(lot_num, temp):
    dly = DlyLineDlog(os.path.join("..\\dlogprocess\\data\\Delay_line\\", lot_num, temp, "summary_" + temp + '.txt'), temp, lot_num)
    df_lst = dly.gen_df_lst()
    return pd.DataFrame(df_lst)

if __name__ == '__main__':
    lotnum = "RC01927M"
    temp = '25C'
    df = data2df(lotnum, temp)
    df = df.append(data2df(lotnum, '105C'))
    df = df.append(data2df(lotnum, '-5C'))
    lotnum = "RC01928M"
    df = df.append(data2df(lotnum, '25C'))
    df = df.append(data2df(lotnum, '105C'))
    df = df.append(data2df(lotnum, '-5C'))

    lotnum = "RC01929M"
    df = df.append(data2df(lotnum, '25C'))
    df = df.append(data2df(lotnum, '105C'))
    df = df.append(data2df(lotnum, '-5C'))

    df.columns = ['Lot', 'Temp', 'Dev#', 'VDD', 'Test', 'Data0', 'Data1']

    df = df[(df.Lot != 'RC01928M') | (df['Dev#'] != 20) | (df.Temp != '25C')]
    df = df[(df.Lot != 'RC01928M') | (df['Dev#'] != 26) | (df.Temp != '25C')]
    df = df[(df.Lot != 'RC01928M') | (df['Dev#'] != 21) | (df.Temp != '105C')]

    df = df[(df.Lot != 'RC01927M') | (df['Dev#'] != 4) | (df.Temp != '25C')]
    df = df[(df.Lot != 'RC01927M') | (df['Dev#'] != 3) | (df.Temp != '25C')]
    df = df[(df.Lot != 'RC01927M') | (df['Dev#'] != 17) | (df.Temp != '25C')]
    df = df[(df.Lot != 'RC01927M') | (df['Dev#'] != 3) | (df.Temp != '105C')]
    df = df[(df.Lot != 'RC01927M') | (df['Dev#'] != 16) | (df.Temp != '105C')]
    df = df[(df.Lot != 'RC01927M') | (df['Dev#'] != 4) | (df.Temp != '-5C')]
    df = df[(df.Lot != 'RC01927M') | (df['Dev#'] != 5) | (df.Temp != '-5C')]
    df = df[(df.Lot != 'RC01927M') | (df['Dev#'] != 6) | (df.Temp != '-5C')]
    df = df[(df.Lot != 'RC01927M') | (df['Dev#'] != 19) | (df.Temp != '-5C')]

    df = df[(df.Lot != 'RC01929M') | (df['Dev#'] != 20) | (df.Temp != '25C')]
    df = df[(df.Lot != 'RC01929M') | (df['Dev#'] != 21) | (df.Temp != '25C')]
    df = df[(df.Lot != 'RC01929M') | (df['Dev#'] != 25) | (df.Temp != '25C')]
    df = df[(df.Lot != 'RC01929M') | (df['Dev#'] != 20) | (df.Temp != '105C')]
    df = df[(df.Lot != 'RC01929M') | (df['Dev#'] != 21) | (df.Temp != '105C')]
    df = df[(df.Lot != 'RC01929M') | (df['Dev#'] != 25) | (df.Temp != '105C')]

    df = df[(df.Lot != 'RC01928M') | (df['Dev#'] != 9)]
    df = df[(df.Lot != 'RC01929M') | (df['Dev#'] != 9)]
    # df = df[(df.Lot != 'RC01929M') | (df['Dev#'] != 17)]
    df = df[(df.Lot != 'RC01928M') | (df['Dev#'] != 14)]
    df = df[(df.Lot != 'RC01927M') | (df['Dev#'] != 2)]
    df = df[(df.Lot != 'RC01928M') | (df['Dev#'] != 15)]
    df = df[(df.Lot != 'RC01929M') | (df['Dev#'] != 24)]

    df.loc[df.Test == 'Delay', 'Data1'] = df[df.Test == 'Delay'].Data1.astype(int)
    df.loc[df.Test == 'Delay', 'Dly'] = df[df.Test == 'Delay'].apply(lambda x: (x['Data0'] * 1000 - int(x['Data1'])) / int(x['Data1']) * 100, axis=1)
    df_dly = df[df.Test == 'Delay']

    VOL1_sum = df[(df.Test == 'VOL') & (df.Data1 == '1mA')].Data0.describe()
    VOL10_sum = df[(df.Test == 'VOL') & (df.Data1 == '10mA')].Data0.describe()
    VOH1_sum = df[(df.Test == 'VOH') & (df.Data1 == '1mA')].Data0.describe()
    VOH10_sum = df[(df.Test == 'VOH') & (df.Data1 == '10mA')].Data0.describe()
    VIH_sum = df[(df.Test == 'VIH')].Data0.describe()
    VIL_sum = df[(df.Test == 'VIL')].Data0.describe()
    IDD_sum = df[(df.Test == 'IDD') & (df.Data1 == 'STATIC')].Data0.describe()
    IDD_sum2 = df[(df.Test == 'IDD') & (df.Data1 == 'DYNAMIC')].Data0.describe()
    Dly1_sum = df_dly[df_dly['Data1'] < 8000]['Dly'].describe()
    Dly2_sum = df_dly[df_dly['Data1'] >= 8000].Dly.describe()
    sum_col = ['VOL_Iload=1mA', 'VOL_Iload=10mA', 'VOH_Iload=1mA', 'VOH_Iload=10mA', 'VIH', "VIL", 'IDD', 'IDD D', 'Delay=2~8uS', 'Delay=8~20uS']

    summary_table = pd.concat([VOL1_sum, VOL10_sum, VOH1_sum, VOH10_sum, VIH_sum, VIL_sum, IDD_sum, IDD_sum2, Dly1_sum, Dly2_sum], axis=1)
    summary_table.columns = sum_col
    summary_table.to_csv('summarytable.csv')

    df.to_csv('raw_data.csv')