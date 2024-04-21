import jsonlines
import sys
import os
import random
from time import sleep


random.seed(42)

a_file = sys.argv[1]
b_file = sys.argv[2]
c_file = sys.argv[3]

a_list = []
b_list = []

with jsonlines.open(a_file) as reader:
    for obj in reader:
        obj['from'] = 'a'
        a_list.append(obj)

with jsonlines.open(b_file) as reader:
    for obj in reader:
        obj['from'] = 'b'
        b_list.append(obj)

c_list = [(a,b) if random.randint(0, 1)==1 else (b,a) for a, b in zip(a_list, b_list)]

print(c_list)
length = len(c_list)
with jsonlines.open(c_file, mode='w') as writer:
    for n, (a, b) in enumerate(c_list):
        win = ''
        while win != '1' and win != '2' and win != 'b' and win != 'n':
            os.system('clear')
            print(f'---\n{n+1}/{length}\n---\n')
            print('Question:')
            print(a['input'])
            print(b['input'])
            print()
            print('1.:\n***')
            print(a['output'])
            print('***\n\n')
            print('2.:\n***')
            print(b['output'])
            print('***')
            print()
    
            win = input('Which is better? 1., 2., both, neither [1,2,b,n]: ').strip().lower()
        win_name = ''
        win_file = ''
        if win == '1':
            win_name = a['from']
        elif win == '2':
            win_name = b['from']
        if win_name == 'a':
            win_file = a_file
        elif win_name == 'b':
            win_file = b_file
        writer.write({'1': a, '2': b, 'win': win, 'win_file': win_file})

        print(win_file)

        sleep(1)

