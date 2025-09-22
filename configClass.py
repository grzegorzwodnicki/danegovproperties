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
        

        




if __name__ == "__main__":
    print("configClass test")
    cn = configClass("config.ini")
    
    print(cn.log_file)
    print(cn.log_output)