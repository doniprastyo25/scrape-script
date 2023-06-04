from base_scrape_job import BaseScrape
import json

class JobStreet(BaseScrape):
    def __init__(self) -> None:
        super().__init__()
        self.exec_script()

    def _register_path(self):
        self._platform = "jobstreet"
        self._platform_base_link = "https://www.jobstreet.co.id"
        self._base_url = "https://www.jobstreet.co.id/id/django-jobs"
        self._xpath_company = '//*[@id="contentContainer"]/div/div/div[1]/div[1]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div/div[2]/span'
        self._xpath_posted = '//*[@id="contentContainer"]/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div/div[2]/span'
        self._xpath_location = '//*[@id="contentContainer"]/div/div/div[1]/div[1]/div[1]/div/div/div[2]/div/div/div/div[1]/div/span'

    def exec_script(self):
        for i in range(1,3):
            self._title = f'//*[@id="jobList"]/div[2]/div[2]/div/div[{i}]/div/div/article/div/div/div[1]/div[1]/div[2]/h1/a/div/span'
            self._content_url = f'#jobList > div.z1s6m00.iw87102 > div:nth-child(2) > div > div:nth-child({i}) > div > div > article > div > div > div.z1s6m00._1hbhsw67i._1hbhsw66e._1hbhsw69q._1hbhsw68m._1hbhsw6n._1hbhsw65a._1hbhsw6ga._1hbhsw6fy > div:nth-child(1) > div:nth-child(2) > h1 > a'
            print(json.dumps(super()._extract_data(self._title, self._content_url), indent=3))


if __name__ == "__main__":
    JobStreet()
