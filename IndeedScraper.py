import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time
import csv

URL = 'https://de.indeed.com/jobs?q&l=M%C3%BCnchen&sort=date'
# conducting a request of the stated URL above:
page = requests.get(URL)
# specifying a desired format of page using the html parser
soup = BeautifulSoup(page.text, 'html.parser')
# printing soup in a more structured tree format for easier reading
soup.prettify()


def extract_job_title_from_result(soup):
    jobs = []
    for div in soup.find_all(name='div', attrs={'class': 'row'}):
        for a in div.find_all(name='a', attrs={'data-tn-element': 'jobTitle'}):
            jobs.append(a['title'])
    return(jobs)


extract_job_title_from_result(soup)


def extract_company_from_result(soup):
    companies = []
    for div in soup.find_all(name='div', attrs={'class': 'row'}):
        company = div.find_all(name='span', attrs={'class': 'company'})
        if len(company) > 0:
            for b in company:
                companies.append(b.text.strip())
        else:
            sec_try = div.find_all(name='span', attrs={
                                   'class': 'result-link-source'})
            for span in sec_try:
                companies.append(span.text.strip())
    return(companies)


extract_company_from_result(soup)


def extract_location_from_result(soup):
    locations = []
    spans = soup.findAll('span', attrs={'class': 'location'})
    for span in spans:
        locations.append(span.text)
    return(locations)


extract_location_from_result(soup)

max_results = 100
city_set = ['M\xfcnchen']
columns = ['city', 'job_title', 'company_name', 'location']


with open('Indeed Job Data.csv', 'a') as f_output:
    csv_output = csv.writer(f_output) 

    for city in city_set:
        for start in range(0, max_results, 10):
            page = requests.get(
                'https://de.indeed.com/jobs?q&l=M%C3%BCnchen&sort=date')
        time.sleep(1)  # ensuring at least 1 second between page grabs
        soup = BeautifulSoup(page.text, 'lxml')
        csv_output.writerow(columns)
        for div in soup.find_all(name='div', attrs={'class': 'row'}):
            # creating an empty list to hold the data for each posting
            job_post = []
            # append city name
            job_post.append(city)
            # grabbing job title
            for a in div.find_all(name='a', attrs={'data-tn-element': 'jobTitle'}):
                job_post.append(a['title'])
            # grabbing company name
            company = div.find_all(name='span', attrs={'class': 'company'})
            if len(company) > 0:
                for b in company:
                    job_post.append(b.text.strip())
            else:
                sec_try = div.find_all(name='span', attrs={
                    'class': 'result-link-source'})
                for span in sec_try:
                    job_post.append(span.text)
            # grabbing location name
            c = div.findAll('span', attrs={'class': 'location'})
            for span in c:
                job_post.append(span.text)

            csv_output.writerows([job_post])
