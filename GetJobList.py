import requests
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
from JobPosting import JobPosting
import os


def handle_response(response,MaxTrials=10,CurrentTrial=0):
    
        status = response.status_code

        if status == 200:
            print("Success")

        elif CurrentTrial < MaxTrials:
            print(f"Error: {status}")
            if status == 429:
                print("Error: Too many requests")
                time.sleep(15*CurrentTrial)
                return False
            else:
                time.sleep(5*CurrentTrial)
                return False
        else:
            print("Error: Max Trials reached")
            return None
    
        return response

def make_request(JobTitle,Location,Position=0,MaxTrials=10,CurrentTrial=0):

    JobTitle = JobTitle.replace(" ","%20") # software engineer =  software%20engineer

    if Position == 0:
        url = f"https://www.linkedin.com/jobs/search?keywords={JobTitle}&location={Location}&trk=public_jobs_jobs-search-bar_search-submit&position=0&pageNum=0"

    elif Position >0:
        url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={JobTitle}&location={Location}&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0&start={Position}"
    
    payload = {}
    headers = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.#033834',
    'dnt': '1',
    'priority': 'u=1, i',
    'referer': 'https://www.linkedin.com/jobs/search?keywords=sales%20manager&location=Canada&geoId=101174742&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Cookie': 'bcookie="v=2&d871c9f5-039b-4f64-85c5-dc2babc12b5d"; lang=v=2&lang=en-us; lidc="b=OGST04:s=O:r=O:a=O:p=O:g=3289:u=1:x=1:i=1725121975:t=1725208375:v=2:sig=AQHm6bOn3Rtbs_qNKwYPSAdIsvQewOXU"; JSESSIONID=ajax:0782009941534482235; bscookie="v=1&202408311633272f5c36f4-f013-48e6-8683-4904264d1ccaAQHsfhGP2AiO6nlZNId4qiDejY145sRF"'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    
    response = handle_response(response,MaxTrials=MaxTrials,CurrentTrial=CurrentTrial)
    if response == False:
        return make_request(JobTitle,Location,Position=Position,CurrentTrial=CurrentTrial+1,MaxTrials=MaxTrials)
    elif response == None:
        return None
    else:
        return response



def parse_jobs(response,CurrentTrial=0,MaxTrials=10):
    Job_df = pd.DataFrame()
    soup = BeautifulSoup(response.text, 'html.parser') 
    
    # Find all job postings  
    job_postings = soup.find_all('div', class_='base-search-card__info')  
    
    # Extract the data from each job posting  
    JobPostingUrls = soup.find_all('div',class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
        
    if len(job_postings) == 0:
        print("No jobs found: Retrying...")

        if CurrentTrial < MaxTrials:
            time.sleep(5*CurrentTrial)
            return parse_jobs(response,CurrentTrial=CurrentTrial+1,MaxTrials=MaxTrials)
        
        else:
            return JobPosting(title=None, company=None, location=None, date_posted=None, job_link=None).to_df()
    
    for i in range(len(job_postings)): 
        title = job_postings[i].find('h3', class_='base-search-card__title').get_text(strip=True)  
        company = job_postings[i].find('a', class_='hidden-nested-link').get_text(strip=True)  if job_postings[i].find('a', class_='hidden-nested-link') else None
        location = job_postings[i].find('span', class_='job-search-card__location').get_text(strip=True)  

        Date1 = job_postings[i].find('time', class_='job-search-card__listdate')
        Date2 = job_postings[i].find('time', class_='job-search-card__listdate--new')

        if Date1:
            date_posted = Date1.get_text(strip=True)
        elif Date2:
            date_posted = Date2.get_text(strip=True)
        else:
            date_posted = None

        try:
            job_link = JobPostingUrls[i].find('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]').get('href') if JobPostingUrls[i].find('a', class_='base-card__full-link absolute top-0 right-0 bottom-0 left-0 p-0 z-[2]') else None
        except:
            job_link = None

        
        Job = JobPosting(title=title, company=company, location=location, date_posted=date_posted, job_link=job_link)
        Job_df = pd.concat([Job_df,Job.to_df()])
    return Job_df

def parse_total_jobs(response):

    soup = BeautifulSoup(response.text, 'html.parser')  
    Total = soup.find('label', {'for': 'f_TPR-0'})  
    PastMonth = soup.find('label', {'for': 'f_TPR-1'})
    PastWeek = soup.find('label', {'for': 'f_TPR-2'})
    Past24Hours = soup.find('label', {'for': 'f_TPR-3'})

    if Total:
        TotalJobs = int(re.sub("[^0-9]", "", Total.get_text(strip=True).split(" ")[-1]))
    else:
        TotalJobs = 0

    if PastMonth:
        PMJobs = int(re.sub("[^0-9]", "", PastMonth.get_text(strip=True).split(" ")[-1]))
    else:
        PMJobs = 0

    if PastWeek:
        PWJobs = int(re.sub("[^0-9]", "", PastWeek.get_text(strip=True).split(" ")[-1]))
    else:
        PWJobs = 0

    if Past24Hours:
        PHJobs = int(re.sub("[^0-9]", "", Past24Hours.get_text(strip=True).split(" ")[-1]))
    else:
        PHJobs = 0

    print(f'all {TotalJobs} and Past Month: {PMJobs} and Past Week: {PWJobs} and Past 24 Hours: {PHJobs}')

    return [TotalJobs,PMJobs,PWJobs,PHJobs]




def get_total_jobs(JobTitle,Location,Position=0):
    
    response = make_request(JobTitle,Location,Position)
    if response == None:
        return [None,None,None,None]
    TotalJobs = parse_total_jobs(response)
    return TotalJobs

def get_job_list(JobTitle,Location,Position=0):
    
    response = make_request(JobTitle,Location,Position)

    if response == None:
        return JobPosting(title=None, company=None, location=None, date_posted=None, job_link=None).to_df()

    Job_df = parse_jobs(response)
    if Job_df.empty:
        return JobPosting(title=None, company=None, location=None, date_posted=None, job_link=None).to_df()
    else:
        return Job_df



