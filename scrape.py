from operator import itemgetter

import requests
from pprint import pprint
from bs4 import BeautifulSoup

# Useful functions
def sort_stories_by_votes_desc(stories):
    return sorted(stories, key=itemgetter('score'), reverse=True)

def top_posts(pages=1):
    try:
        # Fetch response and formulate a Soup Object (to extract from it)
        for page in range(1, pages + 1):
            res = requests.get(f'https://news.ycombinator.com/news?p={page}')
            soup = BeautifulSoup(res.text, 'html.parser')

            # Fetch links from Soup Object
            links = soup.select('.submission')
            submission_list = []

            for item in links:
                id_num = item.attrs.get('id')
                score_tag = soup.select_one(f'#score_{id_num}')
                title_tag = soup.select_one(f'[id="{id_num}"] .title .titleline a')

                if score_tag and title_tag:
                    href = title_tag.attrs.get('href')
                    score = score_tag.text.replace(' points', '')
                    title = title_tag.text

                if int(score) > 99:
                    submission_list.append({"title" : title, "score": score, "URL": href})

        return sort_stories_by_votes_desc(submission_list)
    except Exception as e:
        print('error: ', e)

pprint(top_posts(3))