import configparser
import logging
import sys

class configClass:
    def __init__(self,config_file):
        self.log_file = ""
        self.logging_level = logging.NOTSET        
        self.log_output = ""
        self.chrome_driver_path = ""
        self.chrome_binary_location = ""
        self.show_browser = True

        
        self.telefon = ""
        self.email = ""
        self.nazwaDevelopera = ""
        self.wojewodztwo = ""
        self.powiat = ""
        self.miejscowosc = ""
        self.ulica = ""
        self.kod_pocztowy = ""
        self.rodzaj_nieruchomosci = ""
        self.wartosc_swiadczen = 0
        self.portalUrl = ""
        self.portalUsername = ""
        self.portalPassword = ""
        self.publishData = False
        
        self.read_file(config_file)

    def get_value(self,cnf,section,key,default):
        
        if section in cnf:            
            if key in cnf[section]:
                return cnf[section][key]
        return default

    def read_file(self,config_file):
        config = configparser.ConfigParser()
        print("Config file:",config_file)
        config.read(config_file)

        self.log_file = self.get_value(config,'logging','log_file','log_file.txt')
        log_level = self.get_value(config,'logging','log_level','NOTSET')

        if log_level == 'NOTSET':
            self.logging_level = logging.NOTSET
        if log_level == 'DEBUG':
            self.logging_level = logging.DEBUG
        if log_level == 'WARNING':
            self.logging_level = logging.WARNING
        if log_level == 'ERROR':
            self.logging_level = logging.ERROR
        if log_level == 'CRITICAL':
            self.logging_level = logging.CRITICAL

        self.log_output = self.get_value(config,'logging','log_output','SCREEN')
        self.chrome_driver_path = self.get_value(config,'scrapper','chrome_driver_path','chrome_driver/chromedriver')
        self.chrome_binary_location = self.get_value(config,'scrapper','chrome_binary_path','')
        self.show_browser = self.get_value(config,'scrapper', 'show_browser','1') == '1'
        self.offerUrl = self.get_value(config, 'offersParameters','offerUrl', 'https://ametystowa.pl/oferta-domow/')
        self.telefon =  self.get_value(config, 'offersParameters', 'telefon','')
        self.email = self.get_value(config, 'offersParameters', 'email','')
        self.nazwaDevelopera = self.get_value(config, 'offersParameters', 'nazwaDevelopera','')
        self.wojewodztwo = self.get_value(config, 'offersParameters', 'wojewodztwo','')
        self.powiat = self.get_value(config, 'offersParameters', 'powiat','')
        self.miejscowosc = self.get_value(config, 'offersParameters', 'miejscowosc','')
        self.ulica = self.get_value(config, 'offersParameters', 'ulica','')
        self.kod_pocztowy = self.get_value(config, 'offersParameters', 'kod_pocztowy','')
        self.rodzaj_nieruchomosci = self.get_value(config, 'offersParameters', 'rodzaj_nieruchomosci','')
        self.wartosc_swiadczen = int(self.get_value(config, 'offersParameters', 'wartosc_swiadczen','0'))
        self.portalUrl = self.get_value(config, 'uploadParameters', 'portalUrl','')
        self.portalUsername = self.get_value(config, 'uploadParameters', 'username','')
        self.portalPassword = self.get_value(config, 'uploadParameters', 'password','')
        self.publish_data = self.get_value(config,'uploadParameters', 'publish_data','0') == '1'
        
 
        
        

        




if __name__ == "__main__":
    print("configClass test")
    cn = configClass("config.ini")
    
    print(cn.log_file)
    print(cn.log_output)