import requests as request
from bs4 import BeautifulSoup
import re
import streamlit as st
import time
from PyPDF2 import PdfReader 
import webbrowser
import urllib.parse
import google.generativeai as genai

# Function to fetch job data from the specified URL
def fetch_job_data(url):
    try:
        page = request.get(url)
        page.raise_for_status()  # Raise an error for bad responses
        soup = BeautifulSoup(page.text, "html.parser")
        return soup
    except request.exceptions.HTTPError as err:
        st.error(f"HTTP error occurred: {err}")
    except Exception as err:
        st.error(f"An error occurred: {err}")

# Function to parse job data from the soup object
def parse_job_data(soup):
    job_data = {
        "CompanyLinkList": [],
        "jobTypeList": [],
        "JobLocationList": [],
        "JobLinkList": [],
        "JobPostedList": []
    }

    tables = soup.find_all('table', class_=None)
    for table in tables:
        tableRows = table.find_all('tr')
        for tableRow in tableRows:
            rowDataList = tableRow.find_all('td')
            if not rowDataList:
                continue
            if isinstance(tableRow.find('td').find('a'), type(soup.find('a'))):
                for i, tableData in enumerate(rowDataList):
                    job_data[list(job_data.keys())[i]].append(tableData)
    return job_data

# Function to display job search results
def display_job_results(job_data, user_job_input):
    job_indexes = [index for index, jobType in enumerate(job_data['jobTypeList']) 
                   if user_job_input.lower() in jobType.text.lower()]

    if job_indexes:
        for job_index in job_indexes:
            display_single_job(job_data, job_index)

# Function to display a single job's information
def display_single_job(job_data, job_index):
    company_link = job_data['CompanyLinkList'][job_index].find('a')['href']
    job_location = job_data['JobLocationList'][job_index].text
    job_type = job_data['jobTypeList'][job_index].text
    job_posted = job_data['JobPostedList'][job_index].text

    # Create a container for the job information
    c = st.container()
    c.code(f'Job Type: {job_type}')
    c.code(f'Job Location: {job_location}')
    c.code(f'Job Posted: {job_posted}')

    if c.button("Company Website", type='secondary', key=f"company_{job_index}"):
        webbrowser.open(company_link)

    # More info expander
    expander = c.expander("MORE INFO")
    more_info_link = get_more_info_link(job_data['JobLinkList'][job_index])
    more_info = fetch_job_data(more_info_link)

    # Extract and display more information
    extract_and_display_more_info(expander, more_info, job_data, job_index)

# Function to get the more info link
def get_more_info_link(job_links):
    job_links_list = job_links.contents
    return job_links_list[0]['href'] if len(job_links_list) == 1 else job_links_list[2]['href']

# Function to extract and display more information about the job
def extract_and_display_more_info(expander, more_info, job_data, job_index):
    # Extract company details
    company_name = more_info.find('p', class_="text-left text -lg font-bold text-secondary-400")
    company_name = company_name.text if company_name else ""

    # Display company name
    expander.write(f'COMPANY: **{company_name}**')

    # Extract and display job details
    job_experience_level = more_info.find('p', class_="text-sm font-bold text-secondary-400")
    job_experience_level = job_experience_level.text if job_experience_level else "N/A"
    expander.write(f'**{job_experience_level}** Level')

    job_work_type = more_info.find('p', class_="rounded-full bg-primary-50 px-4 py-2 text-sm text-primary-400")
    job_work_type = job_work_type.text if job_work_type else "N/A"
    expander.write(f'Work Type: **{job_work_type}**')

    job_location = job_data['JobLocationList'][job_index].text
    expander.write(f'Location: **{job_location}**')

    job_requirements = more_info.find('div', string=re.compile("Requirements"))
    if job_requirements:
        requirements_list = job_requirements.nextSibling.find('ul').find_all('li')
        expander.write("**Requirements**")
        for req in requirements_list:
            expander.write(f'- {req.text}')

    job_responsibilities = more_info.find('div', string=re.compile("Responsibilities"))
    if job_responsibilities:
        responsibilities_list = job_responsibilities.nextSibling.find('ul').find_all('li')
        expander.write("**Responsibilities**")
        for resp in responsibilities_list:
            expander.write(f'- {resp.text}')

# Main function to run the Streamlit app
def main():
    st.title("Automated Job Finder")
    user_job_input = st.text_input("Enter the job you are looking for:")

    if user_job_input:
        with st.spinner("Loading..."):
            time.sleep(5)
        st.success(f"Search results for: {user_job_input}")

        # Fetch and parse job data
        url = "https://github.com/SimplifyJobs/New-Grad-Positions"
        soup = fetch_job_data(url)
        if soup:
            job_data = parse_job_data(soup)

            # Display job results
            display_job_results(job_data, user_job_input)

if __name__ == "__main__":
    main()
