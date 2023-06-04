from base_scrape_job import BaseScrape
import json

class Linkedin(BaseScrape):
    def __init__(self):
        super().__init__()
        self.exec_script()
    
    def _register_path(self):
        self._platform: str = "linkedin"
        self._platform_base_link: str = "https://www.linkedin.com"
        self._base_url: str = "https://www.linkedin.com/jobs/search?keywords=Django&location=Indonesia&locationId=&geoId=102478259&f_TPR=&position=1&pageNum=0"
        self._xpath_company: str = '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[1]/a'
        self._xpath_locations: str = '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[1]/span[2]'
        self._xpath_seniority: str = '//*[@id="main-content"]/section[1]/div/div/section[1]/div/ul/li[1]/span'
        self._xpath_type: str = '//*[@id="main-content"]/section[1]/div/div/section[1]/div/ul/li[2]/span'
        self._xpath_job_function: str = '//*[@id="main-content"]/section[1]/div/div/section[1]/div/ul/li[3]/span'
        self._xpath_industries: str = '//*[@id="main-content"]/section[1]/div/div/section[1]/div/ul/li[4]/span'
        self._xpath_posted: str = '//*[@id="main-content"]/section[1]/div/section[2]/div/div[1]/div/h4/div[2]/span[1]'
    
    def exec_script(self):
        for i in range(1, 6):
            self._title: str = f'//*[@id="main-content"]/section[2]/ul/li[{i}]/div/a/span'
            self._content_url: str = f'#main-content > section.two-pane-serp-page__results-list > ul > li:nth-child({i}) > div > a'
            print(json.dumps(super()._extract_data(self._title, self._content_url), indent=3))

if __name__ == "__main__":
    Linkedin()