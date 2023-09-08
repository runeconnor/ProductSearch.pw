import os
from glob import glob
import markdown as md

from includes.constants import ConsoleColors
from includes.functions import php_add_slashes, php_generate_index_php

source = "G:\\My Drive\\Web\\ProductSearch.pw\\Grav\\user\\pages"
target = "D:\\wamp64\\www"

"""
# Get source files
src_files = {
    'L1': glob(f'{source}\\*\\*.md'),
    'L2': glob(f'{source}\\*\\*\\*.md'),
    'L3': glob(f'{source}\\*\\*\\*\\*.md'),
    'L4': glob(f'{source}\\*\\*\\*\\*\\*.md'),
}
for key in src_files.keys():
    with open(f'{key}.txt', 'w', encoding='utf-8') as f:
        for file in src_files[key]:
            f.write(file + '\n')
        print(key, '-- OK')
"""

# Parse source files
lf = 'L4.txt'
with open(lf, 'r', encoding='utf-8') as link_file:
    title = {}
    contents = {}
    if lf == "L1.txt":
        root_path = '../'
    elif lf == "L2.txt":
        root_path = '../../'
    elif lf == "L3.txt":
        root_path = '../../../'
    elif lf == "L4.txt":
        root_path = '../../../../'
    meta_php = f'<?php\n\n$rootpath = "{root_path}";\n$title = [];\n'
    contents_php = """<?php
if (isset($_GET["l"])) {
    switch ($_GET["l"]) {
        """

    link_file_contents_list = link_file.readlines()
    link_file.seek(0)
    slugs = []
    link_idx = 0
    for path in link_file:
        target_folder = target
        source_path = path.strip()
        ln = path.split('\\')
        file_name = ln[-1]
        ln = ln[7:len(ln) - 1]
        folders = []
        for folder in ln:
            folders.append(folder[6:])

        language_code = file_name[-6:-4]

        slug = folders[-1]
        new_folder = False
        if slugs and slug != slugs[-1]:
            new_folder = True
        slugs.append(slug)

        if new_folder:
            title = {}
            contents = {}
            meta_php = f'<?php\n\n$rootpath = "{root_path}";\n$title = [];\n'
            contents_php = """<?php
if (isset($_GET["l"])) {
    switch ($_GET["l"]) {
        """

        with open(source_path, 'r', encoding='utf-8') as md_f:
            cnt = 0
            in_yaml = False
            yaml_exists = False
            title[language_code] = ''

            # Get title if it exists in yaml
            for line in md_f:
                if cnt == 0 and line == '---\n':
                    yaml_exists = True
                    in_yaml = True
                if in_yaml:
                    if cnt != 0 and line == '---\n':
                        in_yaml = False
                        yaml_close_idx = cnt + 1
                    if line[:5] == 'title':
                        title[language_code] = line[7:].strip()
                cnt += 1

            # Remove page yaml
            if yaml_exists:
                md_f.seek(0)
                for i in range(yaml_close_idx):
                    next(md_f)
                contents[language_code] = md_f.read()
            else:
                contents[language_code] = md_f.read()

            # Change image paths
            contents[language_code] = contents[language_code].replace('image://profiles/female/',
                f'{root_path}_img/profiles/f/')
            contents[language_code] = contents[language_code].replace('image://profiles/male/',
                f'{root_path}_img/profiles/m/')

            # Convert markdown to html
            html = md.markdown(contents[language_code])

            # Add css class to profile images
            html = html.replace(r'.jpg" />', r'.jpg" class="profile">').replace(r'<p></p>', '')

            # Remove rogue <hr />s
            html = html.replace(r'<hr />', r'')

        h1_start_idx = html.find('<h1>')
        h1_end_idx = html.find('</h1>')
        # If no title in yaml, first h1 is title
        if not title[language_code]:
            title[language_code] = html[h1_start_idx + 4:h1_end_idx]

        # Add image under h1
        contents[language_code] = html[:h1_end_idx + 5] \
                                  + f'\n<img alt="{title[language_code]}" src="{slug}.jpg" class="img_below_h1">' \
                                  + html[h1_end_idx + 5:]

        # Add article div
        contents[language_code] = r'<div class="article">' + contents[language_code] + r'</div>'

        # Append to file contents
        if link_idx < len(link_file_contents_list) - 1:
            next_slug = link_file_contents_list[link_idx + 1].strip().split('\\')[-2][6:]
        else:
            next_slug = ''
        if slug == next_slug:  # Adding translations
            contents_php += f'case "{language_code}":\n' \
                            f'            echo "{php_add_slashes(contents[language_code])}";\n' \
                            f'            break;\n        '
            meta_php += f'$title["{language_code}"] = "{php_add_slashes(title[language_code])}";\n'
        else:  # No more translations, so default is English
            contents_php += f'    }}\n}} else {{\n    echo "{php_add_slashes(contents["en"])}";\n}}\n?>'
            meta_php += '\n$page_title = $title["en"];\n$page_language = "en";\nif (isset($_GET["l"])) {\n' \
                        '    $page_title = $title[$_GET["l"]];\n$page_language = $_GET["l"];\n}\n?>'
            index_php = php_generate_index_php(root_path)
            for folder in folders:
                target_folder += f'\\{folder}'
            print(f'{ConsoleColors.OKCYAN}{target_folder} -- OK{ConsoleColors.ENDC}')

            # Write everything to files
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)

            target_file = f'{target_folder}\\contents.php'
            with open(target_file, 'w', encoding='utf-8') as file:
                file.write(contents_php)
                print(f'{target_file} -- Written')

            target_file = f'{target_folder}\\meta.php'
            with open(target_file, 'w', encoding='utf-8') as file:
                file.write(meta_php)
                print(f'{target_file} -- Written')

            target_file = f'{target_folder}\\index.php'
            with open(target_file, 'w', encoding='utf-8') as file:
                file.write(index_php)
                print(f'{target_file} -- Written')

        link_idx += 1

print(f'\n{ConsoleColors.OKGREEN}ALL DONE!{ConsoleColors.ENDC}')
