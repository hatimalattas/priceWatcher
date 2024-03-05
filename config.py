from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time


def today():
    return time.strftime("%Y-%m-%d")


def tomorrow():
    return time.strftime("%Y-%m-%d", time.gmtime(time.time() + 86400))


def configure_driver():
    # Set up Selenium with ChromeDriver
    options = Options()
    options.headless = True  # Run in headless mode

    # Set the user agent to an iPhone so that we get the mobile version of the website
    user_agent = ("Mozilla/5.0 (iPhone; CPU iPhone OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "CriOS/121.0.0.0 Mobile/15E148 Safari/604.1")
    options.add_argument(f'--user-agent={user_agent}')

    # Set the window size to 360x640
    driver = webdriver.Chrome(options=options)
    return driver
