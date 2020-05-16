from time import sleep
from bs4 import BeautifulSoup

CLOUD_URL = r'http://t-open.tzonedigital.cn/'
WEB_LOAD_TIME = 5


def get_raw_data():
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Opens the browser up in background

    with Chrome(options=chrome_options) as browser:
        browser.get(CLOUD_URL)
        sleep(WEB_LOAD_TIME)
        html = browser.page_source

    page_soup = BeautifulSoup(html, 'html.parser')
    raw_cloud_data = page_soup.findAll("table", {"id": "tab1"})[0].attrs['jsondata']
    return raw_cloud_data
