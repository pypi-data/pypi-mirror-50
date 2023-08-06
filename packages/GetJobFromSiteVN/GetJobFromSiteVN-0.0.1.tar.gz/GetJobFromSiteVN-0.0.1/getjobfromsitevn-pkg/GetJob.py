from builtins import print, property, str, list
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests


def get_soup(link):
    """

    :param link: link html
    :return: soup of html
    """
    html_cotent = requests.get(link).text
    return bs(html_cotent, 'html.parser')


def getFromCarreerBuilder(link):
    """

    :param link: link of your result you want to show
    :return: (job_title, company_name, location, link)
    """
    soup = get_soup(link)
    # briefs_red = soup.find_all("dd", class_="brief bold-red")
    brief_normal = soup.find_all("dd", class_="brief")
    briefs = brief_normal
    list_jobs = []
    for brief in briefs:
        brief_soup = bs(str(brief), 'html.parser')
        job = brief_soup.find('h3', class_='job').find('a', href=True)
        job_title = job.contents[0]
        company_name = brief_soup.find('p', class_='namecom').find('a').contents[0]
        location = brief_soup.find('p', class_='location').contents[1]
        link = job['href']
        # name_com = bs(str(name_class), 'html.parser').find('a').contents
        job = (job_title, company_name, location, link)
        list_jobs.append(job)
    return list_jobs


def getFromVietnamWork(link):
    """

        :param link: link of your result you want to show
        :return: (job_title, company_name, location, link)
    """
    browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    browser.get("https://www.vietnamworks.com/viec-lam-duoc-pham-cong-nghe-sinh-hoc-tai-da-nang-i6v17-vn")
    list_jobs = []
    get_element = browser.find_elements_by_css_selector(
        "div[class='col-xs-8 col-sm-8 col-lg-9 job-search__job-info-col']")
    for ele in get_element:
        to_html = ele.get_attribute('innerHTML')
        job_soup = bs(str(to_html), 'html.parser')
        job = job_soup.find('h3').find('a', href=True)
        job_title = job.contents[0]
        company_name = job_soup.find('span', class_='job-search__company').contents[0]
        location = job_soup.find('span', class_='job-search__location').find('strong').contents[0]
        link = job['href']
        j = (job_title, company_name, location, link)
        list_jobs.append(j)
    return list_jobs


def getFromCareerLink(link):
    """

        :param link: link of your result you want to show
        :return: (job_title, company_name, location, link)
    """
    soup = get_soup(link)
    jobs = soup.find_all('div', class_='list-group-item')
    list_jobs = []
    for job in jobs:
        job_soup = bs(str(job), 'html.parser')
        job_obj = job_soup.find('a', attrs={'target': '_blank'}, href=True)
        job_title = job_obj.contents[0]
        link = 'https://www.careerlink.vn' + job_obj['href']
        company_name = job_soup.find('a', class_='text-accent').contents[0]
        location = job_soup.find_all('a')[2].contents[0]
        j = (job_title, company_name, location, link)
        list_jobs.append(j)
    return list_jobs


def getFromIndeed(link):
    """

        :param link: link of your result you want to show
        :return: (job_title, company_name, location, link)
    """
    # jobs = soup.find_all('div', class_= 'jobsearch-SerpJobCard unifiedRow row result clickcard')
    browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    browser.get(link)
    list_jobs = []
    jobs = browser.find_elements_by_css_selector(
        "div[class='jobsearch-SerpJobCard unifiedRow row result clickcard']")
    list_jobs = []
    for job in jobs:
        to_html = job.get_attribute('innerHTML')
        job_soup = bs(str(to_html), 'html.parser')
        job_opj = job_soup.find('div', class_='title').find('a', title=True, href=True)
        job_title = job_opj['title']
        link = 'https://vn.indeed.com/viewjob?' + str(job_opj['href']).replace('/rc/clk?', '')
        company_name = str(job_soup.find('span', class_='company').contents[0]).replace('\n', "")
        company_name = ' '.join(company_name.split())
        location = job_soup.find('span', class_='location').contents[0]
        j = (job_title, company_name, location, link)
        list_jobs.append(j)
    return list_jobs


def getFromJobStreet(link):
    """

        :param link: link of your result you want to show
        :return: (job_title, company_name, location, link)
    """
    browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    browser.get(link)
    list_jobs = []
    jobs_2 = browser.find_elements_by_css_selector(
        "li[class='result']")
    jobs_1 = browser.find_elements_by_css_selector(
        "li[class='result sponsored sponsored_top']")
    jobs = jobs_1 + jobs_2
    list_jobs = []
    for job in jobs:
        to_html = job.get_attribute('innerHTML')
        soup = bs(str(to_html), 'html.parser')
        job_obj = soup.find('a', class_='jobtitle', href=True)
        job_title = job_obj.contents[0]
        link = job_obj['href']
        if not str(link)[0] == 'h':
            link = 'https://www.jobstreet.vn' + link
        company_name = soup.find('span', class_='company').contents[0]
        location = soup.find('span', class_='location').contents[0]
        j = (job_title, company_name, location, link)
        list_jobs.append(j)
    return list_jobs


if __name__ == '__main__':
    lj = getFromJobStreet(
        'https://www.jobstreet.vn/vi%E1%BB%87c-l%C3%A0m-C%C3%B4ng-Ngh%E1%BB%87-Sinh-H%E1%BB%8Dc-t%E1%BA%A1i-%C4%90%C3%A0-N%E1%BA%B5ng#email_alert_modal')
    for j in lj:
        print(j)
