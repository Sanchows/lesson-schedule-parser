from parser import *

pairs = parse_pairs_by_day('ИСТ41', '2019-09-16', day_numbers = (0,1,2,3,4))

pairs.__delitem__('info')

for day in pairs.values():
    print('\n')
    print(f"{day['info']['day_name']} {day['info']['date']}")

    day.__delitem__('info')

    for data_pair in day.values():
        for data in data_pair.values():
            for header, text in data.items():
                print(f'{header}: {text}', end = '|')

            print('\n********')