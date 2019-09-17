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