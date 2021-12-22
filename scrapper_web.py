# Dependencies
from bs4 import BeautifulSoup as bs
import sqlite3
import requests
from datetime import date

today = date.today()
d2 = today.strftime("%d/%m/%Y")
d1 = "19/12/2021"
url = "http://127.0.0.1:5000/"
req = requests.get(url)
con = sqlite3.connect("scrap.db")
cur = con.cursor()
cur1 = con.cursor()
cur.execute("DELETE from scrap;")
def srapeit():
    soup = bs(req.content, 'html.parser')
    for name in soup.find_all("td", class_="qqp0_c0"):
        hostname = name.parent.find('td').get_text()
        drive = name.parent.find('td', class_="qqp0_c1").get_text()
        used_percent = name.parent.find('td', class_="qqp0_c5").get_text()
        value = {'host': hostname, 'drive': drive, 'percent': used_percent, 'date': d1}  
        cur.execute("INSERT INTO scrap (hostname, drive, perc, Date) VALUES (:host, :drive, :percent, :date);", value)
        #print(value)

    con.commit()
    con.close()

def srapeit2():
    soup = bs(req.content, 'html.parser')
    for name in soup.find_all("td", class_="qqp0_c0"):
        hostname = name.parent.find('td').get_text()
        drive = name.parent.find('td', class_="qqp0_c1").get_text()
        used_percent = name.parent.find('td', class_="qqp0_c5").get_text()
        value = {'host': hostname, 'drive': drive, 'percent': used_percent, 'date': d2}  
        cur.execute("INSERT INTO sheet1 (hostname, drive, perc, Date) VALUES (:host, :drive, :percent, :date);", value)
        #print(value)

    con.commit()
    con.close()

srapeit()   