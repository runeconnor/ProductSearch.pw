import os
import shutil

next_num = 169
source = r'G:\My Drive\Web\ProductSearch.pw\Images\ai_generated\profiles\f'
destination = r'G:\My Drive\Web\ProductSearch.pw\Images\ai_generated\profiles\female'
src_files = os.listdir(source)

for idx, name in enumerate(src_files):
    num = next_num + idx
    src = f'{source}\\{name}'
    dst = f'{destination}\\{num}.jpg'

    shutil.copy(src, dst)

