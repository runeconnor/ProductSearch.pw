import time
from concurrent.futures import ThreadPoolExecutor

from includes.parameters import *
import includes.functions as f

import openai

openai.api_key = API_KEY
languages = LANGUAGES[:NUM_LANGUAGES]
global_cnt = 0

folders_and_keywords = f.create_subfolders(PARENT_DIR_PATH, KEYWORDS_FILE_PATH)
num_all_items = len(folders_and_keywords) * NUM_LANGUAGES
all_items = []
for language, language_code in languages:
    for folder, keyword in folders_and_keywords:
        all_items.append((folder, keyword, language, language_code, PARENT_DIR_PATH,
                          ARTICLE_TEMPERATURE, USER_COMMENTS_TEMPERATURE, ITEM_TYPE, num_all_items))

avg_len = num_all_items // NUM_THREADS

# Lists to be executed by each thread
sublists = [all_items[i:i + avg_len] for i in range(0, num_all_items, avg_len)]

# Add any remaining items to sublists
if num_all_items % NUM_THREADS != 0:
    sublists[-1].extend(all_items[NUM_THREADS * avg_len:])

# Execute
with ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
    for sublist in sublists:
        executor.map(f.write_article, sublist)
        time.sleep(API_CALL_DELAY)

print(f'\n{ConsoleColors.OKGREEN}ALL DONE!{ConsoleColors.ENDC}')
