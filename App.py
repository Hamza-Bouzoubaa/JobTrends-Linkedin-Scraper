import streamlit as st
import plotly.express as px  
import pandas as pd


# Set page configuration
st.set_page_config(
    page_title="Linkedin Job Trends",
    layout="wide",
    initial_sidebar_state="expanded")

CityList = [

    "Ottawa",
    "Toronto",
    "Montreal",
    "Vancouver",
    "Calgary",
    "Edmonton"

]


st.markdown("<h1 style='text-align: center;'><em>Linkedin Job</em>  <span style='color: blue;'><em>Trends</em></span></h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center;'>Query: Software Engineer</h2>", unsafe_allow_html=True)




col1,col2,col3 = st.columns([3,0.5,0.5])


with col1:
    df = pd.read_csv("JobData/Software engineer/TotalJobs/Software engineer_39_9_2024_TotalJobs.csv")
    st.subheader("Job Distribution by City")
    fig = px.bar(df, x='City', y='Total_Jobs', title='Total Jobs in Different Cities in 38th week of September 2024', color='City')  

    st.plotly_chart(fig)


  
# Split your DataFrame into two  
df1 = df.iloc[:3]  
df2 = df.iloc[3:]  
  
# Iterate over first half of DataFrame and write to first column  
with col2:
    st.markdown('#')
    for index, row in df1.iterrows():  
        st.metric(label=row['City'], value=row['Total_Jobs'])  
    

# Iterate over second half of DataFrame and write to second column 
with col3: 
    st.markdown('#')
    for index, row in df2.iterrows():  
        st.metric(label=row['City'], value=row['Total_Jobs'])  

selected_city = st.selectbox("Select a city", CityList)


col1, col2 = st.columns(2)
# Add a city selector




with col1:
    st.subheader(f" Required Seniority Level in {selected_city}")
    df = pd.read_csv(f'JobData/Software engineer/Software Engineer in {selected_city}.csv')
    SeniorityLevel = df['seniority_level'].value_counts()
    color_discrete_map = {
        'Entry level': 'blue',
        'Mid-Senior level': 'green',
        'Director': 'red',
        'Executive': 'purple',
        'Internship': 'orange'
    }
    fig = px.pie(SeniorityLevel, values=SeniorityLevel.values, names=SeniorityLevel.index, color=SeniorityLevel.index, color_discrete_map=color_discrete_map)
    st.plotly_chart(fig)
    

# Add content to the second column
with col2:
    st.subheader(f"Type of Employment in {selected_city}") 
    EmploymentType = df['employment_type'].value_counts()
    color_discrete_map = {
        'Full-time': 'blue',
        'Part-time': 'green',
        'Contract': 'red',
        'Temporary': 'purple',
        'Volunteer': 'orange',
        'Internship': 'pink'
    }
    fig = px.pie(EmploymentType, values=EmploymentType.values, names=EmploymentType.index, color=EmploymentType.index, color_discrete_map=color_discrete_map)
    st.plotly_chart(fig)



col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Job Industries in {selected_city}")
    Industries = df['industries'].value_counts()
    percentages = Industries / Industries.sum() * 100  
  
    # combine small categories into 'Other'  
    mask = percentages < 2  
    Industries = Industries[~mask]  
    Industries['Other'] = percentages[mask].sum() 

    fig = px.pie(Industries, values=Industries.values, names=Industries.index)
    st.plotly_chart(fig)

with col2:
    st.subheader(f"Company Sizes in {selected_city}")
    CompanySize = df['company_size'].value_counts()

    # Define larger categories for company sizes
    size_mapping = {
        '1-10 employees': 'Small (less than 50)',
        '11-50 employees': 'Small (less than 50)',
        '51-200 employees': 'Medium (50-200)',
        '201-500 employees': 'Medium (50-200)',
        '501-1,000 employees': 'Large (500-5000)',
        '1,001-5,000 employees': 'Large (500-5000)',
        '5,001-10,000 employees': 'Very Large (5000+)',
        '10,001+ employees': 'Very Large (5000+)'
    }


    # Define color mapping for company sizes
    color_discrete_map = {
        'Small (less than 50)': 'lightblue',
        'Medium (50-200)': 'green',
        'Large (500-5000)': 'red',
        'Very Large (5000+)': 'purple'
    }
    

    # Map the company sizes to the larger categories
    CompanySize = CompanySize.groupby(size_mapping).sum()
    # Ensure the order is from small to large
    size_order = ['Small (less than 50)', 'Medium (50-200)', 'Large (500-5000)', 'Very Large (5000+)']  
    CompanySize.index = pd.Categorical(CompanySize.index, categories=size_order, ordered=True)  
    CompanySize = CompanySize.sort_index()  
 
    fig = px.pie(CompanySize, values=CompanySize.values, names=CompanySize.index, color=CompanySize.index, color_discrete_map=color_discrete_map)
    st.plotly_chart(fig)