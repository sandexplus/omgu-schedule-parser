import urllib.request
from bs4 import BeautifulSoup
import json
import urllib.request
from pprint import pprint
import analyze
from itertools import product
import numpy as np

import ftp

need_to_load = True


def table_to_2d(table_tag):
    rowspans = []  # track pending rowspans
    rows = table_tag.find_all('tr')

    colcount = 0
    for r, row in enumerate(rows):
        cells = row.find_all(['td', 'th'], recursive=False)
        colcount = max(
            colcount,
            sum(int(c.get('colspan', 1)) or 1 for c in cells[:-1]) + len(cells[-1:]) + len(rowspans))

        rowspans += [int(c.get('rowspan', 1)) or len(rows) - r for c in cells]
        rowspans = [s - 1 for s in rowspans if s > 1]

    # it doesn't matter if there are still rowspan numbers 'active'; no extra
    # rows to show in the table means the larger than 1 rowspan numbers in the
    # last table row are ignored.

    # build an empty matrix for all possible cells
    table = [[None] * colcount for _ in rows]

    # fill matrix from row data
    rowspans = {}  # track pending rowspans, column number mapping to count
    for row, row_elem in enumerate(rows):
        span_offset = 0  # how many columns are skipped due to row and colspans
        for col, cell in enumerate(row_elem.find_all(['td', 'th'], recursive=False)):
            # adjust for preceding row and colspans
            col += span_offset
            while rowspans.get(col, 0):
                span_offset += 1
                col += 1

            # fill table data
            rowspan = rowspans[col] = int(cell.get('rowspan', 1)) or len(rows) - row
            colspan = int(cell.get('colspan', 1)) or colcount - col
            # next column is offset by the colspan
            span_offset += colspan - 1
            value = cell.get_text()
            for drow, dcol in product(range(rowspan), range(colspan)):
                try:
                    table[row + drow][col + dcol] = value
                    rowspans[col + dcol] = rowspan
                except IndexError:
                    # rowspan or colspan outside the confines of the table
                    pass

        # update rowspan bookkeeping
        rowspans = {c: s - 1 for c, s in rowspans.items() if s > 1}

    # pprint(table)

    return table


def start_parser():
    links = [
        'http://fkn.omsu.ru/academics/Schedule/schedule1_1.htm',
        'http://fkn.omsu.ru/academics/Schedule/schedule2_1.htm',
        'http://fkn.omsu.ru/academics/Schedule/schedule3_1.htm',
        'http://fkn.omsu.ru/academics/Schedule/schedule4_1.htm',
        'http://fkn.omsu.ru/academics/Schedule/schedule5_1.htm',
        'http://fkn.omsu.ru/academics/Schedule/schedulemi_1.htm'
    ]

    for i in range(len(links)):
        fp = urllib.request.urlopen(links[i])
        mybytes = fp.read()
        mystr = mybytes.decode("windows-1251")
        table_list = table_to_2d(BeautifulSoup(mystr, features="html.parser"))
        generate_obj(table_list, i)
    ftp.upload_file(None, len(links), need_to_load)


def generate_obj(table_data, idx):
    global_json = {}

    def init_json():
        for group_idx, group_item in enumerate(table_data[0]):
            if group_idx == 0:
                continue
            if group_idx > 1:
                group_name = analyze.group_name(group_item)
                global_json[group_name] = {}

                for row in range(len(table_data) - 1):
                    time = table_data[row + 1][1]
                    day = table_data[row + 1][0]
                    if day not in global_json[group_name]:
                        global_json[group_name][day] = []
                    for cell in range(len(table_data[row + 1]) - 2):
                        item = table_data[row + 1][group_idx]
                        if cell + 2 != group_idx or not item:
                            continue
                        global_json[group_name][day].append(make_obj_by_string(item, time))

    def clear_json():
        for group_name in global_json:
            for day_name in global_json[group_name]:
                item = global_json[group_name][day_name]
                global_json[group_name][day_name] = [i for n, i in enumerate(item) if i not in item[n + 1:]]

    init_json()
    clear_json()
    create_json_file(global_json, idx)


def create_json_file(obj, idx):
    with open(f"data{idx}.json", "w", encoding='utf-8') as jsonfile:
        json.dump(obj, jsonfile, ensure_ascii=False)
    ftp.upload_file(idx, 0, need_to_load)


def make_obj_by_string(str, time_str):
    if str == '' or not str or time_str == '' or not time_str:
        return None
    obj = {
        'type': analyze.type(str),
        'subgroup': analyze.subgroup(str),
        'week': analyze.week(str),
        'even_odd': analyze.even_odd(str),
        'lesson': analyze.lesson(str),
        'cabinet': analyze.cabinet(str),
        'teacher': analyze.teacher(str),
        'time': analyze.time(time_str),
        'chosen_lesson': analyze.chosen_lesson(str)
    }

    return obj
