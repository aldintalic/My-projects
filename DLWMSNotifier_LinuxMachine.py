from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import getpass
import time
import telegram

options = Options()
options.add_argument('--headless')

#opening page DLWMS 
browser = webdriver.Firefox(executable_path=r'/usr/local/bin/geckodriver', options=options)
browser.get('https://www.fit.ba/student/login.aspx')
telegram_token =''

#Login on DLWMS
def login():
    brojIndeksa = raw_input("Unesite broj indeksa:")
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
        naslov = browser.find_element_by_id('lnkNaslov')
        naslov.click()
        link = browser.current_url
        naslov = browser.find_element_by_id('lnkNaslov').text
        message = '[' + naslov + '](' + link + ')' + '\n\n'
        message += '*Datum: *' + '_' + tempDatumVrijeme[:10] + '_'
        message += '\n*Vrijeme: *' + '_' + tempDatumVrijeme[11:] + 'h _'
        message += '\n*Predmet: *' + '_' + browser.find_element_by_id('lblPredmet').text +'_'
        message += '\n*Autor: *' + '_' + browser.find_element_by_id('linkNapisao').text + '_'
        sendTelegramMsg(message, '')
        datumVrijeme = tempDatumVrijeme
        browser.find_element_by_id('home').click()
        
    #waiting 60 seconds and then refreshing page
    time.sleep(60)
    browser.refresh()
    browser.implicitly_wait(10)
