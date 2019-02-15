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

from selenium.webdriver.common.keys import Keys

names = []


wb = openpyxl.load_workbook("plants2.xlsx", data_only=True) #open your desired workbook
print(wb.sheetnames)
ws = wb[wb.sheetnames[0]]
num_rows = ws.max_row #this grabs too many rows for unclear reasons. must edit later.
print(num_rows)


cell_range = ws["A":"A"]
cell_range = np.asarray(cell_range)[1:] #turn it into a useful format
for m in np.arange(len(cell_range)): 
	# print(n, str(cell_range[n][0].value), str(cell_range[n][1].value))
	try:cell_range[m] = str(cell_range[m].value) #convert from objects to strings
	except: 
		# print(cell_range[m])
		quit()
cell_range = cell_range.astype(str)
try: 
	index_of_null = np.min(np.where(cell_range == ["None"])[0])
except ValueError: index_of_null = len(cell_range)
cell_range = cell_range[:index_of_null] #trim the nulls
for m in np.arange(len(cell_range)): 
	# print(m, str(cell_range[m].replace(u'\xa0', "")))
	cell_range[m] = str(cell_range[m].replace(u'\xa0', ""))



driver = webdriver.Chrome("C:\chromedriver")
driver.get('https://calscape.org/')
good_options = []
for plant_name in cell_range:
	search_box = driver.find_element_by_name('sp')
	search_box.clear()
	search_box.send_keys(plant_name) #(Keys.chord(Keys.CONTROL, "a"), plant_name))
	driver.find_element_by_xpath('//*[@id="form_search"]/a').click()

	soup = BeautifulSoup(driver.page_source, "html.parser")
	try:
		soup = soup.select("div.page_column_left")[0].select("div.species_view")[0].select("div.content.plant_info")[0].select("div")[0].select("div")
		for datum in np.arange(len(soup)):
			if soup[datum].get_text(strip=True)[:8] == "Drainage":
				if soup[datum+1].get_text(strip=True) == "Standing":
					good_options.append(plant_name)
				else: pass
			else: pass
	except: pass


print(good_options)
