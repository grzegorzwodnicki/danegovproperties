from selenium import webdriver
from selenium.common.exceptions import TimeoutException, InvalidSessionIdException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from datetime import date, timedelta

import time
import json
import sys
import logging
import pandas as pd
import os

class Scrapper:

    def __init__(self, _config,current_directory, logging = None):
        self.config = _config

        self.log = []
        self.logger = logging
        self.current_directory = current_directory
        #temporary file for generate and upload data
        self.output_file = os.path.join(current_directory, 'dane_nieruchomosc.csv')
        #filename for uploaded file
        self.output_uploaded_file = os.path.join(current_directory, 'dane_nieruchomosc_uploaded.csv')
        
    def addLog(self, text, error=False):                
        self.logger.info(text)
        
    def importData(self, tableData):
        trs = tableData.find_elements(By.TAG_NAME,'tr')
        tab = []
        for t in trs:
            fields = t.find_elements(By.TAG_NAME, 'td')
            
            if (len(fields) > 12):
                rec = {}
                rec['Nr lokalu'] = fields[1].text
                rec['Status'] = fields[5].text
                rec['Cena Brutto'] = fields[6].text.replace(" ","").replace("zł", "")
                rec['Cena za 1m2'] = fields[7].text.replace(",",'.').replace("zł", "")
                rec['Powierzchnia (m2)'] = fields[3].text.replace(',','.').replace('m²','')
                rec['Województwo'] = self.config.wojewodztwo
                rec['Powiat'] = self.config.powiat
                rec['Miejscowość'] = self.config.miejscowosc
                rec['Ulica'] = self.config.ulica
                rec['Kod pocztowy'] = self.config.kod_pocztowy
                rec['Rodzaj nieruchomości'] = self.config.rodzaj_nieruchomosci
                rec['Pomieszczenie przynależne'] = fields[11].text
                rec['Inne świadczenia pienieżne'] = fields[12].text
                rec['Wartość świadczeń pieniężnych (zł)'] = self.config.wartosc_swiadczen
                rec['Cena obowiązuje od'] = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
                rec['Cena obowiązuje do'] = date.today().strftime("%Y-%m-%d")
                
                rec['Link do prospektu']  = fields[9].find_element(By.TAG_NAME,'a').get_attribute('href')
                rec['Telefon kontaktowy'] = self.config.telefon
                rec['E-mail kontaktowy'] = self.config.email
                rec['Nazwa dewelopera'] = self.config.nazwaDevelopera
                tab.append(rec)
                #for f in fileds:
                #    print(f.text)
        return tab

    def preparingCSVData(self, offerUrl):
        self.openBrowser(offerUrl)
        self.addLog("Browser opened")
        self.addLog("Starting scrapping data and preparing CSV")
        descriptions = self.chDriver.find_elements(By.CSS_SELECTOR, ".cell1")
        if (len(descriptions)>0):
            self.addLog(f"Found {len(descriptions)} tables with data")
            parent_element = descriptions[0].find_element(By.XPATH, "..")
            
            tables = parent_element.find_elements(By.CSS_SELECTOR, ".custom-table")
            ds_table = pd.DataFrame()
            
            if len(descriptions) != len(tables):
                self.addLog("Error duting maching description with tables")
            else:
              for i in range(len(descriptions)):
    
                  if ('nie w sprzedaży' not in descriptions[i].text):
                      self.addLog(f"Importing table {i+1}")
                      tab = self.importData(tables[i])
                      if (len(tab)>0):
                          ds_table = pd.concat([ds_table, pd.DataFrame(tab)], ignore_index=True)
                  else:
                      self.addLog(f"Table {i+1} does not contain sale data, skipping")
            print(">>>>> ===================== <<<<<<<<<")
            print(ds_table)
            ds_table.to_csv(self.output_file, index=False, encoding="utf-8")
            
        self.closeBrowser()
    def uploadData(self):
        self.addLog("Opening portal dane.gov")
        self.openBrowser(self.config.portalUrl)
        time.sleep(3)
        self.addLog("Closing popups")
        #check for any popups
        popup_button = self.chDriver.find_elements(By.ID, "footer-close")
        for ft in popup_button:

            ft.click()
            time.sleep(0.1)
        self.addLog("Clicking on login button")
        all_links = self.chDriver.find_elements(By.LINK_TEXT, 'Zaloguj się')

        found_link = False
        for lnk in all_links:
            if lnk.tag_name.upper() == 'A':
                lnk.click()
                found_link = True


        if found_link == False:
            self.addLog("Login link not found")
            sys.exit(1)                
        time.sleep(1)
        self.addLog("Clicking on email login button")
        btns = self.chDriver.find_elements(By.ID, "email-button")
        if len(btns) == 0:
            self.addLog("Email login button not found")
            sys.exit(1)
        btns[0].click()
        time.sleep(2)
        self.addLog("Login into dane gov")
        _emails = self.chDriver.find_elements(By.ID, 'email')
        _passwords = self.chDriver.find_elements(By.ID, 'password')
        if len(_emails) == 0 or len(_passwords) == 0:
            self.addLog("Email or password field not found")
            sys.exit(1)

        set_value = """
        const el = arguments[0];
        const val = arguments[1];
        el.focus();
        el.value = val;
        el.dispatchEvent(new Event('input', {bubbles: true}));
        el.dispatchEvent(new Event('change', {bubbles: true}));
        """
        

        email = self.chDriver.find_element(By.CSS_SELECTOR, "input#email[name='email']")
        self.chDriver.execute_script(set_value, _emails[0], self.config.portalUsername)

        pwd = self.chDriver.find_element(By.CSS_SELECTOR, "input#password, input[type='password']")
        self.chDriver.execute_script(set_value, _passwords[0], self.config.portalPassword)


        self.chDriver.find_element(By.ID, 'submit-button').click()

        

        time.sleep(500)
        
    def openBrowser(self, _url):
        chrome_options = Options()
        ua = UserAgent()
        # preparing UA options
        chrome_options.add_argument('user-agent={}'.format(ua['google chrome']))
        if not self.config.show_browser:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--ignore-ssl-errors")        

        service = Service(ChromeDriverManager().install())
        self.chDriver = webdriver.Chrome(
             options = chrome_options,service=service
        )
        self.chDriver.get(_url)
        
        
        
      
    def closeBrowser(self):
        self.chDriver.close()
        

    