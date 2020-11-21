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
      'url': '../data/メインストーリー第2部/第7章.tsv',
      'columns': ['ステージ', '周回数', '魔法糸中', '魔法糸大', 'ベル', 'ジュエル', 'プレミアガチャチケット', 'SR以上限定プレミアガチャチケットのかけら', '1984陽彩', '2061陽彩', 'クッキングエプロン陽彩', 'ホリデーカジュアル陽彩', 'ラウンジウェア陽彩', '猛撃の破宝珠', '勇猛の破宝珠']
    },
    {
      'name': 'メインストーリー第2部10章',
      'url': '../data/メインストーリー第2部/第10章.tsv',
      'columns': ['ステージ', '周回数', '魔法糸中', '魔法糸大', 'ベル', 'ジュエル', 'プレミアガチャチケット', 'SR以上限定プレミアガチャチケットのかけら', '1984エリザ', '2061エリザ', 'クッキングエプロンエリザ', 'ホリデーカジュアルエリザ', 'ラウンジウェアエリザ', '俊敏の破宝珠', '精密の破宝珠']
    },
    {
      'name': 'メインストーリー第2部11章',
      'url': '../data/メインストーリー第2部/第11章.tsv',
      'columns': ['ステージ', '周回数', '魔法糸中', '魔法糸大', 'ベル', 'ジュエル', 'プレミアガチャチケット', 'SR以上限定プレミアガチャチケットのかけら', '1984セイラ', '2061セイラ', 'クッキングエプロンセイラ', 'ホリデーカジュアルセイラ', 'ラウンジウェアセイラ', '1984ここあ', '2061ここあ', 'クッキングエプロンここあ', 'ホリデーカジュアルここあ', 'ラウンジウェアここあ', '俊敏の破宝珠', '拒絶の破宝珠']
    },
    {
      'name': '無尽ニンフ',
      'url': '../data/無尽/無尽ニンフ.tsv',
      'columns': ['ステージ', '周回数', 'UR宝珠', 'SR宝珠', 'R宝珠', '魔技のクォーツ', 'ジュエル', '魔法糸大', 'UR確定プレミアガチャチケットのかけら', 'SR以上限定プレミアガチャチケットのかけら', 'プレミアガチャチケット', '属性技の素材（下級）', '属性技の素材（中級）', '属性技の素材（上級）']
    },
]

# 小数点以下丸め設定
COLUMN_ROUND = {
    '周回数': 0,
    '魔法糸中': 3,
    '魔法糸大': 3,
    'ベル': 1,
    'ジュエル': 4,
    'プレミアガチャチケット': 5,
    'SR以上限定プレミアガチャチケットのかけら': 4,
    '1984エリザ': 5,
    '2061エリザ': 5,
    'クッキングエプロンエリザ': 5,
    'ホリデーカジュアルエリザ': 5,
    'ラウンジウェアエリザ': 5,
    '1984陽彩': 5,
    '2061陽彩': 5,
    'クッキングエプロン陽彩': 5,
    'ホリデーカジュアル陽彩': 5,
    'ラウンジウェア陽彩': 5,
    '1984セイラ': 5,
    '2061セイラ': 5,
    'クッキングエプロンセイラ': 5,
    'ホリデーカジュアルセイラ': 5,
    'ラウンジウェアセイラ': 5,
    '1984ここあ': 5,
    '2061ここあ': 5,
    'クッキングエプロンここあ': 5,
    'ホリデーカジュアルここあ': 5,
    'ラウンジウェアここあ': 5,
    '俊敏の破宝珠': 3,
    '精密の破宝珠': 3,
    '猛撃の破宝珠': 3,
    '勇猛の破宝珠': 3,
    '拒絶の破宝珠': 3,
    'UR宝珠': 5,
    'SR宝珠': 3,
    'R宝珠': 3,
    '魔技のクォーツ': 3,
    'UR確定プレミアガチャチケットのかけら': 4,
    '属性技の素材（下級）': 1,
    '属性技の素材（中級）': 1,
    '属性技の素材（上級）': 1,
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
print(template.render(reports=reports))

with open('../reports/main_report.md', 'wt') as f:
    f.write(template.render(reports=reports))

