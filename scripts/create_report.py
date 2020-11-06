import jinja2
import pandas as pd

def read_data(data):
    tmp_df = pd.read_csv(data['url'], sep='\t')
    print(tmp_df)
    # ブースターが入っている場合はベルと魔法糸を1/2に
    for c in ['魔法糸小', '魔法糸中', '魔法糸大']:
        if not c in tmp_df:
            continue
        tmp_df[c] = tmp_df[c] / (tmp_df['魔法糸ブースター'] + 1)
    if 'ベル' in tmp_df:
        tmp_df['ベル'] = tmp_df['ベル'] / (tmp_df['ベルブースター'] + 1)
    return tmp_df.drop(['ベルブースター', '魔法糸ブースター'], axis=1)

# 対象データファイル
DATA_FILES = [
    {
      'name': 'メインストーリー第2部7章',
      'url': 'https://raw.githubusercontent.com/noko-noko-mk2/mgcm-data/main/data/%E3%83%A1%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AA%E3%83%BC%E7%AC%AC2%E9%83%A8/%E7%AC%AC7%E7%AB%A0.tsv',
      'columns': ['ステージ', '周回数', '魔法糸中', '魔法糸大', 'ベル', 'ジュエル', 'プレミアガチャチケット', 'SR以上限定プレミアガチャチケットのかけら', '1984陽彩', '2061陽彩', 'クッキングエプロン陽彩', 'ホリデーカジュアル陽彩', 'ラウンジウェア陽彩', '猛撃の破宝珠', '勇猛の破宝珠']
    },
    {
      'name': 'メインストーリー第2部10章',
      'url': 'https://raw.githubusercontent.com/noko-noko-mk2/mgcm-data/main/data/%E3%83%A1%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AA%E3%83%BC%E7%AC%AC2%E9%83%A8/%E7%AC%AC10%E7%AB%A0.tsv',
      'columns': ['ステージ', '周回数', '魔法糸中', '魔法糸大', 'ベル', 'ジュエル', 'プレミアガチャチケット', 'SR以上限定プレミアガチャチケットのかけら', '1984エリザ', '2061エリザ', 'クッキングエプロンエリザ', 'ホリデーカジュアルエリザ', 'ラウンジウェアエリザ', '俊敏の破宝珠', '精密の破宝珠']
    },
    {
      'name': '無尽ニンフ',
      'url': 'https://raw.githubusercontent.com/noko-noko-mk2/mgcm-data/main/data/%E7%84%A1%E5%B0%BD/%E7%84%A1%E5%B0%BD%E3%83%8B%E3%83%B3%E3%83%95.tsv',
      'columns': ['ステージ', '周回数', 'UR宝珠', 'SR宝珠', 'R宝珠', '魔技のクォーツ', 'ジュエル', '魔法糸大', 'UR確定プレミアガチャチケットのかけら', 'SR以上限定プレミアガチャチケットのかけら', 'プレミアガチャチケット', '属性技の素材（下級）', '属性技の素材（中級）', '属性技の素材（上級）']
    },
]

# 小数点以下丸め設定
COLUMN_ROUND = {
    '周回数': 0,
    '魔法糸中': 3,
    '魔法糸大': 3,
    'ベル': 1,
    'ジュエル': 5,
    'プレミアガチャチケット': 7,
    'SR以上限定プレミアガチャチケットのかけら': 5,
    '1984エリザ': 7,
    '2061エリザ': 7,
    'クッキングエプロンエリザ': 7,
    'ホリデーカジュアルエリザ': 7,
    'ラウンジウェアエリザ': 7,
    '1984陽彩': 7,
    '2061陽彩': 7,
    'クッキングエプロン陽彩': 7,
    'ホリデーカジュアル陽彩': 7,
    'ラウンジウェア陽彩': 7,
    '俊敏の破宝珠': 3,
    '精密の破宝珠': 3,
    '猛撃の破宝珠': 3,
    '勇猛の破宝珠': 3
}

reports = []

for row in DATA_FILES:
    df = read_data(row)
    sum_df = df.groupby('ステージ').sum()
    stage_avg = sum_df.divide(sum_df['周回数'], axis=0).drop(['周回数', '1周スタミナ'], axis=1)
    stage_avg['周回数'] = sum_df['周回数']
    for k, v in COLUMN_ROUND.items():
        if k in stage_avg:
            stage_avg[k] = stage_avg[k].apply(lambda x: format(x, '.%df' % v))
    row['data'] = stage_avg.reset_index()
    reports.append(row)

templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "create_report_template.j2"
template = templateEnv.get_template(TEMPLATE_FILE)

with open('../reports/main_report.md', 'wt') as fp:
    fp.write(template.render(reports=reports))

