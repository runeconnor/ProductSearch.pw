names_paths = [
    'names/1960.txt',
    'names/1970.txt',
    'names/1980.txt',
    'names/1990.txt',
    'names/2000.txt',
    'names/2010.txt'
]

last_names_path = 'names/last.txt'

female = []
male = []
last = []

for names_file in names_paths:
    with open(names_file, 'r', encoding='utf-8') as file:
        for line in file:
            line_list = line.strip().split(',')
            if line_list[1] == 'F':
                if line_list[0] not in female:
                    female.append(line_list[0])
            elif line_list[1] == 'M':
                if line_list[0] not in male:
                    male.append(line_list[0])

with open(last_names_path, 'r', encoding='utf-8') as file:
    for last_name in file:
        ln = last_name.strip().lower().capitalize()
        last.append(ln)

with open('female.txt', 'w', encoding='utf-8') as f:
    for name in female:
        f.write(name+'\n')

with open('male.txt', 'w', encoding='utf-8') as f:
    for name in male:
        f.write(name+'\n')

with open('last.txt', 'w', encoding='utf-8') as f:
    for name in last:
        f.write(name + '\n')



