import requests
from bs4 import BeautifulSoup

def get_facultets():
    url = "http://rasp.barsu.by/stud.php"
    html = requests.get(url).text
    
    bs_fts = BeautifulSoup(html, 'lxml').find('select', id='ft').find_all('option')
    fts = list(map(lambda x: x.text, bs_fts))

    return fts[1:]


def get_specs(ft):
    url = 'http://rasp.barsu.by/get_spec.php'
    params = dict(
        ft = ft
    )
    
    html = requests.get(url, params=params).text

    bs_specs = BeautifulSoup(html, 'lxml').find_all('option')
    specs = list(map(lambda x: x.text, bs_specs))

    return specs[1:]


def get_groups(spec):
    url = 'http://rasp.barsu.by/get_gp.php'
    params = dict(
        sp = spec
    )

    html = requests.get(url, params=params).text

    bs_groups = BeautifulSoup(html, 'lxml').find_all('option')
    groups = list(map(lambda x: x.text, bs_groups))
    
    return groups[1:]


def get_weeks():
    url = "http://rasp.barsu.by/stud.php"
    html = requests.get(url).text
    
    bs_nds = BeautifulSoup(html, 'lxml').find('select', {'name': 'nd'}).find_all('option')
    nds = list(map(lambda x: x.text, bs_nds))

    return nds[1:]