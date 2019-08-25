import requests
import imghdr
# import selenium
from bs4 import BeautifulSoup

from urllib.parse import urlparse, urljoin, urlsplit

# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException

from logger import BemihoLogger
from services.base import BemihoService

class SessionImageService(BemihoService):
    def __init__(self):
        self.driver = None
        self.logger = BemihoLogger(__class__).get_logger()

    def start(self, **kwargs):
        pass
        # if self.driver is None:
        #     chrome_options = webdriver.chrome.options.Options()
        #     chrome_options.add_argument("--disable-extensions")
        #     chrome_options.add_argument("--disable-gpu")
        #     chrome_options.add_argument("--headless")
        #     self.driver = webdriver.Chrome(options=chrome_options)

    # def get_element_by_selector(self, url, selector):
    #     try:
    #         self.driver.get(url)
    #         return self.driver.find_element_by_css_selector(selector)
    #     except NoSuchElementException:
    #         self.driver.close()
    #         return None

    # def get_session_from_url(self, url):
    #     headers = {
    #         "User-Agent":
    #             "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    #     }
    #     new_session = requests.session()
    #     new_session.headers.update(headers)
    #     for cookie in self.get_cookies_from_url(url):
    #         c = {cookie['name']: cookie['value']}
    #         new_session.cookies.update(c)
    #     return new_session

    # def get_cookies_from_url(self, url):
    #     self.driver.get(url)
    #     return self.driver.get_cookies()

    def get_host_name(self, url):
        parsed_url = urlparse(url)
        return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)

    def get_image_content(self, url, selector):
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }
        new_session = requests.session()
        # print("URL:", url)
        response = new_session.get(url, headers=headers)
        # print("RESPONSE", response)
        soup = BeautifulSoup(response.text, 'lxml')
        element = soup.find('img', class_=selector)
        # print("ELEMENT:", element)
        if element is not None:
            image_source = element.get('src')
            parts = urlsplit(image_source)  
            if not parts.scheme or not parts.netloc:
                host_name = self.get_host_name(url)
                image_source = urljoin(host_name, image_source)
                # print("NEW IMAGE SOURCE: ", image_source)
            image_response = new_session.get(image_source, allow_redirects=True)
            # print("SUCCESS: ", len(image_response.content))
            return image_response.content
        else:
            return None
        # element = self.get_element_by_selector(url, selector)
        # if element is not None:
        #     image_source = element.get_attribute('src')
        #     image_session = self.get_session_from_url(image_source)
        #     response = image_session.get(image_source, allow_redirects=True)
        #     return response.content
        # else:
        #     return None

    def stop(self):
        self.driver.quit()