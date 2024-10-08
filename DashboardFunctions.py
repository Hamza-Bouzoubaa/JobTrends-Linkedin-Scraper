import pandas as pd

optionsTraduction = {
        'Last 24h': '24h_Jobs',
        'Last Week': 'Week_Jobs',
        'Last Month': 'Month_Jobs',
        'Total': 'Total_Jobs'
    }

def find_number_jobs_per_city(JobSearch, city, JobDate):
    

    df = pd.read_csv(f'JobData/{JobSearch}/TotalJobs/TotalJobs.csv')
    df = df[df['City'] == city]
    df = df[['Date','City', optionsTraduction[JobDate]]]
    df.rename(columns={optionsTraduction[JobDate]: 'Total_Jobs'}, inplace=True)

    return df

def find_latest_jobs_cities(JobSearch, JobDate):
    df = pd.read_csv(f'JobData/{JobSearch}/TotalJobs/TotalJobs.csv')
    df = df[['Date','City', optionsTraduction[JobDate]]]
    df.rename(columns={optionsTraduction[JobDate]: 'Total_Jobs'}, inplace=True)
    df = df.sort_values(by='Date', ascending=False)
    df = df.groupby('City').apply(lambda x: x.sort_values(by='Date')).reset_index(drop=True)
    df['delta'] = df.groupby('City')['Total_Jobs'].diff()
    df['Total_Jobs'] = df['Total_Jobs'].fillna(0).astype(int)
    df['delta'] = df['delta'].fillna(0).astype(int)
    df = df[df['Date'] == df['Date'].max()]
    

    return df