import os

from includes.constants import LANGUAGES

src = 'folders.txt'
target = r'G:\My Drive\Web\ProductSearch.pw\Static'

for lang in LANGUAGES:
    path = os.path.join(target, lang[1])
    if not os.path.exists(path):
        os.mkdir(path)

