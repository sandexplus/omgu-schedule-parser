import re


def type(str):
    reg = "\([а-яА-Я]+\.\)"
    type_items = re.findall(reg, str)
    type_items = validate_items(type_items)
    if not type_items:
        pass
    else:
        type_items = replacer(type_items, ['(', ')']).title()
    return type_items


def subgroup(str):
    reg = "[0-9] п/г"
    subgroup_items = re.findall(reg, str)
    subgroup_items = validate_items(subgroup_items)
    subgroup_items = replacer(subgroup_items, ' п/г')
    return subgroup_items


def time(str):
    def hours(str):
        reg = "[0-9]+\."
        hours_items = re.findall(reg, str)
        return [replacer(hours_items[0], '.'), replacer(hours_items[1], '.')]

    def minutes(str):
        reg = "\.[0-9]+"
        minutes_items = re.findall(reg, str)

        return [replacer(minutes_items[0], '.'), replacer(minutes_items[1], '.')]

    time_items = {
        'start': {
            'hours': hours(str)[0],
            'minutes': minutes(str)[0]
        },
        'end': {
            'hours': hours(str)[1],
            'minutes': minutes(str)[1]
        }
    }
    return time_items


def week(str):
    outer_reg = "[0-9]+.+нед"
    weeks_str = re.findall(outer_reg, str)
    weeks_str = validate_items(weeks_str)
    reg = "[0-9]+-{0,1}[0-9]*"
    weeks_items = re.findall(reg, weeks_str)

    def compile(weeks):
        weeks_obj = []

        start_reg = "^[0-9]+"
        end_reg = "[0-9]+$"

        for week_iter in weeks:
            week_item_start = re.findall(start_reg, week_iter)
            week_item_start = validate_items(week_item_start)

            week_item_end = re.findall(end_reg, week_iter)
            week_item_end = validate_items(week_item_end)

            weeks_obj.append([week_item_start, week_item_end])

        return weeks_obj

    weeks_arr = compile(weeks_items)

    return weeks_arr


def even_odd(str):
    reg = "[чн]/н "
    even_odd_items = re.findall(reg, str)
    even_odd_items = validate_items(even_odd_items)
    return even_odd_items


def lesson(str):
    reg = " [а-яА-Яa-zA-Z: -]+\(| [а-яА-Яa-zA-Z: -]+\({0,1}$"
    lesson_items = re.findall(reg, str)
    lesson_items = validate_items(lesson_items)
    lesson_items = replacer(lesson_items, ['(']).strip()
    return lesson_items


def cabinet(str):
    reg = ", [0-9\-]+$|, [а-яА-Я 0-9]+\.{0,1}$"
    cabinet_items = re.findall(reg, str)
    cabinet_items = validate_items(cabinet_items).strip()
    cabinet_items = replacer(cabinet_items, [', '])
    return cabinet_items


def teacher(str):
    reg = "[А-Я][а-яА-Я \.]+,"
    teacher_items = re.findall(reg, str)
    teacher_items = validate_items(teacher_items)
    teacher_items = replacer(teacher_items, [','])
    return teacher_items


def group_name(str):
    reg = "[а-яА-Я]{1,3}-.+$"
    group_name_items = re.findall(reg, str)
    group_name_items = validate_items(group_name_items)
    return group_name_items


def chosen_lesson(str):
    reg = "\(курс по выбору\)"
    chosen_lesson_items = re.findall(reg, str)
    chosen_lesson_items = validate_items(chosen_lesson_items)
    return bool(chosen_lesson_items)


def validate_items(items):
    if items:
        return items[0]
    else:
        return ''


def replacer(str, replaces):
    new_str = str
    for replace_item in replaces:
        new_str = new_str.replace(replace_item, '')

    return new_str
