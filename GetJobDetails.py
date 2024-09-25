import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re
import time

def handle_response(response,MaxTrials=5,CurrentTrial=0):
    
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

def make_request(JobURL,MaxTrials=5,CurrentTrial=0):
    payload = {}
    headers = {
    'Cookie': 'bcookie="v=2&d871c9f5-039b-4f64-85c5-dc2babc12b5d"; lang=v=2&lang=en-us; lidc="b=TGST01:s=T:r=T:a=T:p=T:g=3413:u=1:x=1:i=1725195445:t=1725281845:v=2:sig=AQE8ro7KHWSZ59NwKnOx1xnKUW-Xzroh"; JSESSIONID=ajax:6246440277120090716; bscookie="v=1&202409011301077868575c-c958-4da0-833b-39e76815efb2AQHU1aXEIsm920nFET3NHHcWxNwG9l-R"; ccookie=0001AQEpLClb0ypivQAAAZGtraD4o3LC40GB8eIXAjTd1+bZFvV//pN8zDuMBho1b24EWRUccBPsXfoAViaCjpwwC6bEUWGTbpJOmTmLVjO6ta62BZiXkHHFlnS6qHyxTwnxduY/423GjMencshxx3aL8Pi1IOnIwJI4XdiNNr4vnSzZ5sZ7IHc='
    }

    response = requests.request("GET", JobURL, headers=headers, data=payload)
    response = handle_response(response,MaxTrials=MaxTrials,CurrentTrial=CurrentTrial)
    if response == False:
        return make_request(JobURL,CurrentTrial=CurrentTrial+1,MaxTrials=MaxTrials)
    elif response == None:
        return None
    else:
        return response
    
def parse_response(response):
        
    soup = BeautifulSoup(response.text, 'html.parser')
    Job_details = soup.find_all('span', class_='description__job-criteria-text description__job-criteria-text--criteria')
    Seniority_Level = Job_details[0].get_text(strip=True) if Job_details else None
    Employment_Type = Job_details[1].get_text(strip=True) if Job_details else None
    Job_Function = Job_details[2].get_text(strip=True) if Job_details else None
    Industries = Job_details[3].get_text(strip=True) if Job_details else None

    applicants = soup.find('span', class_='num-applicants__caption topcard__flavor--metadata topcard__flavor--bullet')
    applicants = applicants.get_text(strip=True) if applicants else None

    if applicants == None:
        applicants = soup.find('figcaption', class_='num-applicants__caption')
        applicants = applicants.get_text(strip=True) if applicants else None

    meta_tag = soup.find('meta', attrs={'name': 'description'})  
    # Extract content  
    DateDescription = meta_tag['content'] if meta_tag else "No meta tag found"  
    date_match = re.match(r'Posted\s([\d:AMP\s]+)\.\s', DateDescription)
    TimePosted = date_match.group(1) if date_match else None

    div_tag = soup.find('div', class_='show-more-less-html__markup show-more-less-html__markup--clamp-after-5 relative overflow-hidden')  
    Description = div_tag.get_text(separator='\n') if div_tag else "No div tag found"  
    Description = Description.replace("\n","")
    

    location_tag = soup.find('span', class_='sub-nav-cta__meta-text')
    Location = location_tag.get_text(strip=True) if location_tag else None

    company_url_tag = soup.find('a', class_='topcard__org-name-link topcard__flavor--black-link', attrs={'data-tracking-control-name': 'public_jobs_topcard-org-name'})
    company_url = company_url_tag['href'] if company_url_tag else None

    df = pd.DataFrame() 
    df['seniority_level'] = [Seniority_Level]
    df['employment_type'] = [Employment_Type]
    df['job_function'] = [Job_Function]
    df['industries'] = [Industries]
    df['applicants'] = [applicants]
    df['description'] = [Description]
    df['time_posted'] = [TimePosted]
    df['location'] = [Location]
    df['company_url'] = [company_url]

    df = df[['location', 'seniority_level', 'employment_type', 'job_function', 'industries', 'applicants', 'description', 'time_posted', 'company_url']]

    return df

def get_job_details(JobURL,MaxTrials=5):

    response = make_request(JobURL,MaxTrials=MaxTrials)

    if response == None:
        return pd.DataFrame(columns=['Location', 'Seniority Level', 'Employment Type', 'Job Function', 'Industries', 'Applicants', 'description', 'Date Posted', 'Company URL'])
    else:
        return parse_response(response)
    


