from bs4 import BeautifulSoup
from lxml import etree
import requests
import json

class ScrapeBs4:
    def __init__(self) -> None:
        self._xpath_company = '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[1]/a'
        self._xpath_locations = '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[2]'
        self._xpath_seniority = '//*[@id="main-content"]/section[1]/div/div/section[1]/div/ul/li[1]/span'
        self._xpath_type = '//*[@id="main-content"]/section[1]/div/div/section[1]/div/ul/li[2]/span'
        self._xpath_job_function = '//*[@id="main-content"]/section[1]/div/div/section[1]/div/ul/li[3]/span'
        self._xpath_industries = '//*[@id="main-content"]/section[1]/div/div/section[1]/div/ul/li[4]/span'
        self._xpath_posted = '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[2]/span[1]'
        self.base_url = "https://www.linkedin.com/jobs/search?keywords=Django&location=Indonesia&locationId=&geoId=102478259&f_TPR=&position=1&pageNum=0"
        self.exec_script()
    
    def _instance_url(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    
    def _extract_title(self, soup, xpath_tag, tag_href):
        title: list = []
        tree = etree.HTML(str(soup))
        select = tree.xpath(xpath_tag)
        link_elements = soup.select_one(tag_href)
        link = link_elements['href']
        for i in select:
            title.append(i.text)
        cleaned_title = title[0].strip()
        job: dict = {
            "job": cleaned_title,
            "company": self._get_link_job(link, self._xpath_company),
            "locations": self._get_link_job(link, self._xpath_locations),
            "seniority": self._get_link_job(link, self._xpath_seniority),
            "job_role": self._get_link_job(link, self._xpath_job_function),
            "contract": self._get_link_job(link, self._xpath_type),
            "industries": self._get_link_job(link, self._xpath_industries),
            "posted": self._get_link_job(link, self._xpath_posted),
            "link": link,
        }
        return job

    def _get_link_job(self, link, xpath):
        soup = self._instance_url(link)
        raw_value: list = []
        tree = etree.HTML(str(soup))
        select = tree.xpath(xpath)
        for i in select:
            raw_value.append(i.text)
        cleaned_value = raw_value[0].strip()
        return cleaned_value

    
    def exec_script(self):
        soup = self._instance_url(self.base_url)
        for i in range(1, 6):
            print(i)
            title = self._extract_title(soup, f'//*[@id="main-content"]/section[2]/ul/li[{i}]/div/a/span', f'#main-content > section.two-pane-serp-page__results-list > ul > li:nth-child({i}) > div > a')
            print(json.dumps(title, indent=3))


if __name__ == "__main__":
    ScrapeBs4()
