import pandas as pd


class JobPosting:

    def __init__(self, title,job_link, company=None, location=None, date_posted=None, time_posted=None,
                description=None,seniority_level=None, employment_type=None, job_function=None, industries=None, 
                applicants=None, company_url=None,company_size=None,founded=None,type=None,industry=None,headquarters=None):
        
        self.title = title
        self.company = company
        self.location = location
        self.date_posted = date_posted
        self.job_link = job_link
        self.description = description
        self.seniority_level = seniority_level
        self.employment_type = employment_type
        self.job_function = job_function
        self.industries = industries
        self.applicants = applicants
        self.company_url = company_url
        self.time_posted = time_posted
        self.company_size = company_size
        self.founded = founded
        self.type = type
        self.industry = industry
        self.headquarters = headquarters


    def __str__(self):
        return f"""
        Title: {self.title}
        Company: {self.company}
        Location: {self.location}
        Date Posted: {self.date_posted}
        Time Posted: {self.time_posted}
        Seniority Level: {self.seniority_level}
        Employment Type: {self.employment_type}
        Job Function: {self.job_function}
        Industries: {self.industries}
        Applicants: {self.applicants}
        Link: {self.job_link}
        Company URL: {self.company_url}
        Company Size: {self.company_size}
        Founded: {self.founded}
        Type: {self.type}
        Industry: {self.industry}
        Headquarters: {self.headquarters}
        Description: {self.description}

        """
    
    def to_df(self):
        return pd.DataFrame([self.__dict__])
    
    def is_empty(self):
        return self.title is None and self.company is None and self.location is None and self.date_posted is None and self.job_link is None and self.description is None and self.seniority_level is None and self.employment_type is None and self.job_function is None and self.industries is None and self.applicants is None and self.company_url is None and self.time_posted is None and self.company_size is None and self.founded is None and self.type is None and self.industry is None and self.headquarters is None
