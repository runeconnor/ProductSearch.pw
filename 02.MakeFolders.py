import os.path

import includes.functions as fun

root = r"D:\wamp64\www\ProductSearch.pw"

subfolders = fun.get_subfolders(root)

for folder in subfolders:
    keywords_file_path = folder + r"\subdirs.txt"

    if os.path.exists(keywords_file_path):
        folders_and_keywords = fun.create_subfolders(folder, keywords_file_path)
