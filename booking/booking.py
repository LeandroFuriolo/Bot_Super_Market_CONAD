#constant manipulations ex "urls"
import booking.constants as const
#paths system manipulation
import os
# pip install csv "CSV manipulation"
import csv
# pip install pandas "data manipulations"
import pandas as pd
# pip install pathlib "path manipulations"
from pathlib import Path 
# pip install tabulate "list to tables"
from tabulate import tabulate
# pip install translate "translate variables"
from googletrans import Translator
# time instance manipulation
from datetime import date
# time wait manipulation
from time import sleep
# pip install schedule "run task periodically"
import schedule
# pip install winotify "make a windows notifications manager"
from winotify import Notification , audio
#------- S E L E N I U M ------
#PIP INSTALL SELENIUM "WEBDRIVER"
from selenium import webdriver
# selenium by "kind find element 'BY'"
from selenium.webdriver.common.by import By
# for implicity_wait of driver
from selenium.webdriver.support.ui import WebDriverWait
# to configure driver options
from selenium.webdriver.chrome.options import Options
# for which keys are useful
from selenium.webdriver.common.keys import Keys
# for waiting for specific conditions until a defined task is complete
from selenium.webdriver.support import expected_conditions as EC
# webbrowser controller
import webbrowser


class Booking(webdriver.Chrome):
    # driverpath = path of driversaved
    # os.environ Python is a mapping object that represents the user’s environmental variables
    # teardown variable is for close chrome driver if is true.
    # implicity_wait if for make a implicit wait to make the page element available
    def __init__(self, driver_path=r"C:\SeleniumDriver", teardown=False):
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += ";" + self.driver_path
        #to manipulate the driver options for example the path of downloading files
        options = webdriver.ChromeOptions()
        #List of Chrome command line switches to exclude that ChromeDriver by default passes when starting Chrome. Do not prefix switches with "--".
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        #Sets the user preferences for Chrome's user profile.
        options.add_experimental_option("prefs", {"download.default_directory": "C:\\Users\\Leandro\\Desktop\\PythonProjectsCode\\VSCPython\\Python_Selenium_Web_Scraping\\Bot_Super_Market_LIDL\\CSV Files"})
        super(Booking, self).__init__(options=options)
        self.implicitly_wait(15)
        self.maximize_window()
        #self.minimize_window()
        
    #for exiting of chrome web when teardown is True
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()

    #def validator(self):




    #user define a URL PAGE, this can be stay on constant and we put url like cons.BASE_URL into get
    def land_first_page(self, url=""):
        if url == "":
            # notifications of error
            nullurl = Notification(
               app_id="WEBSCRAPING SCRIPT",
               title="ADVERTENCE!", 
               msg="please specify a URL on land_first_page command",
               duration="long"                
            )
            nullurl.set_audio(audio.LoopingAlarm, loop=True)
            nullurl.show()
            self.close()
        else:
            self.get(f'{url}')

    #coockies controller
    def cookies(self, cookies=None):
        try:
            decline_button = self.find_element(By.ID, 
            'onetrust-reject-all-handler')
            decline_button.click()
            sleep(1)
        except:
            print("No cookies element with this class name. Skipping...")
            nullurl = Notification(
               app_id="COOKIES MENSAGGE",
               title="NOTIFICATION!", 
               msg="we dont need specify cookies denied",
               duration="long"                
            )
            nullurl.set_audio(audio.LoopingAlarm, loop=True)
            nullurl.show()

    #go to offerts for all people        
    def offerte_per_tutti(self):
        offerte = self.find_element(By.ID, 
        'link-1816593135')
        offerte.click()

    # go to order and pick up
    def ordina_e_ritira(self):
        ritira_option = self.find_element(By.CSS_SELECTOR,
        'div[class="uk-button uk-button-primary uk-width"]')
        ritira_option.click()

    # region selector, need user specification
    def CAP(self, direction):
        # user validator
        if direction != "":
            indirizzo_CAP = self.find_element(By.CSS_SELECTOR, 'label[class="location-finder-label"]')
            sleep(3)
            indirizzo_CAP.click()
            sleep(1)
            indirizzo_CAP.send_keys(direction)
            sleep(1)
            indirizzo_CAP.send_keys(Keys.ARROW_DOWN)
            indirizzo_CAP.send_keys(Keys.ENTER)
        else:
            # notifications of error
            nullurl = Notification(
               app_id="WEBSCRAPING SCRIPT",
               title="ADVERTENCE!", 
               msg="please specify a region on CAP with '' command",
               duration="long"                
            )
            nullurl.set_audio(audio.LoopingAlarm, loop=True)
            nullurl.show()
            self.close()

    # city of region selector, first option ID      
    def city_clickeable(self, id_city=None):
         # user validator
        if id_city == '1': 
            city = self.find_element(By.XPATH, f'/html/body/main/div[1]/div[2]/div[1]/div[2]/div[1]/div/div/div[1]/ul/li[{id_city}]/button')
            city.click()
        else:
            # notifications of error
            nullurl = Notification(
               app_id="WEBSCRAPING SCRIPT",
               title="ADVERTENCE!", 
               msg="please specify a Option on city_clickeable like 1 with '' command",
               duration="long"                
            )
            nullurl.set_audio(audio.LoopingAlarm, loop=True)
            nullurl.show()
            self.close()

    # city selector like enter
    def select_city(self):
        seleziona = self.find_element(By.CSS_SELECTOR, 'button[class="js-choose-store uk-button uk-button-primary"]')
        seleziona.click()

    # got o offerts list to scrap
    def offerte_per_tutti_in_portal(self):
        offerte = self.find_element(By.ID, 
        'link-926407072')
        offerte.click(); 
    # make report lists to download

    def report_list(self, condition=True):
        #list name
        self.product_list = []
        #headers
        self.product_list.append(
            ["Discount Date", "Product Name", "Product Name Trans." , "Original_Price", "Discount", "Discount Price", "Product Link"]
        )
        #records insertion
        while condition:
            #namber of products listed
            allproducts = self.find_elements(By.CSS_SELECTOR,'div[nkpage="ProductCard"]')
                #scraper one by one product listed
            for e in allproducts:
                discount = e.find_element(By.CSS_SELECTOR, 'span[class="badge-text uk-cursor-pointer"]').text
                #print(discount)
                discount_date = e.find_element(By.CSS_SELECTOR, 'div[class="discount-date"]').text
                #print(discount_date)
                product_name = e.find_element(By.CSS_SELECTOR, 'div[class="no-t-decoration product-description uk-position-relative"]').find_element(By.TAG_NAME, 'h3').text
                # product title translated
                trans = Translator()
                product_translated = trans.translate(product_name, dest='es').text
                #print(product_translated)
                original_price = e.find_element(By.CSS_SELECTOR, 'div[class="product-price-original f-roboto"]').text
                #print(original_price)
                discount_price = e.find_element(By.CSS_SELECTOR, 'div[class="product-price product-price-red f-roboto"]').text
                #print(discount_price)
                product_link = e.find_element(By.CSS_SELECTOR, 'a[class="product uk-flex uk-flex-middle"]').get_property('href')
                #print(product_link)
                #append records in list of products
                self.product_list.append(
                    [discount_date, product_name, product_translated, original_price, discount, discount_price, product_link]
                )
            #try to go at next page   
            try:
                nextpage = self.find_element(By.CSS_SELECTOR, 'a[aria-label="Pagina Successiva"]')
                nextpage.click()
                sleep(3)
            #skip next page
            except:
                condition = False

    #form of show the report "filo or tabulate table on CMD"
    def report_save(self, show=None):
        tolist = self.product_list
        #option 1 tabulate_table 
        if show == "tabulate_table":
            data_table = print(tabulate(tolist, headers="firstrow", tablefmt= "github"))
        #option 2 HTML table    
        elif show == "html_table":
            with open('products.html', 'w') as f:
                f.write(tabulate(tolist, headers="firstrow", tablefmt= "html"))
                self.get('C:\\Users\\Leandro\\Desktop\\PythonProjectsCode\\VSCPython\\Python_Selenium_Web_Scraping\\Bot_Super_Market_LIDL\\products.html')
        #send to csv file
        elif show == "file_table":
            #make a path variable
            df_headLines = pd.DataFrame(tolist)
            user = os.getlogin()
            today = date.today()
            today = f'Offerts {today}.csv'
            disk = 'C:\\Users\\'
            final_path = "\Desktop\PythonProjectsCode\VSCPython\Python_Selenium_Web_Scraping\Bot_Super_Market_LIDL\CSV Files\\"
            path = f'{disk}{user}{final_path}{today}'     
            #send to csv file
            df_headLines.to_csv(path, index=False, header=False)
        else:
            # notifications of error
            nullurl = Notification(
               app_id="WEBSCRAPING SCRIPT",
               title="ADVERTENCE!",
               msg="please specify a Option on report_save like:"
                   "tabulate_table"
                   "html_table"
                   "file_table",
               duration="long"
            )
            nullurl.set_audio(audio.LoopingAlarm, loop=True)
            nullurl.show()
            self.close()