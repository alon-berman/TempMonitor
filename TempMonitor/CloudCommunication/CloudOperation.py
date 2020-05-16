import urllib.request
from time import sleep

from bs4 import BeautifulSoup

from ErrorManagement.ProgramFlowExceptions import SoupMissingException


def get_data_by_cloud(cloud, soup_obj=None):
    data = None
    if cloud == 'tzonedigital':
        if soup_obj is not None:
            data = soup_obj.findAll("table", {"id": "tab1"})[0].attrs['jsondata']
        else:
            raise SoupMissingException

    return data


def extract_table_as_json():
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Opens the browser up in background

    with Chrome(options=chrome_options) as browser:
        browser.get(CLOUD_URL)
        sleep(10)
        html = browser.page_source

    page_soup = BeautifulSoup(html, 'html.parser')
    raw_cloud_data = get_data_by_cloud(cloud='tzonedigital',
                                       soup_obj=page_soup)


    # html_doc = get_all_data().decode('UTF-8')
    # bs = BeautifulSoup(html_doc, 'html.parser')
    # #html_doc = """<ul class="foo">foo</ul><ul data-bin="Sdafdo39">"""
    # var = var = [item['jsondata'] for item in bs.find_all('table')]
