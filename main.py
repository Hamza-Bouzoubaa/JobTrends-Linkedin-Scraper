import pandas as pd
import datetime
import os
from GetJobList import get_total_jobs
from LinkedinScraper import ScrapeAllJobs,ScrapeAllJobsDetails,ScrapeAllCompanies
CityList = [

    "Ottawa",
    "Toronto",
    "Montreal",
    "Vancouver",
    "Calgary",
    "Edmonton"

]

def CreateCityComparaison(Job,CityList = CityList):
    # Create the directory if it doesn't exist
    job_data_dir = f"JobData/{Job}/TotalJobs"
    os.makedirs(job_data_dir, exist_ok=True)

    df = pd.DataFrame()
    TotalJobs = []
    
    for city in CityList:
        print("City: ", city)   
        Result  = get_total_jobs(Job,city)
        if Result == [None,None,None,None]:
            print("Failed to get total jobs")
            return None
        TotalJobs.append(Result)

    print(TotalJobs)
    df["City"] = CityList
    df["24h_Jobs"] = [x[3] for x in TotalJobs]
    df["Week_Jobs"] = [x[2] for x in TotalJobs]
    df["Month_Jobs"] = [x[1] for x in TotalJobs]
    df["Total_Jobs"] = [x[0] for x in TotalJobs]

    df["Week"] = datetime.datetime.now().isocalendar()[1]
    df["Month"] = datetime.datetime.now().month
    df["Year"] = datetime.datetime.now().year

    df.to_csv(f"JobData/{Job}/TotalJobs/{Job}_{datetime.datetime.now().isocalendar()[1]}_{datetime.datetime.now().month}_{datetime.datetime.now().year}_TotalJobs.csv",index=False)
    return df    

def GetCityData(Job,CityList = CityList):
    for city in CityList:
        print("City: ", city)
        Result,Path  = ScrapeAllJobs(Job,city,Limit=100)
        Result,Path = ScrapeAllJobsDetails(Path)
        Result,Path = ScrapeAllCompanies(Path)

        print('Successfully scraped data for ', city)




    
    
## example usage
CreateCityComparaison("Software engineer")
GetCityData("Software engineer")