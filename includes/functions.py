import json
import os
import random
import time
import re
import openai

from includes.parameters import *

global_cnt = 0


def call_openai_api(system_prompt: str, user_prompt: str, model: str = "gpt-3.5-turbo", temperature: float = 0.7,
                    keyword: str = "", language: str = "English") -> str:
    """
    Calls OpenAI API and returns the response.
    :param system_prompt: The system prompt - Use this to describe how you want the AI model to behave.
    :param user_prompt: The user prompt - Use this to describe what you want the AI model to do.
    :param model: The AI model that will be used.
    :param temperature: How creative do you want the AI to be? Values between 0.0 (deterministic) and 2.0 (crazy).
    :param keyword: The keyword with which the AI model will generate its response.
    :param language: The language in which you want the AI model to respond.
    :return: The response of the AI model.
    """
    system_msg = [{"role": "system", "content": system_prompt}]
    user_assistant_msg = [{"role": "user", "content": user_prompt + f' KEYWORD: {keyword}, LANGUAGE: {language}.'}]

    msgs = system_msg + user_assistant_msg
    response = openai.ChatCompletion.create(model=model,
                                            messages=msgs,
                                            temperature=temperature)
    status_code = response["choices"][0]["finish_reason"]
    assert status_code == "stop", f"The status code was {status_code}."

    return response["choices"][0]["message"]["content"]


def capitalize_every_word(title: str) -> str:
    """
    Capitalizes the first letter of every word in the given string.
    :param title: The string to be capitalized.
    :return: Capitalized string.
    """
    return ' '.join(w[:1].upper() + w[1:] for w in title.split(' '))


def create_subfolders(parent_dir_path: str, keywords_file_path: str) -> list[tuple[str, str]]:
    """
    Creates the subfolders where each item returned by the API call will be stored.
    Returns the list of keywords used and the folders created as a list of (folder, keyword) tuples.
    :param parent_dir_path: Path to the parent directory where subfolders will be created.
    :param keywords_file_path: Path to the keywords file, where each keyword is given in its own line.
    :return: Returns the list of keywords used and the folders created as a list of (folder, keyword) tuples.
    """
    folders_and_keywords = []
    with open(keywords_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.lower().strip()
            removed = line.replace(' &', '')
            folder_name = re.sub(r'[^a-z0-9\s+]', '', removed).replace(' ', '-')
            folders_and_keywords.append((folder_name, line))

    for folder, _ in folders_and_keywords:
        path = os.path.join(parent_dir_path, folder)
        if not os.path.exists(path):
            os.mkdir(path)

    # returns a list of (folder, keyword) tuples
    return folders_and_keywords


def get_subfolders(path):
    subfolders = [f.path for f in os.scandir(path) if f.is_dir()]
    return subfolders


def is_item(path):
    if os.path.exists(path):
        return True
    return False


def parse_article_title(data: str, item_type: str) -> str:
    article_title_json = json.loads(data)
    title = article_title_json['title']

    header = ''
    if item_type == 'blog':
        header += BLOG_HEADER
    elif item_type == 'item':
        header += ITEM_HEADER
    header += f'{title}\n---\n\n'
    return header


def parse_user_comments(data: str) -> str:
    """
    Changes user comments from json to Markdown format.
    :param data: User comments in json format.
    :return: User comments in Markdown format.
    """
    user_comments_json = json.loads(data)
    # user_comments_markdown = f'\n\n<div class="user_comments">\n\n## User Comments\n\n'
    user_comments_markdown = f'## User Comments\n\n'
    for commenter in user_comments_json:
        name = commenter['name']
        last_name = commenter['last name']
        gender = commenter['gender']
        comment = commenter['comment']
        profile_image_id = random.randint(1, NUM_PROFILE_IMAGES[gender])
        user_comments_markdown += f'![{name} {last_name}]' \
                                  f'(image://profiles/{gender}/{profile_image_id}.jpg) ' \
                                  f'**{name} {last_name}**: {comment}\n\n'
    # user_comments_markdown += f'</div>'
    return user_comments_markdown


def php_add_slashes(data: str) -> str:
    return data.replace(r'"', r'\"')


def php_generate_index_php(root):
    template = """<?php include_once("meta.php"); ?>
<!DOCTYPE html>
<html lang="<?php echo $page_language ?>">

<head>
<meta charset="utf-8">
<title><?php echo $page_title ?></title>
""" + f'<link rel="stylesheet" href="{root}styles.css">' + """
</head>

<body>
<div class="ps-grid">
<header class="header">""" + f'<?php include_once("{root}_inc/header.php"); ?>' + """</header>
<main class="main-content"><?php include_once("contents.php"); ?></main>
<section class="left-sidebar">""" + f'<?php include_once("{root}_inc/left-sidebar.php"); ?>' + """</section>
<aside class="right-sidebar">""" + f'<?php include_once("{root}_inc/right-sidebar.php"); ?>' + """</aside>
<footer class="footer">""" + f'<?php include_once("{root}_inc/footer.php"); ?>' + """</footer>
</div>
</body>

</html>
"""
    return template


def write_article(data: tuple) -> None:
    """
    Makes API calls to the AI model to generate a pSEO article.
    :param data: A tuple containing (folder, keyword, language, language_code, parent_dir_path, \
        article_temperature, user_comments_temperature, item_type, num_all_items).
    :return: None.
    """
    folder, keyword, language, language_code, parent_dir_path, \
        article_temperature, user_comments_temperature, item_type, num_all_items = data

    global global_cnt

    article_file_path = f"{parent_dir_path}\\{folder}\\{item_type}.{language_code}.md"
    if not is_item(article_file_path):
        article_written = False
        article_header_written = False
        article_text_written = False
        user_comments_written = False
        while not article_written:
            try:
                print(f'Writing article for KEYWORD: {keyword} -- LANGUAGE: {language}\n')
                article = ''

                # ARTICLE TITLE AND HEADER
                while not article_header_written:
                    try:
                        article_title_json = call_openai_api(SYSTEM_PROMPT, ARTICLE_TITLE_PROMPT,
                                                             MODEL, article_temperature, keyword, language)
                        time.sleep(API_CALL_DELAY)
                        article_header_markdown = parse_article_title(article_title_json, item_type)
                        article = article_header_markdown
                    except Exception as err:
                        print(f"{ConsoleColors.FAIL}- HEADER: FAILED {article_file_path}\n{err=},"
                              f"{type(err)=}{ConsoleColors.ENDC}")
                    else:
                        article_header_written = True

                # ARTICLE TEXT
                while not article_text_written:
                    try:
                        article_text_markdown = call_openai_api(SYSTEM_PROMPT, ARTICLE_PROMPT,
                                                                MODEL, article_temperature, keyword, language)
                        time.sleep(API_CALL_DELAY)
                        article += article_text_markdown
                    except Exception as err:
                        print(f"{ConsoleColors.FAIL}- TEXT: FAILED {article_file_path}\n{err=},"
                              f"{type(err)=}{ConsoleColors.ENDC}")
                    else:
                        article_text_written = True

                # USER COMMENTS
                while not user_comments_written:
                    try:
                        user_comments_json = call_openai_api(SYSTEM_PROMPT, USER_COMMENTS_PROMPT, MODEL,
                                                             user_comments_temperature, keyword, language)
                        time.sleep(API_CALL_DELAY)
                        user_comments_markdown = parse_user_comments(user_comments_json)
                        article += user_comments_markdown
                    except Exception as err:
                        print(f"{ConsoleColors.FAIL}- USER COMMENTS: FAILED {article_file_path}\n{err=},"
                              f"{type(err)=}{ConsoleColors.ENDC}")
                    else:
                        user_comments_written = True

                # WRITE ARTICLE TO FILE
                with LOCKS['write']:
                    with open(article_file_path, 'w', encoding='utf-8') as article_file:
                        article_file.write(article)

            except Exception as err:
                print(f"{ConsoleColors.FAIL}FAILED TO WRITE ARTICLE! {article_file_path}\n{err=},"
                      f"{type(err)=}{ConsoleColors.ENDC}")

            else:
                conditions = [
                    article_header_written,
                    article_text_written,
                    user_comments_written
                ]
                if not (False in conditions):
                    article_written = True
                    with LOCKS['counter']:
                        global_cnt += 1
                    print(f'{ConsoleColors.OKCYAN}DONE | KEYWORD: {keyword} -- LANGUAGE: {language}{ConsoleColors.ENDC}')
                    percentage = round(global_cnt / num_all_items * 100, 1)
                    print(folder, '--', f"{global_cnt}/{num_all_items} ({percentage}%)\n")
    else:
        print(f'{ConsoleColors.WARNING}Article exists, skipping...{article_file_path}{ConsoleColors.ENDC}\n')
