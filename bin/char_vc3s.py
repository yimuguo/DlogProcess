from dlogprocess.char.char_dlog import CharDlog
import pandas as pd


def main():
    dfs = pd.DataFrame()
    temp = '25C'
    for unit in range(1, 11):
        vc3s = CharDlog('..\\data\\Char\\' + temp + '\\U' + str(unit) + '.txt', temp, unitnum=unit)
        dfs = dfs.append(vc3s.gen_df())
    temp = '90C'
    for unit in range(1, 11):
        vc3s = CharDlog('..\\data\\Char\\' + temp + '\\U' + str(unit) + '.txt', temp, unitnum=unit)
        dfs = dfs.append(vc3s.gen_df())
    dfs.to_csv('testlotvc3s.csv')

if __name__ == '__main__':
    main()
