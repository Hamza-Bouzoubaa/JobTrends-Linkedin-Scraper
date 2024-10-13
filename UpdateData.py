import pandas as pd
from LinkedinScraper import ScrapeAllJobs,ScrapeAllJobsDetails,ScrapeAllCompanies
from main import CreateCityComparaison,GetCityData
from logger import logging

logger = logging.getLogger(__name__)  
logger.info('--------------- DataUpdate.py running ---------------')

JobWatchList = ['Software Engineer' , 'Internship']

def update_total_jobs():
    for Job in JobWatchList:
        df = CreateCityComparaison(Job)
        if df is not None:
            logger.info(f"Successfully updated total jobs for {Job}")
        else:
            logger.error(f"Failed to update total jobs for {Job}")

def update_job_data():
    for Job in JobWatchList:
        GetCityData(Job)  

update_total_jobs()

logger.info('--------------- DataUpdate.py finished ---------------')




