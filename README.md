# LinkedIn Scraper and Dashboard using Streamlets and Python  
  
This project is part of a Microsoft event aimed at building a LinkedIn job posting scraper and a dashboard using Streamlets and Python.

## What the Project Does  
  
The LinkedIn Scraper and Dashboard project is designed to scrape job posting data from LinkedIn based on a specified job title and location.   
  
Once you provide a job title and location, the scraper performs a search and goes through all the associated job postings within that location. It then scrapes comprehensive data about each job, including details about the job role and the company posting the job.  
  
This data can then be used for various purposes, such as job market analysis, tracking industry trends, or even aiding in a job search. The scraped data is also displayed on an interactive dashboard, making it easy to analyze and interpret. 
  
## Prerequisites  
  
Before you begin, ensure you have met the following requirements:  
  
- You have installed the latest version of [Python](https://www.python.org/downloads/)  
  
## Installing JobTrends 
  
To install JobTrends, follow these steps:  
  
1. Clone the repository:   
```git clone https://github.com/Hamza-Bouzoubaa/JobTrends.git ```

  
## Using the Dashboard  
  
To run the Dashboard, follow these steps:  
  
1. Run the application:  
streamlit run app.py


2. To scrape new data, modify the two functions at the end of the `main.py` file according to the job posting and location you're interested in.
   ```
   ## example usage
   def main():
      JobtoSearch = "Software engineer"
      CreateCityComparaison(JobtoSearch)
      GetCityData(JobtoSearch)

   if __name__ == "__main__":
      main()
    ```
  
## Contact  
  
If you want to contact me you can reach me at `hbouz007@uottawa.ca`.  
