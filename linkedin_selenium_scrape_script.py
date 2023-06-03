from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from lxml import etree
import time
driver = webdriver.Chrome()

class Scrape:
    time_sleep = time.sleep(5)
    actions = ActionChains(driver)
    def __init__(self):
        self.base_url = "https://www.linkedin.com"
        self._instance_url()
        time.sleep(2)
        self.actions
        self.exec_script()

    def _instance_url(self):
        driver.get(self.base_url)
        self.time_sleep
    
    def _get_elements(self, xpath_element):
        get_elements = driver.find_element('xpath', xpath_element)
        return get_elements

    def _get_elements_and_click(self, xpath_element):
        get_elements = self._get_elements(xpath_element)
        self.actions.click(get_elements).perform()
    
    def _get_elements_and_fill(self, xpath_elements, send_keys):
        get_elements = self._get_elements(xpath_elements)
        get_elements.send_keys(send_keys)
    
    def _get_all_tag(self):
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        return soup.prettify()
    
    def _extract_title(self, xpath_link):
        list_title = []
        soup_process = self._get_all_tag()
        tree = etree.HTML(str(soup_process))
        select = tree.xpath(xpath_link)
        for i in select:
            list_title.append(i.text)
        cleaned_element = list_title[0].strip()
        return cleaned_element

    
    def exec_script(self):
        self._get_elements_and_click('/html/body/nav/ul/li[4]/a')
        time.sleep(2)
        self._get_elements_and_fill('//*[@id="job-search-bar-keywords"]','Django')
        self._get_elements_and_click('//*[@id="jobs-search-panel"]/form/section[2]/button')
        self._get_elements_and_fill('//*[@id="job-search-bar-location"]', 'indonesia')
        self._get_elements_and_click('//*[@id="jobs-search-panel"]/form/button')
        for i in range(1, 5):
            title = self._extract_title(f'//*[@id="main-content"]/section[2]/ul/li[{i}]/div/a/span')
            print(title)
        time.sleep(2)

if __name__ == "__main__":
    Scrape()