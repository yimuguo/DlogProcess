from dlogprocess.char.char_dlog import CharDlog
import pandas as pd


def main():
    dfs = pd.DataFrame()
    temp = '25C'
    for unit in range(1, 11):
        vc3s = CharDlog('..\\dlogprocess\\data\\char\\' + temp + '\\U' + str(unit) + '.txt', temp, unitnum=unit)
        dfs = dfs.append(vc3s.gen_df())
    temp = '90C'
    for unit in range(1, 11):
        vc3s = CharDlog('..\\dlogprocess\\data\\char\\' + temp + '\\U' + str(unit) + '.txt', temp, unitnum=unit)
        dfs = dfs.append(vc3s.gen_df())
    dfs.to_csv('testlotvc3s.csv')

    df_1 = pd.DataFrame()
    temp = '25C'
    vc3s = CharDlog('..\\dlogprocess\\data\\char\\1 part at Room.txt')
    df_1.append(vc3s.gen_df())
    dfs.to_csv('test.csv')

if __name__ == '__main__':
    main()
