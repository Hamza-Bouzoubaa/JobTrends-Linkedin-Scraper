import streamlit as st
import plotly.express as px  
import pandas as pd
from DashboardFunctions import find_number_jobs_per_city,find_latest_jobs_cities
import os
import plotly.graph_objects as go


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
selected_city = st.sidebar.selectbox("Select a city", CityList)
# Add a sidebar list with report names
# Get report names from folders available in JobData/
report_path = 'JobData/'
report_names = [folder for folder in os.listdir(report_path) if os.path.isdir(os.path.join(report_path, folder))]



st.sidebar.markdown("---")
st.sidebar.markdown("### Available Reports")
selected_report = st.sidebar.selectbox("", report_names, index=report_names.index("Software engineer") if "Software engineer" in report_names else 0)
st.sidebar.markdown("---")

st.sidebar.markdown("### Contact")
st.sidebar.markdown("**Email:** [hamza.bouzoubaa@hotmail.com](mailto:hamza.bouzoubaa@hotmail.com)")



st.markdown("<h1 style='text-align: center;'><em>Linkedin Job</em>  <span style='color: blue;'><em>Trends</em></span></h1>", unsafe_allow_html=True)
st.markdown(f"<h2 style='text-align: center;'>Query: {selected_report}</h2>", unsafe_allow_html=True)





col1,col2 = st.columns([3,0.9])




with col1:
    col11,col12 = st.columns([1,2])
    with col11:
        JobDate = st.selectbox('Posting date', options=['Last 24h', 'Last Week', 'Last Month', 'Total'], index=3)
    df = find_number_jobs_per_city(JobSearch=selected_report, city=selected_city, JobDate=JobDate)
    fig = px.line(df, x='Date',
                    y='Total_Jobs',
                    title=f'Jobs Over Time in {selected_city} ({JobDate})',
                    labels={'Date':'Date', 'Total_Jobs':'Total Jobs'},
                    line_shape='spline',
                    hover_data={'Date': '|%B %d, %Y'})
    fig.update_traces(
        hovertemplate='<b>Date: %{x}</b><br><b>Total Jobs: %{y}</b><extra></extra>',
        textfont_size=20  # Increase the font size
    )
    
    fig.update_xaxes(tickformat='%Y-%m-%d')
    fig.update_layout(  
        height=500,  
        title_x=0.5, # centers the title  
      
        font=dict( # changes the font  
            size=25,  
        )  
    )  
    
    fig.update_traces(  
        mode = 'lines+markers', # adds markers to the line plot,
        
        line=dict(width=3) , # increases the line width  
        marker=dict()
    )  
    
    fig.update_xaxes(  
        tickangle=-25,  # rotates the x-axis labels for better visibility  
        title_standoff=25 # provides more space between the axis title and the tick labels  
    ) 


    st.plotly_chart(fig)

df = find_latest_jobs_cities(JobSearch=selected_report,JobDate=JobDate)
# Split your DataFrame into two  
df1 = df.iloc[:2]  
df2 = df.iloc[2:4]  
df3 = df.iloc[4:6]
with col2:
    st.markdown('#')

    col21,col22,col23,col24 = st.columns([0.5,1,1,1])
    # Iterate over first half of DataFrame and write to first column  
    with col22:
        st.markdown('#')
        for index, row in df1.iterrows():  
            st.metric(label=row['City'], value=row['Total_Jobs'], delta=row['delta'])   
        

    # Iterate over second half of DataFrame and write to second column 
    with col23: 
        st.markdown('#')
        for index, row in df2.iterrows():  
            st.metric(label=row['City'], value=row['Total_Jobs'], delta=row['delta'])   

    with col24 :
        st.markdown('#')
        for index, row in df3.iterrows():  
            st.metric(label=row['City'], value=row['Total_Jobs'], delta=row['delta'])   









col1, col2 = st.columns(2)
# Add a city selector




with col1:
    st.subheader(f" Required Seniority Level in {selected_city}")
    df = pd.read_csv(f'JobData/{selected_report}/{selected_report} in {selected_city}.csv')
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