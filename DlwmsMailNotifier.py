from selenium import webdriver
import smtplib
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import getpass
import time


options = Options()
options.add_argument('--headless')

#opening page DLWMS - a
browser = webdriver.Firefox(executable_path=r'C:\Users\talicni\Downloads\geckodriver-v0.24.0-win64\geckodriver.exe')
browser.get('https://www.fit.ba/student/login.aspx')

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

#Sending mail using SMTP
def sendMail(message):
    server = smtplib.SMTP('smtp.live.com', 587)
    server.ehlo()
    server.starttls()
    fromAdd = 'aldin.talic@outlook.com'
    toAdd = 'aldin.talic@outlook.com'
    subject = 'NOVA OBAVIJEST NA SISTEMU !!!  ' + message
    header = 'To: ' + fromAdd + '\n' + 'From: ' + toAdd + '\n' + 'Subject: ' + subject
    msg = 'Subject: OBAVIJEST !!!' + '\n' + message
    server.login(fromAdd, passEmail)
    server.sendmail(fromAdd, toAdd, header)
    server.quit()

login()
print("CONNECTED TO DLWMS !")

#Getting pass for email account
passEmail = getpass.getpass("Password za mail:")

#waiting for loading page
browser.implicitly_wait(10)

#Getting date and time for last notification on DLWMS
datumVrijeme = browser.find_element_by_id('lblDatum')
datumVrijeme = datumVrijeme.text[:len(datumVrijeme.text)-1]

#infinite loop
while True:
    tempDatumVrijeme = browser.find_element_by_id('lblDatum')
    tempDatumVrijeme = tempDatumVrijeme.text[:len(tempDatumVrijeme.text)-1]
    
    #getting date and time for last notification and checking if it different from datumVrijeme
    if tempDatumVrijeme != datumVrijeme:
        obavijest = browser.find_element_by_id('lnkNaslov').text
        sendMail(obavijest)
        datumVrijeme = tempDatumVrijeme
    
    #waiting 20 seconds and then refreshing page
    time.sleep(20)
    browser.refresh()
    browser.implicitly_wait(10)
