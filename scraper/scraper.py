import sys
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
        try:
            self.page = requests.get(self.url, headers= HEADERS)
        except:
            print("Error: ", sys.exc_info()[0])
            self.page = ""

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

    @property
    def file_name(self):
        return self.occupation + '_' + self.job_id + '.txt'

    @property
    def file_path(self):
        return self.directory + '/' + self.file_name

    @property
    def html(self):
        html = self.parse()
        return "h-source: %s\n\n%s" % (self.page.url, html.strip())

    @property
    def source(self):
        soup = BeautifulSoup(self.content, 'html.parser')
        [[s.extract() for s in soup(tag)] for tag in ['head', 'footer', 'meta', 'script', 'style', 'link', 'header']]

        return soup

    def parse(self):
        if (self.content) == 0 : return None

        content = None

        if re.search('http(s?):\/\/.*?us\.jobs', self.page.url):
            title = self.source.select('div.t16.bld.l20')[0]
            body  = self.source.find(id='contentm')
            content = "%s\n%s" % (title.getText(), body.getText())

        if re.search('http(s?):\/\/.*?usajobs\.gov', self.page.url):
            title = self.source.find(id='job-title')
            body  = self.source.find(id='main-content')
            content = "%s\n%s" % (title.getText(), body.getText())

        #https://dashboard.montanaworks.gov/IWRSManageAccountWeb/faces/jsp/search/JobDetails.xhtml?jadrId=102664487
        if re.search('http(s?):\/\/dashboard\.montanaworks\.gov\/IWRSManageAccountWeb\/faces\/jsp\/search\/JobDetails\.xhtml', self.page.url):
            title = self.source.findAll('h1')[0]
            body  = self.source.find(id='jobDetailsDiv')
            content = "%s\n%s" % (title.getText(), body.getText())

        #https://jobs.utah.gov/jsp/utjobs/single-job?j=3659721
        if re.search('http(s?):\/\/jobs\.utah\.gov\/jsp\/utjobs\/single-job', self.page.url):
            content = self.source.find(id= 'joInlineId').getText()

        #https://jobs.myflorida.com/job/TALLAHASSEE-OPERATIONS-MANAGER-C-SES-64035425-FL-32399/444240500/
        if re.search('http(s)?:\/\/jobs\.myflorida\.com\/job', self.page.url):
            content = self.source.select('div.jobDisplay')[0].getText()

        #https://www.governmentjobs.com/careers/tracyca/jobs/1913665/city-manager-per-contract
        if re.search('http(s)?:\/\/www\.governmentjobs\.com\/careers', self.page.url):
            content = self.source.select('div.entity-info')[0].getText()

        #http://agency.governmentjobs.com/sc/default.cfm?action=viewJob&jobID=1908940

# 500 Errors
#https://www.azjobconnection.gov/ada/r/jobs/AZ02876155
#https://idahoworks.gov/ada/r/jobs/ID01010215
#https://www.kansasworks.com/ada/r/jobs/KS10528733

# Session expires
#https://www.employflorida.com/vosnet/jobbanks/jobdetails.aspx?enc=9B8/uT7EfbEIDLIMZ8rho7tTtq1JCrGjGTW0jt1m+sNa9bAzLiA3uWxZ3o2fn5mh4i+aWkk9Ixxy0q9tw3uhnL6zIaDzX3q71naeNBSN9f898VAw0BBYM1rvp3d6inHtVfVbq6+uvF+utxH+TDF0lMb2YU/qALobeMNf9yoLyGE=

#https://www1.iowajobs.org/jobs/seeker/search/search.seek?actionButton=Search&keywords=6301715
#https://hca.taleo.net/careersection/0hca/jobdetail.ftl?job=20792-62910&lang=en
#https://ajg.taleo.net/careersection/2/jobdetail.ftl?job=39663#39663
#https://massanf.taleo.net/careersection/ex/jobdetail.ftl?job=170006QO&lang=en
#https://www.minnesotaworks.net/viewjob.aspx?jobid=9694118
#https://jobs.mitalent.org/job-seeker/job-details/5058313
#https://virginiajobs.peopleadmin.com/postings/95546#95546
#https://wit.twc.state.tx.us/WORKINTEXAS/wtx?pageid=EM_JP_JOB_DETAILS&id=5273305
#https://csg.applicantpro.com/jobs/679409.html#679409
#http://jobs.hr.wisc.edu//cw/en-us/job/496810/assistant-director
#https://csg.applicantpro.com/jobs/679392.html#679392
#https://www.jobgateway.pa.gov/jponline/JobSeeker/JobPostingDetails?QCf9GhbSC5Nn41_TB0_axNd6x8c38Fs6lT_RL7JjiNX4Qq0_L3UR2aaWoAc@aBw8Q1JsNTIWPmFT_4oUve5xm37PpJ1BQwyPrEV6Hxo6zqniFwW4sPNx
#https://hubinternational.jobs/san-diego-ca/vice-president-policyholder-advocate/788D467A432B4895B767C8CBCA741D2B/job/?utm_campaign=American%20Job%20Center&vs=206&utm_medium=NLX&utm_source=American%20Job%20Center-DE
#https://okjobmatch.com/ada/r/jobs/OK01446242
#https://jobs-octa.icims.com/jobs/1826/section-manager-ii-iii---measure-m-local-programs/job
#https://seeker.worksourcewa.com/jobview/GetJob.aspx?JobID=190911383
#https://joblink.maine.gov/ada/r/jobs/280950
#https://statejobsny.com/public/vacancyDetailsView.cfm?id=45635#45635
#https://www.healthcaresource.com/fremontmedical/index.cfm?fuseaction=search.jobDetails&template=dsp_job_details.cfm&cJobId=102157
#https://pfizer.jobs/global/gerente-de-distrito/7BBC4B39E9DE41A99FB51FD728533D0C/job/?utm_campaign=American%20Job%20Center&vs=206&utm_medium=NLX&utm_source=American%20Job%20Center-DE
#https://secure.emp.state.or.us/jobs/index.cfm?location_content=jobdisplay.cfm&ord=1981981
#http://jobs.jobvite.com/smithbucklin/job/ohfp6fwL?nl=1&nl=1
#https://searchjobs.dartmouth.edu/postings/43913
#https://jobs.citi.com/job/-/-/287/6307549?utm_source=directemployers&utm_campaign=2017_media_foundational&utm_medium=job_board&utm_content=job_posting&ss=paid
#https://cbre.referrals.selectminds.com/jobs/svp-corporate-development-29975?SubSourceId=50000165
#https://albany.interviewexchange.com/jobofferdetails.jsp;jsessionid=2220A0605B1B265EEDB9DF4A5028FADE?JOBID=91075&CNTRNO=1&TSTMP=0
#https://lacare.secure.force.com/openings/ts2__JobDetails?jobId=a0K2A00000KQOjkUAH&tSource=#a0K2A00000KQOjkUAH
#https://nycdoe.silkroad.com/epostings/index.cfm?fuseaction=app.jobinfo&jobid=216773&company_id=15651&version=2&source=ONLINE&jobOwner=1002388&aid=1#216773
#https://joblink.alabama.gov/ada/r/jobs/2318020
#https://www.jobaps.com/MD/sup/bulpreview.asp?R1=17&R2=002587&R3=0041#170025870041
#https://utdirect.utexas.edu/apps/hr/jobs/nlogon/171120010457
#https://www.sujobopps.com/postings/72694
#https://jobs.target.com/job/san-francisco/stores-executive-intern-san-francisco-peninsula-oakland-and-alameda/1118/5148289

        if not content :
            print(self.page.url)
            content = self.source.getText()

        return self.clean_content(content)

    def clean_content(self, html):
        html = re.sub('\r', '', html)
        html = re.sub('\n+', '\n', html)
        html = re.sub('\t', '  ', html)
        return html.strip()

    def save(self):
        if os.path.exists(self.file_path):
            return self

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        with open(self.file_path, "w") as f:
            try:
                f.write( str(self.html) )
            except:
                print("Error: ", sys.exc_info()[0])
                print(self.parse())

        return self

class ResultsPage(Page):
    def __init__(self, occupation, title, per_page=500):
        self.occupation = occupation
        self.title = title
        self.current_page = 1
        self.per_page = per_page
        self.base_url = "https://www.careeronestop.org/Toolkit/Jobs/find-jobs.aspx"
        self.url = self.base_url + "?source=DEA&keyword=%s&location=US&occtitle=%s&pagesize=%s&currentpage=%s" % (occupation, title, self.per_page, self.current_page)
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
