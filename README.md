
# Lesson schedule parser
## Baranavichy State University lesson parser.

### Installation

Install the dependencies.

```sh
$ pip3 install bs4
$ pip3 install lxml
```
### Examples:
```python
from schdl import *
from parser import *
import json

ft = get_facultets()[0] # Инженерный факультет
spec = get_specs(ft)[0] # Агрономия
group = get_groups(spec)[0] # Ас11
week = get_weeks()[2] # 2019-09-16

pairs = parse_pairs_by_day(group, week, day_numbers = (0))

js = json.dumps(pairs, separators=(',', ':'), ensure_ascii=False, indent = 4)

print(js)
```
### Examples 2:
```python3
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
```
