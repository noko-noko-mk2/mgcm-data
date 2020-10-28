import pandas as pd

def read_data(data_files):

    def read_tsv(f):
        tmp_df = pd.read_csv(f, sep='\t')
        # ブースターが入っている場合はベルと魔法糸を1/2に
        for c in ['魔法糸小', '魔法糸中', '魔法糸大']:
            tmp_df[c] = tmp_df[c] / (tmp_df['魔法糸ブースター'] + 1)
        tmp_df['ベル'] = tmp_df['ベル'] / (tmp_df['ベルブースター'] + 1)
        return tmp_df.drop(['ベルブースター', '魔法糸ブースター'], axis=1)
        
    return pd.concat([
        read_tsv(f) for f in data_files
    ])
