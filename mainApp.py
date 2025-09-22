import configClass
import os
import sys
import pandas
import scrapper
import logging
def preparingData(_configObject):
    _scrapper = scrapper.Scrapper(_configObject.chrome_driver_path, _configObject.chrome_binary_location,logging, _configObject.show_browser)
    _scrapper.preparingCSVData(_configObject.offerUrl)
    
    
def sendingData(_configObject):
    pass


def main():
    current_directory = os.path.dirname(__file__)
    _config = configClass.configClass(os.path.join(current_directory,'config.ini'))
    
    
    _config = configClass.configClass(
    os.path.join(current_directory, 'config.ini'))

    _log_file = os.path.join(current_directory, _config.log_file)
    if _config.log_output == 'SCREEN':
        logging.basicConfig(level=_config.logging_level,
                        format='%(asctime)s:  %(message)s')
    else:
        logging.basicConfig(level=_config.logging_level,
                        filename=_log_file, format='%(asctime)s:  %(message)s')

    chrome_driver_path = os.path.join(
    current_directory, _config.chrome_driver_path)
    logging.info("Starting program")


    preparingData(_config)
    




if __name__ == "__main__":
    main()
    
    