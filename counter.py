import jsonlines
import sys
from collections import Counter

a_file = sys.argv[1]
a_list = []
with jsonlines.open(a_file) as reader:
    for obj in reader:
        a_list.append(obj)

print([a['win_file'] for a in a_list])

c = Counter([a['win_file'] for a in a_list])

print(c)
print(c.most_common())
