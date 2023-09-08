read_path = r'cats/_main.txt'
cats = []
with open(read_path, 'r', encoding='utf-8') as f:
    for line in f:
        catlist = line.strip(' \ufeff').split(',')
        if catlist[1] == cat:
            if catlist[2] not in cats:
                cats.append(catlist[2])

with open('cats/_main.txt', 'w', encoding='utf-8') as f:
    for cat in cats:
        f.write(cat+'\n')
