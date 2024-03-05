from bs4 import BeautifulSoup
from config import configure_driver
from config import today, tomorrow
import time

driver = configure_driver()

today = today()
tomorrow = tomorrow()


def open_url(url, checkin, checkout):
    # url = f'{url}?checkin=2024-03-07&checkout=2024-03-08'
    url = f'{url}?checkin={checkin}&checkout={checkout}'
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # open('test.html', 'w').write(str(soup))
    return soup
