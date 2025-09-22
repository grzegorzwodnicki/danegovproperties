from selenium import webdriver
from selenium.common.exceptions import TimeoutException, InvalidSessionIdException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.remote_connection import LOGGER
from selenium.webdriver import ActionChains
from fake_useragent import UserAgent
import time
import json
import sys
import logging


class Scrapper:

    def __init__(self, chrome_driver_path, binary_location='',logging = None, show_browser=False):
        self.chromedriver = chrome_driver_path
        self.chromeBinaryLocation = binary_location
        self.log = []
        self.logger = logging
        self.show_browser = show_browser

    def addLog(self, text, error=False):                
        self.logger.info(text)
    def preparingCSVData(self, offerUrl):
        self.openBrowser(offerUrl)
        self.add("Browser opened")
        self.add("Starting scrapping data and preparing CSV")
        
        
    def openBrowser(self, _url):
        self.addLog("Opening browser: "+_url)
        options = Options()
        ua = UserAgent()
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
#                options.add_argument('--no-sandbox')
        options.add_argument('user-agent={}'.format(ua['google chrome']))
        if self.show_browser == False:
            options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1200,900')
    
        if self.chromeBinaryLocation != '':
            options.binary_location = self.chromeBinaryLocation
        self.chDriver = webdriver.Chrome(
            self.chromedriver, options=options, desired_capabilities=caps)
        self.chDriver.get(_url)
        
        
        wait = WebDriverWait(self.chDriver, 60)
        action = ActionChains(self.chDriver)

        self.chDriver.maximize_window()


      
    def closeBrowser(self):
        self.chDriver.close()
        

    