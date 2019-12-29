from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import sys
from schdl import get_weeks

def get_rasp_by_group(group, nd):
    url = "http://rasp.barsu.by/stud.php"
    payload = dict(
        ft = '0',
        sp = '0',
        gp = group,
        nd = nd,
    )

    html = requests.post(url, data = payload).text

    bs_rasp = BeautifulSoup(html, 'lxml').find('table', class_ = 'text table-bordered').find('tbody')

    return bs_rasp

def get_week_rasp(rasp):
    """Возвращает список (bs4) расписаний на неделю по дням"""
    splitted_rasp = []

    trs = rasp.find_all('tr', align='center')
    
    n = 0
    while n < 6*8:
        splitted_rasp.append(trs[n:8+n])
        n+=8

    return splitted_rasp

def get_days(rasp):
    """Возвращает список словарей с названиями дня недели и даты"""

    days = []
    week_rasp = get_week_rasp(rasp)

    for rasp_day in week_rasp:
        day_name, date = rasp_day[0].find_all('td')[:2]
            
        days.append({
            'day_name': day_name.text.strip(),
            'date': date.text.strip()
        })

    return days

def get_pairs_by_day(group, nd, day_numbers):
    """Возвращает список (bs4) пар на день"""
    rasp_html = get_rasp_by_group(group, nd)
    rasp = get_week_rasp(rasp_html)

    day_names = ('ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА')

    rasp_day = {}

    rasp_day['info'] = {
                        'group': group,
                        'week': nd,
                        }
    for day_number in day_numbers:
        day_name, date = rasp[day_number][0].find_all('td')[:2]

        rasp_day[f'day_{day_number}'] = {}
        
        rasp_day[f'day_{day_number}']['info'] = {
                                                'day_name': day_names[day_number], 
                                                'date': date.text.strip()
                                                }

        rasp_day[f'day_{day_number}']['pairs'] = {}

        headers = ('Подгр.', 'Время занятия', 'Дисциплина', 'Преподаватель', 'Аудитория')
        
        for pair in range(0, 8):
            html_by_day = rasp[day_number][pair]
            columns = html_by_day.find_all('td')[-5:]
            columns.insert(0, columns.pop(2))
            
            rasp_day[f'day_{day_number}']['pairs'][f'pair_{pair+1}'] = dict(zip(headers, columns))

    return rasp_day


def parse_pairs_by_day(group, nd, day_numbers):
    
    rasp_day = get_pairs_by_day(group, nd, day_numbers)

    for day_number in day_numbers:
        pairs = rasp_day.get(f'day_{day_number}').get('pairs')
        
        for pair in pairs.values():
            for key, value in pair.items():
                tmp_value = str(value).split('<br/>')
                tmp_value = list(map(lambda x: x.replace('<td>', '').replace('</td>', '').strip(), tmp_value))
                
                if key != 'Подгр.':
                    pair[key] = list(filter(None, tmp_value))
                else:
                    pair[key] = tmp_value

    return rasp_day

def get_schedule(group, nd, day_numbers):
    """Возвращает строку с расписанием на конкретные дни"""
    # ('❶', '❷', '❸', '❹', '❺', '❻', '❼', '❽')
    # ('①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧')
    # ('1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣')
    symbol_numbers = ('1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣')

    pairs = parse_pairs_by_day(group, nd, day_numbers)
                    
    pairs.__delitem__('info')

    for day in pairs.values():
        
        top = f"\n📌 {day['info']['day_name']} {day['info']['date']} 📌\n≋ƃ≋≋≋≋≋α≋≋≋≋≋ρ≋≋≋≋≋Г≋≋≋≋≋Ꮍ≋\n"
        txt_msg = top[:]
        day.__delitem__('info')

        for data_pair in day.values():
            
            for num, data in enumerate(data_pair.values()):
                count_pair = len(data['Дисциплина'])
                if count_pair < 1:
                    continue
                txt_msg += f'{symbol_numbers[num]} ►'
                txt_msg += ''.join(data['Время занятия'])
                txt_msg += '◄\n'
                data.__delitem__('Время занятия')
                for i in range(count_pair):
                    for num, (key, text) in enumerate(data.items()):
                        try:
                            if text[i]:
                                txt_msg += text[i]
                                if key == 'Подгр.':
                                    txt_msg += ' подгр. - '
                                else:
                                    txt_msg += ' ∘ '
                        except IndexError:
                            pass
                        
                    if count_pair > 1 and count_pair-i != 1:
                        txt_msg += '\n~~~'
                        
                    txt_msg += '\n'
                txt_msg += '\n' # ∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵
        if txt_msg == top:
            txt_msg += "🕺 Занятий нет! 🕺"

        yield txt_msg

def get_current_and_next_week():
    """Возвращает список с 2 элементами: расписание на текущую и следующую неделю"""

    now = datetime.strftime(datetime.utcnow() + timedelta(hours=3), '%Y-%m-%d')

    current_day, next_day = get_current_and_next_day()
    if current_day == 6:
        now = datetime.strftime(datetime.utcnow() + timedelta(hours=3) + timedelta(days = 1), '%Y-%m-%d')

    weeks = get_weeks()

    next_week = None
    current_week = None

    result = []
    now_str = ''.join(now.split('-'))
    
    if int(now_str) >= int(''.join(weeks[-1].split('-'))):
        return [weeks[-1], None]

    for week in weeks:
        week_str = ''.join(week.split('-'))
        if (int(week_str) <= int(now_str)):
            current_week = week[:]
            # continue
        else:
            result.append(current_week)
            next_week = week[:]
            result.append(next_week)
            break

    return result

def get_current_and_next_day():
    '''Возвращает список из номера текущего дня и следующего.'''
    
    datetime_now = datetime.utcnow() + timedelta(hours=3)
    weekday_current = datetime.weekday(datetime_now)
    weekday_next = datetime.weekday(datetime_now + timedelta(days = 1))

    return [weekday_current, weekday_next]