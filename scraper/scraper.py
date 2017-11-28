import os
import re
import logging
import Occupations
import requests
from bs4 import BeautifulSoup

class Page(object):
    def __init__(self, url):
        self.page = None
        self.url = url

    def fetch(self):
        logging.debug(self.url)
        HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0"}
        self.page = requests.get(self.url, headers= HEADERS)
        return self

    @property
    def content(self):
        if self.page == None : self.fetch()
        return self.page.content

    def parse(self):
        return self

class JobPage(Page):
    def __init__(self, url, occupation, job_id):
        super().__init__(url)
        self.occupation = occupation
        self.job_id = job_id

    @property
    def onet(self):
        """ Each item in the SOC is designated by a six-digit code. The hyphen between the second
        and third digit is used only for clarity """
        return self.occupation[:-3]

    @property
    def major(self):
        """ first two digits of the SOC code represent the major group; """
        return self.occupation[:2] + "-0000"

    @property
    def minor(self):
        """ third digit represents the minor group """
        return self.occupation[:4] + "000"

    @property
    def broad_occupation(self):
        """ fourth and fifth digits represent the broad occupation """
        return self.onet[:6] + "0"

    @property
    def directory(self):
        return "data/" + self.major

    def parse(self):
        soup = BeautifulSoup(self.content, 'html.parser')
        [[s.extract() for s in soup(tag)] for tag in ['script', 'style', 'link']]
        return soup

    def save(self):
        html = self.parse()

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        file_name = self.occupation + '_' + self.job_id + '.txt'
        with open(self.directory + '/' + file_name, "w") as f:
            value = str(html.get_text())
            f.write(value)

        return self

class ResultsPage(Page):
    def __init__(self, occupation, title, per_page=500):
        self.occupation = occupation
        self.title = title
        self.current_page = 1
        self.per_page = per_page
        self.base_url = "https://www.careeronestop.org/Toolkit/Jobs/find-jobs.aspx"
        self.url = self.base_url + "?keyword=%s&location=US&occtitle=%s&pagesize=%s&currentpage=%s" % (occupation, title, self.per_page, self.current_page)
        self.max_pages = 1
        super().__init__(self.url)

    def run(self):
        self.next()

    def next(self):
        if self.parse():
            self.current_page = self.current_page + 1
            if self.current_page > self.max_pages : return False
            self.next()

    def parse(self):
        logging.info("Parsing current_page: %s" % self.current_page)
        soup = BeautifulSoup(self.content, 'html.parser')
        div = soup.find_all('div', class_='datagrid')
        if not div: return None
        div = div[0]
        table = div.find_all('table')[0]

        rows = table.find_all('tr')
        for row in rows[1:]:
            columns = row.find_all('td')
            url = columns[0].find('a')['href']
            company = columns[1].get_text()
            location = columns[2].get_text()
            job_id = url.split('/')[-1:][0]

            JobPage(url, self.occupation, job_id).save()

        return soup

class Scraper(object):
    def __init__(self, code, title):
        self.code = code
        self.title = title

    def __str__(self):
        return self.code + " " + self.title

    def fetch(self):
        logging.info(str(self))
        ResultsPage(self.code, self.title).run()
        return 'running'

    @staticmethod
    def run():
        for occupation in Occupations.occupations():
            scraper = Scraper(occupation[0], occupation[1])
            scraper.fetch()

def main():
    logging.basicConfig(level=logging.INFO)
    Scraper.run()

if __name__ == '__main__' : main()
