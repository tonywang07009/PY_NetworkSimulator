"""重算本資料夾的 AOA、CPM 與單一 change 在製排程；不是模擬器程式。"""
import csv
from datetime import date, timedelta
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def expected(triple):
    a, m, b = triple
    if not 0 <= a <= m <= b or not all(math.isfinite(x) for x in triple):
        raise ValueError(f'invalid estimate: {triple}')

    return (a + 4 * m + b) / 6


def cpm(edges, finish):
    nodes = sorted({n for edge in edges for n in (edge['i'], edge['j'])})
    early = {n: 0.0 for n in nodes}
    for edge in edges:
        if edge['i'] >= edge['j']:
            raise ValueError('events must be topologically numbered')

    if len({(e['i'], e['j']) for e in edges}) != len(edges):
        raise ValueError('duplicate event pair')

    for node in nodes:
        for edge in edges:
            if edge['i'] == node:
                early[edge['j']] = max(early[edge['j']], early[node] + edge['duration'])
    late = {n: early[finish] for n in nodes}
    for node in reversed(nodes):
        outgoing = [e for e in edges if e['i'] == node]
        if outgoing:
            late[node] = min(late[e['j']] - e['duration'] for e in outgoing)
    rows = []
    for edge in edges:
        es, ef = early[edge['i']], early[edge['i']] + edge['duration']
        lf = late[edge['j']]
        rows.append(dict(**edge, ES=es, EF=ef, LS=lf-edge['duration'], LF=lf,
                         TF=lf-ef, FF=early[edge['j']]-ef))
    return rows, early, late


def calendar(tasks, engineer=4, human=2, case='te', wait_days=0, boost_packages=(), boost_human=4, flexible=False):
    # 每日共同時段從第0小時開始；活動可跨日暫停；不平行處理不同change。
    now = 0.0
    human_used = {}
    result = []
    for task in tasks:
        if task['phase'] == 'M':
            # 人工合併之前的額外外部等待；每次等待完整工作日。
            now += wait_days * 24
        amount = task[case]
        human_capacity = boost_human if task['package'] in boost_packages else human
        capacity = min(engineer, human_capacity) if task['joint'] and not flexible else engineer
        start = None
        segments = []
        while amount > 1e-8:
            day = math.floor(now / 24 + 1e-10)
            offset = now - day * 24
            room = capacity-offset
            if task['joint'] and flexible:
                room = min(room, human_capacity-human_used.get(day, 0))
            if room <= 1e-8:
                now = (day + 1) * 24
                continue

            if start is None:
                start = now
            used = min(amount, room)
            if task['joint']:
                human_used[day] = human_used.get(day, 0) + used
            segments.append([now, now+used])
            amount -= used
            now += used
        result.append(dict(id=task['id'], package=task['package'], phase=task['phase'],
                           start_hour=start, finish_hour=now, segments=json.dumps(segments)))
    return result, now


def workdays(hour):
    return math.floor(hour / 24 + 1e-10) + (hour % 24) / 4


def write_csv(name, rows):
    with (ROOT / name).open('w', newline='', encoding='utf-8-sig') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def deadline_plan(tasks, critical):
    # 暫按臺灣政府日曆排休；不是使用者已確認的個人工作日曆。
    start, target = date(2026, 10, 26), date(2026, 12, 31)
    excluded = {date(2026, 10, 26), date(2026, 12, 25)}
    dates = []
    day = start
    while day <= target:
        if day.weekday() < 5 and day not in excluded:
            dates.append(day)
        day += timedelta(days=1)
    options = [
        ('原容量、共同時段固定', 4, 2, [], False),
        ('原容量、共同時段彈性', 4, 2, [], True),
        ('工程8h、人工仍2h', 8, 2, [], True),
        ('只加速技術關鍵包', 8, 2, critical, True),
        ('關鍵包加近關鍵CLM支路', 8, 2, critical+['W11', 'W14'], True),
    ]
    result = []
    selected = None
    for name, eng, hum, boost, flexible in options:
        schedule, end = calendar(tasks, engineer=eng, human=hum,
                                 boost_packages=boost, flexible=flexible)
        days = math.ceil(end/24)
        result.append(dict(option=name, engineer_daily_h=eng, human_normal_daily_h=hum,
                           human_boost_daily_h=4 if boost else hum, workdays=days,
                           available_workdays=len(dates), margin_days=len(dates)-days,
                           finish_date=dates[days-1].isoformat() if days <= len(dates) else '超過年底'))
        if name == '關鍵包加近關鍵CLM支路':
            selected = schedule
    write_csv('deadline-scenarios.csv', result)
    write_csv('accelerated-resource-schedule.csv', selected)
    by_id = {t['id']: t for t in tasks}
    human_days = {}
    engineering_days = {}
    for item in selected:
        for left, right in json.loads(item['segments']):
            number = math.floor(left/24)
            engineering_days[number] = engineering_days.get(number, 0) + right-left
            if by_id[item['id']]['joint']:
                entry = human_days.setdefault(number, dict(hours=0, activities=[]))
                entry['hours'] += right-left
                entry['activities'].append(item['id'])
    assert all(v <= 8+1e-8 for v in engineering_days.values())
    assert all(v['hours'] <= 4+1e-8 for v in human_days.values())
    assert math.isclose(sum(v['hours'] for v in human_days.values()),
                        sum(t['te'] for t in tasks if t['joint']))
    write_csv('accelerated-human-load.csv', [
        dict(day=k+1, date=dates[k].isoformat(), human_h=v['hours'],
             extra_over_2h=max(0, v['hours']-2), activities=' / '.join(v['activities']))
        for k, v in sorted(human_days.items())])
    lines = ['# 需要額外安排的人工加速日（提案）', '',
             '僅列超過原每日2 h的日期。D＝設計／決策，H＝導讀與接受，M＝人工合併核對。',
             '日期以10/27開工及暫用休假日曆試排；尚未獲確認，不是已安排的行事曆。', '',
             '| 日期 | 當日合計 | 超過2 h | 活動 |', '|---|---:|---:|---|']
    for k, v in sorted(human_days.items()):
        if v['hours'] > 2+1e-8:
            lines.append(f"| {dates[k]} | {v['hours']:.2f} h | {v['hours']-2:.2f} h | {'、'.join(v['activities'])} |")
    lines.extend(['', '完整負荷見 [CSV](accelerated-human-load.csv)；模組說明見 [加速計畫](05-year-end-acceleration.md)。', ''])
    (ROOT/'06-accelerated-days.md').write_text('\n'.join(lines))
    packages = []
    for p in dict.fromkeys(t['package'] for t in tasks):
        part = [s for s in selected if s['package'] == p]
        first, last = math.floor(part[0]['start_hour']/24), math.floor(part[-1]['finish_hour']/24)
        packages.append(dict(package=p, start=dates[first].isoformat(), finish=dates[last].isoformat()))
    write_csv('accelerated-work-packages.csv', packages)
    summary = dict(target=str(target), available_workdays=len(dates),
                   proposed_finish=result[-1]['finish_date'], reserve_workdays=result[-1]['margin_days'],
                   extra_human_days=sum(v['hours'] > 2+1e-8 for v in human_days.values()),
                   extra_human_hours=sum(max(0, v['hours']-2) for v in human_days.values()),
                   planned_total_human_hours=sum(v['hours'] for v in human_days.values()),
                   note='容量與共同時段彈性尚未獲確認；估算不含未量測的長時間CLM批次執行')
    (ROOT/'deadline-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n')


def main():
    data = json.loads((ROOT / 'schedule.json').read_text())
    engineer = data['capacities']['engineer_h_per_day']
    human = data['capacities']['human_h_per_day']
    if engineer != 4 or not 0 < human <= 24:
        raise ValueError('this draft uses a 4-hour engineering calendar; human capacity must be positive')

    phases = data['phases']
    tasks = []
    edges = []
    for package in data['packages']:
        for phase, triple in zip(phases, package['estimates'], strict=True):
            tasks.append(dict(id=f"{package['id']}-{phase['id']}", package=package['id'],
                              phase=phase['id'], joint=phase['joint'],
                              a=triple[0], m=triple[1], b=triple[2], te=expected(triple)))
        duration = sum(t['te'] for t in tasks if t['package'] == package['id'])
        edges.append(dict(id=package['id'], i=package['i'], j=package['j'],
                          name=package['name'], duration=duration))
    edges.extend(dict(id=f'D{k:02}', i=i, j=j, name='虛活動', duration=0.0)
                 for k, (i, j) in enumerate(data['dummies'], 1))
    rows, early, late = cpm(edges, data['finish'])
    assert all(r['TF'] >= -1e-8 and r['FF'] >= -1e-8 for r in rows)
    # 獨立菱形例：兩支路3h/5h，短支路浮時2h，專案5h。
    sample = [dict(id='A', i=0, j=1, duration=3), dict(id='B', i=0, j=2, duration=5),
              dict(id='D', i=1, j=2, duration=0)]
    proof, ee, _ = cpm(sample, 2)
    assert ee[2] == 5 and proof[0]['TF'] == 2
    write_csv('activities.csv', tasks)
    write_csv('cpm.csv', rows)
    write_csv('events.csv', [dict(event=n, E=early[n], L=late[n]) for n in early])
    expanded = []
    for number, package in enumerate(data['packages'], 1):
        ends = [package['i']*100] + [package['i']*100+number*6+k for k in range(1, 6)] + [package['j']*100]
        selected = [t for t in tasks if t['package'] == package['id']]
        for k, task in enumerate(selected):
            expanded.append(dict(id=task['id'], i=ends[k], j=ends[k+1], duration=task['te']))
    expanded.extend(dict(id=e['id'], i=e['i']*100, j=e['j']*100, duration=0)
                    for e in edges if not e['duration'])
    detail, detail_early, _ = cpm(expanded, data['finish']*100)
    assert detail_early[data['finish']*100] == early[data['finish']]
    write_csv('aoa-detail.csv', detail)
    schedule, end = calendar(tasks, human=human)
    by_id = {t['id']: t for t in tasks}
    for item in schedule:
        task = by_id[item['id']]
        cap = min(engineer, human) if task['joint'] else engineer
        assert item['start_hour'] % 24 < cap + 1e-8
        assert item['finish_hour'] % 24 <= cap + 1e-8
    write_csv('resource-schedule.csv', schedule)
    summary = dict(status='DRAFT', engineer_hours=sum(t['te'] for t in tasks),
                   human_hours=sum(t['te'] for t in tasks if t['joint']),
                   theoretical_cpm_hours=early[data['finish']],
                   critical_packages=[r['id'] for r in rows if r['duration'] and abs(r['TF']) < 1e-8],
                   scenarios={})
    for case in ['a', 'm', 'te', 'b']:
        _, finish = calendar(tasks, human=human, case=case)
        summary['scenarios'][case] = dict(workdays=workdays(finish), weeks=workdays(finish)/5)
    summary['capacity_sensitivity'] = {}
    for hours in [1, 2, 4]:
        _, finish = calendar(tasks, human=hours)
        summary['capacity_sensitivity'][str(hours)] = math.ceil(workdays(finish))
    summary['wait_sensitivity_days'] = {}
    for wait in [0, 1, 2]:
        _, finish = calendar(tasks, human=human, wait_days=wait)
        summary['wait_sensitivity_days'][str(wait)] = math.ceil(workdays(finish))
    summary['reserve_20_percent_days'] = math.ceil(workdays(end)*1.2)
    (ROOT / 'summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n')
    deadline_plan(tasks, summary['critical_packages'])
    package_rows = []
    cumulative_human = 0
    for p in data['packages']:
        selected = [t for t in tasks if t['package'] == p['id']]
        scheduled = [s for s in schedule if s['package'] == p['id']]
        human_h = sum(t['te'] for t in selected if t['joint'])
        cumulative_human += human_h
        package_rows.append(dict(package=p['id'], name=p['name'],
                                 **{t['phase']: t['te'] for t in selected},
                                 engineer_h=sum(t['te'] for t in selected), human_h=human_h,
                                 human_h_cumulative=cumulative_human,
                                 start_day=math.floor(scheduled[0]['start_hour']/24)+1,
                                 finish_day=math.ceil(workdays(scheduled[-1]['finish_hour']))))
    write_csv('work-packages.csv', package_rows)
    markdown = ['# AOA 主網路（彙總工作包）', '',
                '圓圈是事件；活動與期望工時標在箭線。虛線是 0 h 虛活動。單位是有效工作小時，箭長不代表時間。', '',
                '```mermaid', 'flowchart LR']
    for node in early:
        markdown.append(f'    E{node}(("{node}<br/>E {early[node]:.2f}<br/>L {late[node]:.2f}"))')
    for row in rows:
        label = f"{row['id']} {row['name']} / {row['duration']:.2f} h"
        arrow = f'-. "{label}" .->' if not row['duration'] else f'-->|"{label}"|'
        markdown.append(f"    E{row['i']} {arrow} E{row['j']}")
    markdown.extend(['```', '', '詳細數值見 [CPM表](cpm.csv)；實際單一change排程見 [資源排程](resource-schedule.csv)。', ''])
    (ROOT / 'aoa-network.md').write_text('\n'.join(markdown))
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
