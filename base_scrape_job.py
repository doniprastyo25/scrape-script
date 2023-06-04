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
        
    def _instance_url(self, url: str, return_result: bool=False) -> BeautifulSoup:
        response: requests.models.Response = requests.get(url)
        soup: BeautifulSoup = BeautifulSoup(response.content, 'html.parser')
        if return_result:
            return soup
        self.soup: str = soup
    
    def _extract_link(self, xpath_link: str) -> str:
        link_elements: bs4.element.Tag = self.soup.select_one(xpath_link)
        link: str = link_elements['href']
        if self._platform == "linkedin":
            return link
        link = self._platform_base_link + link
        return link

    def _get_link_job(self, link: str, xpath: str, need_result_link: bool) -> str | None:
        soup: BeautifulSoup = self._instance_url(link, need_result_link)
        raw_value: list = []
        tree: lxml.etree._Element = etree.HTML(str(soup))
        if tree is None:
            return
        select: list | None = tree.xpath(xpath)
        for i in select:
            raw_value.append(i.text)
        cleaned_value: str = raw_value[0].strip()
        return cleaned_value

    def _custom_result(self, link: str) -> dict:
        object_custom: dict = {}
        for i in dir(self):
            if "_xpath_" in i and getattr(self, i) is not None:
                title: str = i.replace("_xpath_", "")
                value = self._get_link_job(link, getattr(self, i), True)
                if value is not None:
                    object_custom[title] = value
        return object_custom

    def _extract_data(self, xpath_tag: str, xpath_link: str) -> dict:
        title: list = []
        tree: lxml.etree._Element = etree.HTML(str(self.soup))
        select: list = tree.xpath(xpath_tag)
        link: str = self._extract_link(xpath_link)
        for i in select:
            title.append(i.text)
        clean_title: str = title[0].strip()
        additional_info: dict = self._custom_result(link)
        job: dict = {
            "job": clean_title,
            "link": link
        }
        job.update(additional_info)
        return job
