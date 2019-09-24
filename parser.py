from bs4 import BeautifulSoup
import requests
import sys

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

    rasp_day = {}

    rasp_day['info'] = {
                        'group': group,
                        'week': nd,
                        }
    for day_number in day_numbers:
        day_name, date = rasp[day_number][0].find_all('td')[:2]

        rasp_day[f'day_{day_number}'] = {}
        
        rasp_day[f'day_{day_number}']['info'] = {
                                                'day_name': day_name.text.strip(), 
                                                'date': date.text.strip()
                                                }

        rasp_day[f'day_{day_number}']['pairs'] = {}

        headers = ('Время занятия', 'Дисциплина', 'Подгр.', 'Преподаватель', 'Аудитория')
        
        for pair in range(0, 8):
            html_by_day = rasp[day_number][pair]
            columns = html_by_day.find_all('td')[-5:]
            
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
                pair[key] = list(filter(None, tmp_value))

    return rasp_day

def get_schedule(group, nd, day_numbers):

    symbol_numbers = ('①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧')
    symbol_numbers_v2 = ('❶', '❷', '❸', '❹', '❺', '❻', '❼', '❽')

    txt_msg = ""

    pairs = parse_pairs_by_day(group, nd, day_numbers)
                    
    pairs.__delitem__('info')

    for day in pairs.values():
        
        txt_msg += f"\n📌 {day['info']['day_name']} {day['info']['date']} 📌\n≋ᴮ≋≋≋≋≋ᴬ≋≋≋≋≋ᴿ≋≋≋≋≋ᴳ≋≋≋≋≋ᵁ≋\n"

        day.__delitem__('info')

        for data_pair in day.values():
            
            for num, data in enumerate(data_pair.values()):
                count_pair = len(data['Дисциплина'])
                if count_pair < 1:
                    continue
                txt_msg += f'{symbol_numbers[num]} ПАРА ►'
                txt_msg += ''.join(data['Время занятия'])
                txt_msg += '◄\n'
                data.__delitem__('Время занятия')

                for i in range(count_pair):
                    for num, text in enumerate(data.values()):
                        try:
                            txt_msg += text[i]
                            if num < 3:
                                txt_msg += ' ∘ '
                        except IndexError:
                            pass
                    if count_pair > 1 and count_pair-i != 1:
                        txt_msg += '\n~~~'
                        
                    txt_msg += '\n'
                txt_msg += '∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵∴∵\n'
    
    return txt_msg