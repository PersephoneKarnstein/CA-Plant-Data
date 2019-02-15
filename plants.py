import tkinter as tk
from tkinter import ttk
from tkinter import *
import numpy as np 
import warnings, tkFileDialog, shutil, sys, os

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=UserWarning)

import time, re, openpyxl
from selenium import webdriver
from bs4 import BeautifulSoup

if os.path.isfile("plants2.xslx") == True:
	os.remove("plants2.xlsx")
else: pass

names = []

wb = openpyxl.Workbook()
ws = wb.active
ws = wb[wb.sheetnames[0]]
driver = webdriver.Chrome("C:\chromedriver")
driver.get('http://www.calflora.org/cgi-bin/specieslist.cgi?namesoup=&countylist=any&lifeform=Herb&lifeform=Shrub&native=t&plantcomm=m45&format=photos&orderby=taxon')
soup = BeautifulSoup(driver.page_source, "html.parser")
for n in np.arange(len(soup.find_all("a", class_="blueLink"))):
			names.append(soup.find_all("a", class_="blueLink")[n].get_text())
while True:
	try:
		driver.find_element_by_name('next').click()
		soup = BeautifulSoup(driver.page_source, "html.parser")
		for n in np.arange(len(soup.find_all("a", class_="blueLink"))):
			names.append(soup.find_all("a", class_="blueLink")[n].get_text())
		print(len(names))
	except:
		break

for n in np.arange(len(names)): 
	ws.cell(column=1, row=n+1, value=names[n])
	print(n)
wb.save("plants2.xlsx")
