import requests
from bs4 import BeautifulSoup

def get_kafedrs():
    url = "http://rasp.barsu.by/teach.php"
    html = requests.get(url).text
    
    bs_fts = BeautifulSoup(html, 'lxml').find('select', id='kf').find_all('option')
    fts = list(map(lambda x: x.text, bs_fts))

    return fts[1:] 


def get_prepods(kf):
    url = 'http://rasp.barsu.by/get_tch.php'
    params = dict(
        kf = kf
    )
    
    html = requests.get(url, params=params).text

    bs_specs = BeautifulSoup(html, 'lxml').find_all('option')
    specs = list(map(lambda x: x.text, bs_specs))

    return specs[1:]

def is_valid_prepod(pr):
    for kf in get_kafedrs():
        for prepod in get_prepods(kf):
            if prepod.lower() == pr.lower():
                return True, prepod
    return False, None

def get_weeks():
    url = "http://rasp.barsu.by/teach.php"
    html = requests.get(url).text
    
    bs_nds = BeautifulSoup(html, 'lxml').find('select', {'name': 'nd'}).find_all('option')
    nds = list(map(lambda x: x.text, bs_nds))

    return nds[1:]