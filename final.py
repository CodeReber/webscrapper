from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtWidgets import QApplication
from bs4 import BeautifulSoup as bs
import sqlite3
from datetime import date
import datetime
import os, sys
from PyQt5.uic import loadUiType

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
FORM_CLASS,_=loadUiType(resource_path("main.ui"))

class Main(QMainWindow, FORM_CLASS):
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    con = sqlite3.connect(resource_path("scrap.db"))
    cur = con.cursor()
    cur1 = con.cursor()
    cur2 = con.cursor()
    #cur.execute("DELETE from scrap;")
    #file1 = "C:\\Users\\azure\\Desktop\\Penn_DATA\compare\\file1\\disk.html"
    #file2 = "C:\\Users\\azure\\Desktop\\Penn_DATA\compare\\file1\\disk.html"
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        self.setupUi(self)
        self.Handel_Buttons()

    def Handel_Buttons(self):
        self.pushButton.clicked.connect(self.scrapeit)
        self.pushButton_2.clicked.connect(self.phy_current_compare)
        self.pushButton_4.clicked.connect(self.vm_current_compare)

    def scrapeit(self):
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        file1 = resource_path("file1\\disk.html")
        con = sqlite3.connect(resource_path("scrap.db"))
        cur = con.cursor()
        cur.execute("DELETE from scrap;")
        cur.execute("DELETE from vm_org;")
        with open(file1, 'r') as f:

            contents = f.read()

            soup = bs(contents, 'html.parser')
            for name in soup.find_all("td", class_="qqp0_c0"):
                hostname = name.parent.find('td').get_text()
                drive = name.parent.find('td', class_="qqp0_c1").get_text()
                used_percent = name.parent.find('td', class_="qqp0_c5").get_text()
                value = {'host': hostname, 'drive': drive, 'percent': used_percent, 'date': d1}  
                cur.execute("INSERT INTO scrap (hostname, drive, perc, Date) VALUES (:host, :drive, :percent, :date);", value)
                #print(value)
            for name in soup.find_all("td", class_="qqp2_c0"):
                hostname = name.parent.find('td').get_text()
                drive = name.parent.find('td', class_="qqp2_c1").get_text()
                used_percent = name.parent.find('td', class_="qqp2_c4").get_text()
                value = {'host': hostname, 'drive': drive, 'percent': used_percent, 'date': d1}  
                cur.execute("INSERT INTO vm_org (hostname, drive, perc, Date) VALUES (:host, :drive, :percent, :date);", value)

        con.commit()
        # Once adding to database is complete, display confirmation message
        msgBox = QMessageBox()
        msgBox.setText("Added to database")
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        # Once OK is selected, reset all values
        if returnValue == QMessageBox.Ok:
            print("ok")

    def phy_current_compare(self):
        #tomorrow = date.today() + datetime.timedelta(days=1)
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        file1 = resource_path("file2\\disk.html")
        con = sqlite3.connect(resource_path("scrap.db"))
        cur = con.cursor()
        cur1 = con.cursor()
        cur2 = con.cursor()
        cur.execute("DELETE from sheet1;")
        cur.execute
        #Open the file perform scrape and insert into DB
        with open(file1, 'r') as f:

            contents = f.read()

            soup = bs(contents, 'html.parser')
            for name in soup.find_all("td", class_="qqp0_c0"):
                hostname = name.parent.find('td').get_text()
                drive = name.parent.find('td', class_="qqp0_c1").get_text()
                used_percent = name.parent.find('td', class_="qqp0_c5").get_text()
                value = {'host': hostname, 'drive': drive, 'percent': used_percent, 'date': d1}  
                cur.execute("INSERT INTO sheet1 (hostname, drive, perc, Date) VALUES (:host, :drive, :percent, :date);", value)
                #print(value)
        #Put DB query results into table
        dt1 = "24/12/2021"
        dt2 = "25/12/2021" 
        results_table = cur.execute("select sh1.hostname, sh1.drive, sh1.perc, sh2.perc from scrap as sh1, sheet1 as sh2 where sh1.hostname = sh2.hostname AND sh1.drive = sh2.drive")
        #results_table_dropped = cur1.execute("select distinct hostname from scrap where hostname not in (select hostname from sheet1)")
        #results_table_added = cur2.execute("select distinct hostname from sheet1 where hostname not in (select hostname from scrap)")
        self.tableWidget_5.setRowCount(0)
        #self.tableWidget.setRowCount(0)
        #self.tableWidget_2.setRowCount(0)

        #Loop through and output to the result table
        for rownum, rowdata in enumerate(results_table):
            self.tableWidget_5.insertRow(rownum)
            for columnnum, data in enumerate(rowdata):
                self.tableWidget_5.setItem(rownum, columnnum, QTableWidgetItem(str(data)))
        self.tableWidget_5.resizeColumnsToContents()
        #self.label_2.setText("4")
        #Loop through and output to the dropped table
        # for rownum, rowdata in enumerate(results_table_dropped):
        #     self.tableWidget.insertRow(rownum)
        #     for columnnum, data in enumerate(rowdata):
        #         self.tableWidget.setItem(rownum, columnnum, QTableWidgetItem(str(data)))

        #Loop through and output to the added table
        # for rownum, rowdata in enumerate(results_table_added):
        #     self.tableWidget_2.insertRow(rownum)
        #     for columnnum, data in enumerate(rowdata):
        #         self.tableWidget_2.setItem(rownum, columnnum, QTableWidgetItem(str(data)))

        con.commit()
        # Once adding to database is complete, display confirmation message
        msgBox = QMessageBox()
        msgBox.setText("Added to database")
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        # Once OK is selected, reset all values
        if returnValue == QMessageBox.Ok:
            print("ok")

    def vm_current_compare(self):
        #tomorrow = date.today() + datetime.timedelta(days=1)
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        file1 = resource_path("file2\\disk.html")
        con = sqlite3.connect(resource_path("scrap.db"))
        cur = con.cursor()
        cur1 = con.cursor()
        cur2 = con.cursor()
        cur.execute("DELETE from vm_current;")
        #Open the file perform scrape and insert into DB
        with open(file1, 'r') as f:

            contents = f.read()

            soup = bs(contents, 'html.parser')

            for name in soup.find_all("td", class_="qqp2_c0"):
                hostname = name.parent.find('td').get_text()
                drive = name.parent.find('td', class_="qqp2_c1").get_text()
                used_percent = name.parent.find('td', class_="qqp2_c4").get_text()
                value = {'host': hostname, 'drive': drive, 'percent': used_percent, 'date': d1}  
                cur.execute("INSERT INTO vm_current (hostname, drive, perc, Date) VALUES (:host, :drive, :percent, :date);", value)
                #print(value)
        #Put DB query results into table
        dt1 = "24/12/2021"
        dt2 = "25/12/2021" 
        results_table = cur.execute("select DISTINCT sh1.hostname, sh1.drive, sh1.perc, sh2.perc from vm_org as sh1, vm_current as sh2 where sh1.hostname = sh2.hostname AND sh1.drive = sh2.drive")
        #results_table_dropped = cur1.execute("select distinct hostname from scrap where hostname not in (select hostname from sheet1)")
        #results_table_added = cur2.execute("select distinct hostname from sheet1 where hostname not in (select hostname from scrap)")
        self.tableWidget.setRowCount(0)
        #self.tableWidget.setRowCount(0)
        #self.tableWidget_2.setRowCount(0)

        #Loop through and output to the result table
        for rownum, rowdata in enumerate(results_table):
            self.tableWidget.insertRow(rownum)
            for columnnum, data in enumerate(rowdata):
                self.tableWidget.setItem(rownum, columnnum, QTableWidgetItem(str(data)))
        self.tableWidget.resizeColumnsToContents()
        #self.label_2.setText("4")
        #Loop through and output to the dropped table
        # for rownum, rowdata in enumerate(results_table_dropped):
        #     self.tableWidget.insertRow(rownum)
        #     for columnnum, data in enumerate(rowdata):
        #         self.tableWidget.setItem(rownum, columnnum, QTableWidgetItem(str(data)))

        #Loop through and output to the added table
        # for rownum, rowdata in enumerate(results_table_added):
        #     self.tableWidget_2.insertRow(rownum)
        #     for columnnum, data in enumerate(rowdata):
        #         self.tableWidget_2.setItem(rownum, columnnum, QTableWidgetItem(str(data)))

        con.commit()
        # Once adding to database is complete, display confirmation message
        msgBox = QMessageBox()
        msgBox.setText("Added to database")
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        # Once OK is selected, reset all values
        if returnValue == QMessageBox.Ok:
            print("ok")
def main():
    
    app=QApplication(sys.argv)
    window=Main()
    window.show()
    app.exec_()

if __name__=='__main__':
    main()   