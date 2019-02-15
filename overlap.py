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


wb = openpyxl.load_workbook("plants.xlsx", data_only=True) #open your desired workbook
print(wb.sheetnames)
ws = wb[wb.sheetnames[0]]
# num_rows = ws.max_row #this grabs too many rows for unclear reasons. must edit later.
# print(num_rows)

#import and clean plant lists
namesarray = np.asarray([["A", "B", "C", "D", "E"],["Mixed_Evergreen", "Northern_Juniper_Woodland", "Redwood_Forest", "Pinyon_Juniper_Woodland", "Chaparral"]]).T
# print(namesarray)
for n in np.arange(len(namesarray)):
	# print(namesarray[n][1])
	cell_range = ws[namesarray[n][0]:namesarray[n][0]]
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
	# print(cell_range)
	globals()[str(namesarray[n][1])] = cell_range
	# print(str(namesarray[n][1]))
	# print(globals()[str(namesarray[n][1])])

# build overlap lists of biomes
#n and m here represent the column numbers that you want to calculate overlap for. By returning it to the commented versions next to lines 54 and 55, you can also calculate the overlap for every column with every other column.
overlap_names = []
for n in np.asarray([1,2]): # for n in np.arange(len(namesarray)): 
	for m in np.asarray([4]):# for m in np.arange(len(namesarray))[n+1:]:
		this_overlap = namesarray[n][1] + "-" + namesarray[m][1]
		overlap_names.append(this_overlap)
		# print(this_overlap)
		globals()[this_overlap] = []
		for elem in globals()[namesarray[n][1]]:
			# print(n, m, elem)
			if elem in globals()[namesarray[m][1]]:
				try:
					globals()[this_overlap].append(elem)
					# index_of_match = globals()[str(namesarray[m][1])].index(elem)
					# print("True", index_of_match, globals()[str(namesarray[m][1])][index_of_match])
				except: pass
			else: pass
		# print(this_overlap, len(globals()[this_overlap]), len(globals()[namesarray[n][1]]), len(globals()[namesarray[m][1]]))



driver = webdriver.Chrome("C:\chromedriver")
driver.get('https://calscape.org/')
for overlap in overlap_names:
	good_options = []
	for plant_name in globals()[overlap]:
		search_box = driver.find_element_by_name('sp')
		search_box.clear()
		search_box.send_keys(plant_name) #(Keys.chord(Keys.CONTROL, "a"), plant_name))
		driver.find_element_by_xpath('//*[@id="form_search"]/a').click()

		soup = BeautifulSoup(driver.page_source, "html.parser")

		annoying_options = soup.select("div.option.selected")
		if len(annoying_options) == 3:
			water_req = annoying_options[1].get_text(strip=True)
		else: 
			water_req = ""
			for elem in annoying_options:
				if elem.get_text(strip=True) in ["Extremely Low", "Very Low", "Low", "Moderate - High"]:
					water_req = elem.get_text(strip=True)
				else: pass

		if (water_req != "" and water_req in ["Very Low", "Extremely Low"]):
		 	good_options.append(plant_name)
		else: pass
	globals()[overlap] = good_options
	print(overlap, good_options)


# page_content > div.page_column_left > div.species_view > div.content > div.plant_info > fieldset:nth-child(4) > div:nth-child(3) > div > div.field_options_container > div.option.selected
# soup = BeautifulSoup(driver.page_source, "html.parser")
# for n in np.arange(len(soup.find_all("a", class_="blueLink"))):
# 			names.append(soup.find_all("a", class_="blueLink")[n].get_text())
# while True:
# 	try:
# 		driver.find_element_by_name('next').click()
# 		soup = BeautifulSoup(driver.page_source, "html.parser")
# 		for n in np.arange(len(soup.find_all("a", class_="blueLink"))):
# 			names.append(soup.find_all("a", class_="blueLink")[n].get_text())
# 		print(len(names))
# 	except:
# 		break

# for n in np.arange(len(names)): 
# 	ws.cell(column=1, row=n+1, value=names[n])
# 	print(n)
# wb.save("plants2.xlsx")
