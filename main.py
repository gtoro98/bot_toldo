from threading import Timer
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
import os 
from selenium.webdriver.support.ui import Select
import datetime as dt
from datetime import timedelta
import sys

load_dotenv()

#opciones de toldo
fila = 5  # Fila E (A: 1, B: 2, C: 3, D: 4, E: 5, F: 6, G: 7, H: 8)
num_toldo = 13

def find_element_custom(browser, by, path):
        element = 'undefined'
        while element == 'undefined':
            try:
                element = browser.find_element(by, path)
            except:
                pass
        return element

def select_by_value_custom(select, value, number):
    bool = True
    

    while bool:
        value_string = value + str(number)
        try:
            select.select_by_value(value_string)
            bool = False
            return number
            break
        except:
            if number < 21: 
                number += 1
            else:
                number -=1
            pass

def login(browser):
    user_name = os.getenv('USER_NAME')
    password = os.getenv('PASSWORD')

    browser.get('https://www.camurigrande.auditoriamovil.com/index.php')
    
    find_element_custom(browser, By.NAME, 'correo').send_keys(user_name)
    
    find_element_custom(browser, By.NAME, 'contrasena').send_keys(password)
    find_element_custom(browser, By.XPATH, "//button[contains(text(), 'Ingresar')]").click()
    #time.sleep(3)
    #browser.find_element(By.XPATH, "//form[@name='form_perfil']/button[1]").click()

def reserva (browser):
    browser.get('https://www.camurigrande.auditoriamovil.com/tu_perfil.php?op=soc_kiosko_reserva')
    Select(find_element_custom(browser, By.TAG_NAME, "select")).select_by_index(1)
    find_element_custom(browser, By.XPATH, "//button[contains(text(), 'Iniciar Reserva')]").click()
    select_toldo(browser)
    
    time.sleep(5)

def select_toldo(browser):

    #seleccione el tipo de reserva
    Select(find_element_custom(browser, By.ID, "tipo-reserva")).select_by_index(1)

    #seleccione la fila
    row = select_by_value_custom(Select(find_element_custom(browser, By.ID, "fila")), "FIL-000", fila)
    print(row)
    print(chr(row + 64))
    #seleccione la fila
    select_by_value_custom(Select(find_element_custom(browser, By.ID, "col")), "T186-KI-" + chr(row + 64), num_toldo)

    find_element_custom(browser, By.XPATH, "//button[contains(text(), 'Continuar')]").click()

def main():
    # Initiate the browser
    option = webdriver.ChromeOptions()
    option.add_argument('--lang=en-US')
    option.add_argument('--window-size=1200,1000')

    driverPath = 'C:\\webdriver\\chromedriver.exe'
    browser=webdriver.Chrome(driverPath,chrome_options=option)

    login(browser)
    reserva(browser)
    sys.exit()

today = dt.datetime.now()
day_of_the_week = today.weekday()

if day_of_the_week <= 3:
    time_delta = 3 - day_of_the_week
else:
    time_delta = 6 - day_of_the_week + 4

nxt_thursday = today + dt.timedelta(days=time_delta)
nxt_thursday = nxt_thursday.replace(hour=12, minute=0, second=0, microsecond=0)
print(nxt_thursday)
delay = (nxt_thursday - today).total_seconds()
print(delay)
Timer(1,main,()).start()