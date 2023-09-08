from includes.constants import *

# CHANGE THESE AS NEEDED
ITEM_TYPE = 'blog'  # 'blog' or 'item'
PARENT_DIR_PATH = PATH_PAGES + "\\00008.beauty-personal-care"
KEYWORDS_FILE_PATH = "folders.txt"
NUM_PROFILE_IMAGES = {
    'male': 271,
    'female': 256
}

NUM_THREADS = 32
API_CALL_DELAY = 1.2  # seconds
NUM_LANGUAGES = 1

MODEL = 'gpt-3.5-turbo'
ARTICLE_TEMPERATURE = TEMPERATURE['balanced']
USER_COMMENTS_TEMPERATURE = TEMPERATURE['creative']
