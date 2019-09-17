
# Lesson schedule parser
## Baranavichy State University lesson parser.

### Installation

Install the dependencies.

```sh
$ pip3 install bs4
$ pip3 install lxml
```
### Examples
```python
from schdl import *
from parser import *
import json

ft = get_facultets()[0] # Инженерный факультет
spec = get_specs(ft)[0] # Агрономия
group = get_groups(spec)[0] # Ас11
week = get_weeks()[2] # 2019-09-16

pairs = parse_pairs_by_day(group, week, day_number = 1)

js = json.dumps(pairs, separators=(',', ':'), ensure_ascii=False, indent = 4)

print(js)
```
