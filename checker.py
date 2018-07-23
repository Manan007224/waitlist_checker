from selenium import webdriver
import time
import json
import os
from sys import argv
import numpy
import pandas

class course:
	def __init__(self, name, section, desciption, status, waiting):
		self.name = name
		self.section = section
		self.desciption = desciption
		self.status = status
		self.waiting = waiting

	def to_dict(self):
		return {
			'number': self.name,
			'section': self.section,
			'name': self.desciption,
			'status': self.status,
			'waiting': self.waiting
		}

def get_data(rows):
	i=4
	Courses = []
	while i<60:
		courseNumber = rows[i].text
		tds = rows[i+2].find_elements_by_tag_name('td')
		courseSection = tds[4].text
		courseName = tds[6].text
		courseStatus = tds[11].text
		courseWaiting = tds[12].text if courseStatus == 'Waiting' else 'N/A'
		crs = course(courseNumber, courseSection, courseName, courseStatus, courseWaiting)
		Courses.append(crs)
		i=i+21
	
	courses_df = pandas.DataFrame.from_records([crs.to_dict() for crs in Courses])
	return courses_df



driver = webdriver.Chrome()
driver.get("https://sims.sfu.ca/psp/csprd/?cmd=login")
username = os.environ['username']
password = os.environ['password']
email = driver.find_element_by_xpath("//*[@id='user']")
email.send_keys(username)
pw = driver.find_element_by_xpath("//*[@id='pwd']")
pw.send_keys(password)
driver.find_element_by_xpath("//*[@id='login']/div/div/div[8]/input").click()
time.sleep(3)
driver.find_element_by_xpath("//*[@id='DERIVED_SSS_SCL_SS_WEEKLY_SCHEDULE']").click()
time.sleep(3)
iframe = driver.find_element_by_xpath("//*[@id='ptifrmtgtframe']")
driver.switch_to.frame(iframe)
time.sleep(3)
en_link = driver.find_element_by_xpath("//*[@id='win1divDERIVED_SSTSNAV_SSTS_NAV_SUBTABS']/div/table/tbody/tr[2]/td[2]/a")
en_link.click()
time.sleep(3)
driver.find_element_by_xpath("//*[@id='SSR_DUMMY_RECV1$sels$1$$0']").click()
driver.find_element_by_xpath("//*[@id='DERIVED_SSS_SCT_SSR_PB_GO']").click()
time.sleep(3)
courses_table = driver.find_element_by_xpath("//*[@id='$ICField35$scroll$0']")
rows = courses_table.find_elements_by_tag_name('tr')
courses_df = get_data(rows)
print(courses_df)
time.sleep(3)
driver.close()

