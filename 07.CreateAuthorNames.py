from random import randint, random

female_names_path = 'names/female.txt'
male_names_path = 'names/male.txt'
last_names_path = 'names/last.txt'

female_names = []
male_names = []
last_names = []

with open(female_names_path, 'r', encoding='utf-8') as f:
    for line in f:
        female_names.append(line.strip())

with open(male_names_path, 'r', encoding='utf-8') as f:
    for line in f:
        male_names.append(line.strip())

with open(last_names_path, 'r', encoding='utf-8') as f:
    for line in f:
        last_names.append(line.strip())

# Generate Female Author Names
female_probabilities = {
    'name_lastname': 0.70,
    'name_name_lastname': 0.90,
    'name_name_name_lastname': 0.93,
    'name_lastname_hyphen_lastname': 0.98,
    'name_name_lastname_hyphen_lastname': 0.99,
    'name_name_name_lastname_hyphen_lastname': 1.00
}

female_author_names = []

for i in range(0, 1000):
    lastname = last_names[randint(0, len(last_names)-1)]
    name = female_names[randint(0, len(female_names) - 1)]
    probability = random()
    if probability <= female_probabilities['name_lastname']:
        female_author_names.append(f'{name} {lastname}')
    elif probability <= female_probabilities['name_name_lastname']:
        name2 = female_names[randint(0, len(female_names) - 1)]
        while name2 == name:
            name2 = female_names[randint(0, len(female_names) - 1)]
        female_author_names.append(f'{name} {name2} {lastname}')
    elif probability <= female_probabilities['name_name_name_lastname']:
        name2 = female_names[randint(0, len(female_names) - 1)]
        while name2 == name:
            name2 = female_names[randint(0, len(female_names) - 1)]
        name3 = female_names[randint(0, len(female_names) - 1)]
        while name3 == name:
            name3 = female_names[randint(0, len(female_names) - 1)]
        female_author_names.append(f'{name} {name2} {name3} {lastname}')
    elif probability <= female_probabilities['name_lastname_hyphen_lastname']:
        lastname2 = last_names[randint(0, len(last_names)-1)]
        while lastname2 == lastname:
            lastname2 = last_names[randint(0, len(last_names)-1)]
        female_author_names.append(f'{name} {lastname}-{lastname2}')
    elif probability <= female_probabilities['name_name_lastname_hyphen_lastname']:
        name2 = female_names[randint(0, len(female_names) - 1)]
        while name2 == name:
            name2 = female_names[randint(0, len(female_names) - 1)]
        lastname2 = last_names[randint(0, len(last_names) - 1)]
        while lastname2 == lastname:
            lastname2 = last_names[randint(0, len(last_names) - 1)]
        female_author_names.append(f'{name} {name2} {lastname}-{lastname2}')
    elif probability <= female_probabilities['name_name_name_lastname_hyphen_lastname']:
        name2 = female_names[randint(0, len(female_names) - 1)]
        while name2 == name:
            name2 = female_names[randint(0, len(female_names) - 1)]
        name3 = female_names[randint(0, len(female_names) - 1)]
        while name3 == name:
            name3 = female_names[randint(0, len(female_names) - 1)]
        lastname2 = last_names[randint(0, len(last_names) - 1)]
        while lastname2 == lastname:
            lastname2 = last_names[randint(0, len(last_names) - 1)]
        female_author_names.append(f'{name} {name2} {lastname}-{lastname2}')
    else:
        raise Exception("Something went very wrong. Check your program logic.")

with open('1000_female_author_names.txt', 'w', encoding='utf-8') as f:
    for name in female_author_names:
        f.write(f'{name}\n')

# Generate Male Author Names
male_probabilities = {
    'name_lastname': 0.70,
    'name_name_lastname': 0.95,
    'name_name_name_lastname': 0.99,
    'name_lastname_hyphen_lastname': 0.995,
    'name_name_lastname_hyphen_lastname': 0.998,
    'name_name_name_lastname_hyphen_lastname': 1.0
}

male_author_names = []

for i in range(0, 1000):
    lastname = last_names[randint(0, len(last_names)-1)]
    name = male_names[randint(0, len(male_names) - 1)]
    probability = random()
    if probability <= male_probabilities['name_lastname']:
        male_author_names.append(f'{name} {lastname}')
    elif probability <= male_probabilities['name_name_lastname']:
        name2 = male_names[randint(0, len(male_names) - 1)]
        while name2 == name:
            name2 = male_names[randint(0, len(male_names) - 1)]
        male_author_names.append(f'{name} {name2} {lastname}')
    elif probability <= male_probabilities['name_name_name_lastname']:
        name2 = male_names[randint(0, len(male_names) - 1)]
        while name2 == name:
            name2 = male_names[randint(0, len(male_names) - 1)]
        name3 = male_names[randint(0, len(male_names) - 1)]
        while name3 == name:
            name3 = male_names[randint(0, len(male_names) - 1)]
        male_author_names.append(f'{name} {name2} {name3} {lastname}')
    elif probability <= male_probabilities['name_lastname_hyphen_lastname']:
        lastname2 = last_names[randint(0, len(last_names)-1)]
        while lastname2 == lastname:
            lastname2 = last_names[randint(0, len(last_names)-1)]
        male_author_names.append(f'{name} {lastname}-{lastname2}')
    elif probability <= male_probabilities['name_name_lastname_hyphen_lastname']:
        name2 = male_names[randint(0, len(male_names) - 1)]
        while name2 == name:
            name2 = male_names[randint(0, len(male_names) - 1)]
        lastname2 = last_names[randint(0, len(last_names) - 1)]
        while lastname2 == lastname:
            lastname2 = last_names[randint(0, len(last_names) - 1)]
        male_author_names.append(f'{name} {name2} {lastname}-{lastname2}')
    elif probability <= male_probabilities['name_name_name_lastname_hyphen_lastname']:
        name2 = male_names[randint(0, len(male_names) - 1)]
        while name2 == name:
            name2 = male_names[randint(0, len(male_names) - 1)]
        name3 = male_names[randint(0, len(male_names) - 1)]
        while name3 == name:
            name3 = male_names[randint(0, len(male_names) - 1)]
        lastname2 = last_names[randint(0, len(last_names) - 1)]
        while lastname2 == lastname:
            lastname2 = last_names[randint(0, len(last_names) - 1)]
        male_author_names.append(f'{name} {name2} {lastname}-{lastname2}')
    else:
        raise Exception("Something went very wrong. Check your program logic.")

with open('1000_male_author_names.txt', 'w', encoding='utf-8') as f:
    for name in male_author_names:
        f.write(f'{name}\n')

