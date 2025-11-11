from operator import itemgetter
import requests
from pprint import pprint
from bs4 import BeautifulSoup

def sort_stories_by_votes_desc(stories):
    return sorted(stories, key=itemgetter('score'), reverse=True)

def top_posts(pages=1, min_score=100):
    submission_list = []

    for page in range(1, pages + 1):
        res = requests.get(f'https://news.ycombinator.com/news?p={page}')
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')

        links = soup.select('.submission')

        for item in links:
            id_num = item.attrs.get('id')
            score_tag = soup.select_one(f'#score_{id_num}')
            title_tag = soup.select_one(f'[id="{id_num}"] .title .titleline a')

            if score_tag and title_tag:
                try:
                    score = int(score_tag.text.replace(' points', ''))
                    if score >= min_score:
                        title = title_tag.text
                        href = title_tag.attrs.get('href')
                        submission_list.append({"title": title, "score": score, "URL": href})
                except ValueError:
                    # Skip malformed score
                    continue

    return sort_stories_by_votes_desc(submission_list)

if __name__ == "__main__":
    pprint(top_posts(pages=3))
