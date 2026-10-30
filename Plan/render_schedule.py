"""用既有 Matplotlib 匯出排程圖；先執行 recalculate.py。"""
import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from matplotlib.patches import Patch


ROOT = Path(__file__).resolve().parent
font_path = Path('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc')
if font_path.is_file():
    font_manager.fontManager.addfont(str(font_path))
    plt.rcParams['font.family'] = font_manager.FontProperties(fname=font_path).get_name()
plt.rcParams['svg.fonttype'] = 'path'


def rows(name):
    with (ROOT/name).open(encoding='utf-8-sig') as stream:
        return list(csv.DictReader(stream))


def aoa():
    events = {int(x['event']): x for x in rows('events.csv')}
    edges = rows('cpm.csv')
    first = {0:(0,2), 10:(2.5,2), 20:(5,2), 30:(7.5,4), 40:(7.5,2),
             50:(10,2), 60:(7.5,0), 70:(12.5,2), 80:(15,2)}
    second = {80:(0,2), 90:(2.7,2), 100:(5.4,2), 110:(8.1,2), 120:(10.8,4.4),
              130:(10.8,0), 135:(13.5,4.4), 140:(13.5,0), 150:(16.2,0),
              160:(18.9,2), 170:(21.6,2)}
    fig, axes = plt.subplots(2, 1, figsize=(21, 10), layout='constrained')
    for ax, positions, title in zip(axes, [first, second],
                                    ['一、基礎模組與動作驗證', '二、引擎、研究框架與既有 CLM'], strict=True):
        ax.set_title(title, loc='left', fontsize=14)
        for edge in edges:
            i, j = int(edge['i']), int(edge['j'])
            if i not in positions or j not in positions:
                continue

            left, right = positions[i], positions[j]
            dummy = float(edge['duration']) == 0
            critical = abs(float(edge['TF'])) < 1e-8
            color = '#b62535' if critical else '#355f85'
            ax.annotate('', xy=right, xytext=left,
                        arrowprops=dict(arrowstyle='-|>', color=color,
                                        linestyle='--' if dummy else '-', lw=1.8,
                                        shrinkA=25, shrinkB=25))
            name = '' if dummy else '\n'+edge['name']
            text = f"{edge['id']} {float(edge['duration']):.2f} h{name}"
            x, y = (left[0]+right[0])/2, (left[1]+right[1])/2
            if i == 120 and j == 140:
                x += .4
            y += .48 if right[1] >= left[1] else -.48
            ax.text(x, y, text, ha='center', va='center', fontsize=9,
                    color=color, bbox=dict(facecolor='white', edgecolor='none', pad=1.5))
        for event, (x, y) in positions.items():
            e = events[event]
            ax.text(x, y, f"{event}\nE {float(e['E']):.2f}\nL {float(e['L']):.2f}",
                    ha='center', va='center', fontsize=8,
                    bbox=dict(boxstyle='circle,pad=.35', facecolor='#f6f8fa', edgecolor='#526272'))
        ax.set_xlim(-.8, max(x for x, _ in positions.values())+.8)
        ax.set_ylim(-1.5, 5.8)
        ax.axis('off')
    fig.suptitle('剩餘專案 AOA：活動在箭線、圓圈為事件｜草案 v0.2', fontsize=17)
    fig.legend(handles=[Line2D([], [], color='#b62535', label='零總浮時路徑'),
                        Line2D([], [], color='#355f85', label='其他活動'),
                        Line2D([], [], color='#526272', ls='--', label='0 h 虛活動')],
               loc='lower left', ncol=3)
    fig.text(.99, .015, 'E/L：事件最早／最晚有效工時；箭長不代表時間。未計資源容量與外部等待。',
             ha='right', fontsize=9)
    fig.savefig(ROOT/'aoa-network.svg')
    fig.savefig('/tmp/pynet-plan-aoa.png', dpi=110)
    plt.close(fig)


def gantt(source, output, capacity, title, dated=False):
    packages = rows('work-packages.csv')
    names = {p['package']: p['name'] for p in packages}
    order = list(names)
    colors = dict(D='#7054a1', P='#307ba5', H='#c66b19', X='#2a8163', G='#687582', M='#b62535')
    fig, ax = plt.subplots(figsize=(16, 9), layout='constrained')
    end = 0
    for item in rows(source):
        y = order.index(item['package'])
        for start, finish in json.loads(item['segments']):
            day = int(start//24)
            left, width = day+(start-day*24)/capacity, (finish-start)/capacity
            ax.broken_barh([(left,width)], (y-.32,.64), facecolors=colors[item['phase']])
            end = max(end, left+width)
    ax.set_yticks(range(len(order)), [f'{p}  {names[p]}' for p in order])
    ax.invert_yaxis()
    ax.set_xlim(0, int(end)+2)
    ax.set_xticks(range(0, int(end)+2, 5))
    ax.set_xlabel('工作日位置（0 為 D1 開始；空白代表時段／關卡等待）')
    ax.set_title(title, loc='left', fontsize=14)
    ax.grid(axis='x', alpha=.2)
    ax.set_axisbelow(True)
    labels = dict(D='D 設計', P='P 原型測試', H='H 人工接受', X='X 抽離', G='G 文件交付', M='M 合併')
    ax.legend(handles=[Patch(color=c, label=labels[k]) for k,c in colors.items()],
              loc='upper center', bbox_to_anchor=(.5,-.09), ncol=6, fontsize=9)
    if dated:
        dates = rows('accelerated-work-packages.csv')
        for p in dates:
            y = order.index(p['package'])
            ax.text(end+.3, y, p['finish'][5:], va='center', fontsize=8)
        ax.set_xlim(0,end+4)
    fig.savefig(ROOT/output)
    if dated:
        fig.savefig('/tmp/pynet-plan-accelerated.png', dpi=110)
    plt.close(fig)


if __name__ == '__main__':
    aoa()
    gantt('resource-schedule.csv', 'resource-gantt.svg', 4,
          '原容量比較：工程4 h／人工2 h，固定共同時段｜93工作日')
    gantt('accelerated-resource-schedule.csv', 'accelerated-gantt.svg', 8,
          '年底加速提案：工程8 h，指定關卡人工最多4 h｜38工作日，暫排12/17', dated=True)
