import platform
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from config import download_temp_path, get_driver_path


def get_browser() -> WebDriver:
    options = webdriver.ChromeOptions()
    # for downloading PDF file
    prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': download_temp_path}
    options.add_experimental_option('prefs', prefs)

    browser = webdriver.Chrome(executable_path=get_driver_path(), options=options)
    return browser
