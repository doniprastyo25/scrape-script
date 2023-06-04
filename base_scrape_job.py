from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from lxml import etree
import requests
import json

class BaseScrape(ABC):

    @abstractmethod
    def _register_path(self):
        self._platform = None
        self._platform_base_link = None
        self._base_url = None
        self._title = None
        self._xpath_seniority = None
        self._xpath_company = None
        self._xpath_location = None
        self._xpath_posted = None
        self._xpath_job_role = None
        self._xpath_contract = None
        self._xpath_industries = None

    def __init__(self) -> None:
        self._register_path()
        if self._platform is None:
            raise Exception("self._platform and self._platform_base_link should be fill")
        self._instance_url(self._base_url)
        
    def _instance_url(self, url, return_result=False):
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        if return_result:
            return soup
        self.soup = soup
    
    def _extract_link(self, xpath_link):
        link_elements = self.soup.select_one(xpath_link)
        link = link_elements['href']
        if self._platform == "linkedin":
            return link
        link = self._platform_base_link + link
        return link

    def _get_link_job(self, link, xpath, need_result_link):
        soup = self._instance_url(link, need_result_link)
        raw_value: list = []
        tree = etree.HTML(str(soup))
        select = tree.xpath(xpath)
        for i in select:
            raw_value.append(i.text)
        cleaned_value = raw_value[0].strip()
        return cleaned_value

    def _custom_result(self, link) -> dict:
        object_custom: dict = {}
        for i in dir(self):
            if "_xpath_" in i and getattr(self, i) is not None:
                title: str = i.replace("_xpath_", "")
                object_custom[title] = self._get_link_job(link, getattr(self, i), True)
        return object_custom

    def _extract_data(self, xpath_tag, xpath_link) -> dict:
        title: list = []
        tree = etree.HTML(str(self.soup))
        select = tree.xpath(xpath_tag)
        link = self._extract_link(xpath_link)
        for i in select:
            title.append(i.text)
        clean_title = title[0].strip()
        additional_info: dict = self._custom_result(link)
        job: dict = {
            "job": clean_title,
            "link": link
        }
        job.update(additional_info)
        return job
