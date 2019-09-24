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

def is_valid_group(gr):
    # for ft in get_facultets():
    #     for spec in get_specs(ft):
    #         for group in get_groups(spec):
    #             if group.lower() == gr.lower():
    #                 return True
    # return False

    groups = [
        'Ас11', 'Ас21', 'Ас31', 'ИСТ11', 'ИСТ21', 'ИСТ31', 'ИСТ41', 'ТОСП11', 'ТОСП21', 'ТОСП31', 
        'ТОСПс11', 'ТОСПс21', 'ТО41', 'ТО51', 'ТМ11', 'ТМ21', 'ТМ31', 'ТМ41', 'ТМ51', 'ТМзс11', 
        'ДОз217', 'ПДз119', 'ППз218', 'ГЭ11', 'ГЭ21', 'ГЭ31', 'ГЭ41', 'ДО11', 'ДО21', 'ДО31', 
        'ДО41', 'ДОз31', 'НО11', 'НО21', 'НО31', 'НО41', 'ОТИ11', 'ОТИ21', 'ОТИ31', 'ОТИ41',
        'ПП11', 'ПП21', 'ПП31', 'ПП41', 'ППз31', 'СП11', 'СП21', 'СП31', 'СП41', 'СПД11', 
        'ТиМОВм11', 'ФК11', 'ФК21', 'ФК31', 'ФК41', 'БИЯ11', 'БИЯ21', 'БИЯ31', 'ИЯ11', 'ИЯ21',
        'ИЯ22', 'ИЯ31', 'ИЯ32', 'ИЯ41', 'НА11', 'НА21', 'СИЯ11', 'СИЯ12', 'СИЯ13', 'СИЯ21', 
        'СИЯ22', 'СИЯ23', 'СИЯ31', 'СИЯ32', 'СИЯ33', 'СИЯ41', 'СИЯ42', 'СИЯ43', 'Б31', 'БА11', 
        'БА21', 'БА31', 'БА41', 'БАздс21', 'БАздс31', 'М41', 'Мзд41', 'Мздс21', 'Мздс31', 'ПХ11', 
        'ПХ21', 'ПХ22', 'ПХ31', 'ПХ32', 'ПХ41', 'ПХ42', 'ПХздс31', 'ЭОП31', 'ЭОП41', 'ЭОП51', 
        'ЭТ41', 'ЭП11', 'ЭП21', 'ЭП31', 'ЭМ11', 'ЭМ21', 'ЭМ31']

    lower_groups = list(map(lambda x: x.lower(), groups))

    if gr in lower_groups:
        return True, groups[lower_groups.index(gr)]
    else:
        return False, None

def get_weeks():
    url = "http://rasp.barsu.by/stud.php"
    html = requests.get(url).text
    
    bs_nds = BeautifulSoup(html, 'lxml').find('select', {'name': 'nd'}).find_all('option')
    nds = list(map(lambda x: x.text, bs_nds))

    return nds[1:]