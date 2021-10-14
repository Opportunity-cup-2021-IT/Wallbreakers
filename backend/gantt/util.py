import pandas as pd
import numpy as np
import re
import sys
import datetime
from gantt import Task

sys.setrecursionlimit(1000000)


def get_child(child, activity_field):
    text = child.find(activity_field).text
    if text is None:
        return None
    return int(text)


def clean_csv(filename):
    """
    Функция очищает входные данные: форматирует дату, очищает тип связи,
    удаляет пустые строки и восстанавливает потерянные данные.
    """
    dt = pd.read_csv(filename, index_col='ID')

    for i in ['НН', 'ОН', 'ОО', 'НО', re.compile('[-+]\d+д')]:
        for j in ['Предшественники', 'Последователи']:
            dt[j] = dt[j].str.replace(i, '', regex=True)

    aga = {' Январь ': '.01.', ' Февраль ': '.02.', ' Март ': '.03.', ' Апрель ': '.04.', ' Май ': '.05.',
           ' Июнь ': '.06.', ' Июль ': '.07.', ' Август ': '.08.', ' Сентябрь ': '.09.', ' Октябрь ': '.10.',
           ' Ноябрь ': '.11.', ' Декабрь ': '.12.'}

    for old, new in aga.items():
        dt['Начало'] = dt['Начало'].str.replace(old, new, regex=True)
        dt['Окончание'] = dt['Окончание'].str.replace(old, new, regex=True)

    dt['Длительность'] = dt['Длительность'].str.replace('д', '')

    for task in dt.index:
        for i in ['Предшественники', 'Последователи']:
            if dt[i][task] is np.nan:
                dt[i][task] = ''

    dt = dt.dropna()

    for i in ['Предшественники', 'Последователи']:
        for task in dt.index:
            if dt[i][task].find('...') >= 0:
                dt[i][task] = dt[i][task].replace('...', '')
                for task_find in dt.index:
                    if dt[list({'Предшественники', 'Последователи'} - {i})[0]][task_find].find(str(task)) >= 0:
                        dt[i][task] = dt[i][task] + str(task_find) + ';'
    return dt


def next_(row):
    return [int(i) for i in row.split(';') if i and i != 'nan']


def get_first_elem_in_lst(row):
    if row == row:
        return row[0]
    return None


def read_csv(filename):
    """
    Функция форматирует дату и приводит таблицу к рабочему виду.
    """
    dt = clean_csv(filename)
    date = datetime.datetime(1990, 1, 1)
    dt['Начало'] = (pd.to_datetime(dt['Начало']) - date).dt.days
    dt['Окончание'] = (pd.to_datetime(dt['Окончание']) - date).dt.days
    dt['Длительность'] = dt['Длительность'].str.split(',').apply(get_first_elem_in_lst).astype(int)
    dt['lag'] = 0
    dt['Последователи'] = dt['Последователи'].astype(str).fillna('').apply(next_)
    dt['costs'] = 1
    dt.loc[dt['Длительность'] == 0, 'costs'] = 1000
    dt.drop(['Предшественники'], axis=1, inplace=True)
    return dt.rename(columns={'ID': 'id',
                              'Длительность': 'duration',
                              'Последователи': 'nexts',
                              'Начало': 'start_date',
                              'Окончание': 'finish_date'}).astype(int, errors='ignore')


def df2model(df: pd.DataFrame):
    """
    Преобразует dataframe в модель графа.
    """
    schedule = {}
    next = {}
    for i, row in df.iterrows():
        a = Task(i, schedule, row.start_date, row.finish_date, row.duration, row.lag)
        schedule[i] = a
        next[i] = row.nexts
    for k in schedule:
        for n in next[k]:
            if k not in schedule or n not in schedule:
                print(f"Task does not exists! {n} {k}")
                continue
            schedule[k].append_next(n)
            print(schedule[k], n)
    return schedule


def model2df(start: int, act_db: dict):
    """
    Преобразует модель графа в dataframe.
    """
    q = [start]
    model2df_used = set()
    mdl_list = []
    while len(q) > 0:
        a = q.pop()
        if a in model2df_used:
            continue
        model2df_used.add(a)
        act = act_db[a]
        nexts = act.next_activity
        mdl_list.append([act.id, act.start_date, act.finish_date, act.duration, 0, [e for e in nexts],
                     1000 if act.duration == 0 else 1])
        for ina in nexts:
            if ina not in model2df_used:
                q.append(ina)
    return pd.DataFrame(mdl_list, columns=['id', 'start_date', 'finish_date', 'duration', 'lag', 'nexts', 'cost'])


def modelDict2df(sch: dict):
    """
    Преобразует словарь в dataframe.
    """
    dt = pd.DataFrame(columns=['id', 'start_date', 'finish_date', 'duration', 'lag', 'nexts', 'cost'])
    dt.id = dt.id.astype(int)
    dt.start_date = dt.start_date.astype(int)
    dt.finish_date = dt.finish_date.astype(int)
    dt.duration = dt.duration.astype(int)
    ss = set()
    for k in sch.keys():
        if k not in ss:
            try:
                model_df = model2df(k, sch)
            except KeyError:
                print(f"Task doesn't not exists: {k}")
                continue
            dt = pd.concat([dt, model_df], axis=0)
            idset = set(model_df.id)
            ss = ss.union(idset)
    return dt



