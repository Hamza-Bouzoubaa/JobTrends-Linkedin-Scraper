import pandas as pd
from LinkedinScraper import ScrapeAllJobs,ScrapeAllJobsDetails,ScrapeAllCompanies
from main import CreateCityComparaison,GetCityData

JobWatchList = ['Software Engineer' , 'Internship']

def update_total_jobs():
    for Job in JobWatchList:
        CreateCityComparaison(Job)

def update_job_data():
    for Job in JobWatchList:
        GetCityData(Job)  

update_total_jobs()





