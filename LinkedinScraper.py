from JobPosting import JobPosting
import pandas as pd
from fake_useragent import UserAgent
from GetJobList import get_job_list, get_total_jobs
from GetJobDetails import get_job_details
from GetCompanyDetails import get_company_details


def ScrapeAllJobs(JobTitle,Location,Limit=1000):
    df = pd.DataFrame(columns=['Title', 'Company', 'Location', 'Date Posted', 'Link'])
    TotalJobs = get_total_jobs(JobTitle,Location)
    if TotalJobs[0] is None:
        return None
    TotalJobs = min(TotalJobs[0],Limit)


    Jobsdf = get_job_list(JobTitle,Location,0)

    if Jobsdf.empty:
        return None

    print(TotalJobs)  
    for i in range(60, min(TotalJobs, 1010), 10):
        print(len(Jobsdf),i+10)
        jobs = get_job_list(JobTitle,Location,Position=i)
        if jobs['title'].isnull().all():
            continue
        Jobsdf = pd.concat([Jobsdf,jobs])
        
    Jobsdf.to_csv(f"JobData/{JobTitle}/{JobTitle} in {Location}.csv",index=False)
    return Jobsdf, f"JobData/{JobTitle}/{JobTitle} in {Location}.csv"

 

def ScrapeAllJobsDetails(dfPath):
    df = pd.read_csv(dfPath)
    df_with_details = pd.DataFrame()
    for i in range(len(df)):
        print(i)
        JobURL = df.iloc[i]['job_link']
        if pd.isna(JobURL):
            continue
        JobDetails = get_job_details(JobURL)
        print(JobDetails.columns)
        if JobDetails.empty:
            continue
            
        Job = JobPosting(title = df.iloc[i]['title'],company=df.iloc[i]['company'],location=df.iloc[i]['location'],date_posted=df.iloc[i]['date_posted'],job_link=df.iloc[i]['job_link'],description=JobDetails['description'][0],time_posted=JobDetails['time_posted'][0] ,seniority_level=JobDetails['seniority_level'][0],employment_type=JobDetails['employment_type'][0],job_function=JobDetails['job_function'][0],industries=JobDetails['industries'][0],applicants=JobDetails['applicants'][0],company_url=JobDetails['company_url'][0])
        df_with_details = pd.concat([df_with_details,Job.to_df()])
       
    df_with_details.to_csv(dfPath,index=False)
    return df_with_details, dfPath


def ScrapeAllCompanies(dfPath):
    df = pd.read_csv(dfPath)
    df_with_details = pd.DataFrame()
    for i in range(len(df)):
        CompanyURL = df.iloc[i]['company_url']
        if pd.isna(CompanyURL):
            continue
        CompanyDetails = get_company_details(CompanyURL)
        if CompanyDetails.empty:
            continue
        print(i)
        print(CompanyDetails.columns)
        Job = JobPosting(title = df.iloc[i]['title'],company=df.iloc[i]['company'],location=df.iloc[i]['location'],date_posted=df.iloc[i]['date_posted'],job_link=df.iloc[i]['job_link'],description=df.iloc[i]['description'],time_posted=df.iloc[i]['time_posted'] ,seniority_level=df.iloc[i]['seniority_level'],employment_type=df.iloc[i]['employment_type'],job_function=df.iloc[i]['job_function'],industries=df.iloc[i]['industries'],applicants=df.iloc[i]['applicants'],company_url=df.iloc[i]['company_url'],company_size=CompanyDetails['company_size'][0] if 'company_size' in CompanyDetails else None,founded=CompanyDetails['founded'][0] if 'founded' in CompanyDetails else None ,type=CompanyDetails['type'][0] if 'type' in CompanyDetails else None ,industry=CompanyDetails['industry'][0] if 'industry' in CompanyDetails else None ,headquarters=CompanyDetails['headquarters'][0] if 'headquarters' in CompanyDetails else None)
        df_with_details = pd.concat([df_with_details,Job.to_df()])


    df_with_details.to_csv(dfPath,index=False)
    return df_with_details, dfPath

