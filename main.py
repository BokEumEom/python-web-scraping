import time
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

from requests import get
from bs4 import BeautifulSoup
from selenium import webdriver
from extractors.wwr import extract_wwr_jobs

chromedriver = "C:/Users/bokeu/Downloads/chromedriver_win32/chromedriver.exe"

browser = webdriver.Chrome(chromedriver)

url = "https://kr.indeed.com/jobs?q=python&limit=50"
#browser.get(url)
#print(browser.page_source)

base_url = "https://kr.indeed.com/jobs?q="
search_term = "devops"

browser.get(f"{base_url}{search_term}")
html = browser.page_source
'''
if response.status_code != 200:
  print("Can't request website")
  print(response.status_code)
  print(response.text)
else:
'''
results = []
soup = BeautifulSoup(html, "html.parser")
job_list = soup.find('ul', class_='jobsearch-ResultsList')
jobs = job_list.find_all('li', recursive=False)
for job in jobs:
  zone = job.find("div", class_="mosaic-zone")
  if zone == None:
    anchor = job.select_one("h2 a")
    title = anchor['aria-label']
    link = anchor['href']
    company = job.find("span", class_="companyName")
    location = job.find("div", class_="companyLocation")
    job_data = {
      'link': f"https://kr.indeed.com{link}",
      'company': company.string,
      'location': location.string,
      'position': title
    }
    results.append(job_data)
for result in results:
  print(result, "\n//////////\n")