import copy

import requests
from bs4 import BeautifulSoup

from helpers.clog import CLog
from models.general_models import Problem


class Codeforces:
    def __init__(self):
        self.s = requests.session()
        self._headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        }

    def get_problem_list(self, page_index):
        url = f'https://codeforces.com/problemset/page/{page_index}'

        headers = copy.deepcopy(self._headers)
        r = self.s.get(url, headers=headers)

        raw = r.text
        # print(raw)

        soup = BeautifulSoup(raw, 'html.parser')

        pagination = soup.select('div.pagination > ul > li')
        last_page = pagination[-2]
        # print(last_page)
        last_page_index = int(last_page.select('span.page-index')[0]['pageindex'])
        if page_index>last_page_index:
            CLog.warn(f'Overpass last page: #{page_index}/{last_page_index}')
            return []
        CLog.info(f'Getting problem list from page: #{page_index}/{last_page_index}')

        problem_tags = soup.select('table.problems > tr')[1:] # remove header line
        print(len(problem_tags))
        # print(problem_tags[0])

        problems = []
        for problem_tag in problem_tags:
            problem = Problem()
            pid = problem_tag.select('td.id a')[0]

            problem.src_id = pid.text.strip()
            problem.src_url = 'https://codeforces.com' + pid['href']

            ptitle = problem_tag.select('td')[1].select('div')[0]
            problem.name = ptitle.select('a')[0].text.strip()

            ptags = problem_tag.select('td')[1].select('div')[1].select('a')
            for ptag in ptags:
                tag = ptag.text.strip()
                problem.tags.append(tag)

            difficulty = problem_tag.select('td')[3].select('span')
            if difficulty:
                difficulty = difficulty[0].text.strip()
                difficulty = int(difficulty) ** 0.5
                dmax = 3800 ** 0.5
                dmin = 250 ** 0.5

                difficulty = (difficulty - dmin)/(dmax-dmin) * 10
            else:
                difficulty = 0

            problem.difficulty = difficulty

            problems.append(problem)

            # print(problem.name)
            # print(problem.src_id)
            # print(problem.src_url)
            # print(problem.tags)
            # print(problem.difficulty)
            # break
        return problems

    def get_problem_detail(self, problem):
        url = problem.src_url
        pass


if __name__ == '__main__':
    cf = Codeforces()
    problems = cf.get_problem_list(1)
    for i in range(len(problems)):
        print(f'#{i+1} - {problems[i].src_id} - {problems[i].name} - {problems[i].difficulty}')
