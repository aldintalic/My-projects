from selenium import webdriver
import smtplib
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import getpass
import time
import telegram

options = Options()
options.add_argument('--headless')

#opening page DLWMS - a
browser = webdriver.Firefox(executable_path=r'C:\Users\talicni\Downloads\geckodriver-v0.24.0-win64\geckodriver.exe', options=options)
browser.get('https://www.fit.ba/student/login.aspx')
telegram_token = '837912044:AAEg-fuq-WGSNhwJpPKxskdQkMWgZxu6yR4'

#Login on DLWMS
def login():
    brojIndeksa = input("Unesite broj indeksa:")
    lozinka = getpass.getpass("Unesite lozinku:")

    ib = browser.find_element_by_id('txtBrojDosijea')
    ib.send_keys(brojIndeksa)

    loz = browser.find_element_by_id('txtLozinka')
    loz.send_keys(lozinka)

    btn = browser.find_element_by_id('btnPrijava')
    btn.click()

def sendTelegramMsg(msg, chat_id, token = telegram_token):
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg, parse_mode=telegram.ParseMode.MARKDOWN)

login()
print("CONNECTED TO DLWMS !")

#waiting for loading page
browser.implicitly_wait(10)

#Getting date and time for last notification on DLWMS
datumVrijeme = browser.find_element_by_id('lblDatum')
datumVrijeme = datumVrijeme.text[:len(datumVrijeme.text)-1]

#infinite loop...
while True:
    tempDatumVrijeme = browser.find_element_by_id('lblDatum')
    tempDatumVrijeme = tempDatumVrijeme.text[:len(tempDatumVrijeme.text)-1]
    #getting date and time for last notification and checking if it different from datumVrijeme
    if tempDatumVrijeme != datumVrijeme:
        obavijest = browser.find_element_by_id('lnkNaslov').text
        sendTelegramMsg(obavijest, '612482025')
        datumVrijeme = tempDatumVrijeme

    #waiting 20 seconds and then refreshing page
    time.sleep(20)
    browser.refresh()
    browser.implicitly_wait(10)
