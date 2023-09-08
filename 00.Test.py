import openai

from includes.parameters import *
from includes.functions import call_openai_api, parse_article_title

openai.api_key = API_KEY
system_prompt = SYSTEM_PROMPT
user_prompt = ARTICLE_TITLE_PROMPT
model = "gpt-3.5-turbo"
temperature = TEMPERATURE["creative"]
keyword = """noco jump starter"""
language = "Russian"


content = call_openai_api(system_prompt, user_prompt, model, temperature,
                          keyword, language)

head = parse_article_title(content, 'blog')

print(head)

with open("response.txt", "w", encoding="utf-8") as file:
    file.write(head)
