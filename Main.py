# -----------------------------------------------1. Importing Libraries------------------------------------------------
import requests as request
from bs4 import BeautifulSoup
import re
import streamlit as st
import time
from PyPDF2 import PdfReader 
import webbrowser
import urllib.parse
import google.generativeai as genai
import os
# -----------------------------------------------2.Requesting and Getting response from database------------------------------------------------

page=request.get("https://github.com/SimplifyJobs/New-Grad-Positions")
soup=BeautifulSoup(page.text,"html.parser")
# -----------------------------------------------3. List of all Jobs-Data -Realtime------------------------------------------------
jobtypetype=type(soup.find('a'))

CompanyLinkList=[]
jobTypeList=[]
JobLocationList=[]
JobLinkList=[]
JobPostedList=[]
JobDataList=[CompanyLinkList,jobTypeList,JobLocationList,JobLinkList,JobPostedList]

tables =soup.find_all('table',class_=None)
for table in tables:
    tableRows=table.find_all('tr')
    for tableRow in tableRows:
        rowDataList=tableRow.find_all('td')
        if(rowDataList==[]):
            continue
        i=0
        if(type(tableRow.find('td').find('a')) == jobtypetype):
            for tableData in rowDataList:
                JobDataList[i].append(tableData)
                i+=1

# --------------------------------------------------------4.Getting JobType Input from User----------------------------------------------------------
#---------------------------------------------------------------------------------STREAMLIT
st.sidebar.title("Automated Job finder")
UserJobInput=st.sidebar.text_input("Enter the Job You are looking For :")
if UserJobInput:
    with st.spinner("Loading..."):
        time.sleep(5)
#------------------------------------------------------------------------------        

job_indexes = []
if UserJobInput:
    for index,UserjobType in enumerate(jobTypeList):
        if UserJobInput.lower() in UserjobType.text.lower():
            job_indexes.append(index)
            

if job_indexes:
    for job_index in job_indexes:
        CompanyLink=CompanyLinkList[job_index].find('a')['href']
        JobLocation=JobLocationList[job_index].text
        jobType=jobTypeList[job_index].text



        for index,JobLinks in enumerate(JobLinkList[index].find_all('a')):
            if(index==0):
                ApplicationLink=JobLinks['href']
                # st.write(f'{JobLinks.find("img")["alt"]} : {ApplicationLink}\n')
            else:
                SimplifyLink=JobLinks['href']
                # st.write(f'{JobLinks.find("img")["alt"]} : {SimplifyLink}\n')

        JobPosted=JobPostedList[index].text
        # st.write(f'Job Posted : {JobPostedList[index].text} \n\n')

#---------------------------------------------------------------------------------STREAMLIT
        c=st.container(border=True)
        c.code(f'Job Type : {jobType}')
        c.code(f'Job Location : {JobLocation}')
        c.code(f'Job Posted : {JobPosted}')
        if c.button("Company Website",type='secondary',key=f"company_{job_index}"):
            webbrowser.open(CompanyLink)

        if c.button("Direct Apply", key=f"apply_{job_index}"):
            webbrowser.open(ApplicationLink)

#More Info(Button) of any job on which the user clicks can send the index value for JobDataList(Every List Inside) and then the Simplify data can be retrieved-----
#For now we are taking 'moreInfoIndex'
# ------------------------------------------5.Retrieving Selected Job Information from simplify to display----------------------------------------------------------

# -----------------------------------------------2.Requesting and Getting response from simplify----------------------------------------------------------------

        expander = c.expander("MORE INFO")
        moreInfoIndex=job_index
            
        JobLinkListList=JobLinkList[moreInfoIndex].contents

        if(len(JobLinkListList)==1):
            moreInfoLink=JobLinkListList[0]['href']
        else:
            moreInfoLink=JobLinkListList[2]['href']
        Response=request.get(moreInfoLink)
        moreInfo=BeautifulSoup(Response.text,"html.parser")

        ##---------------------------------------------Extracting Data from Simplify of moreInfoLink---------------------------------------------------------------
        #------------------------------------------Extracting Company Details-----------------------------------------------------
        companyName=moreInfo.find('p',class_="text-left text-lg font-bold text-secondary-400")
        if(type(companyName)!=type(None)):
            companyName=companyName.text
        else:
            companyName=""

        
        if(type(moreInfo.find('p',class_="text-left text-sm"))!=type(None)):
            companyWork=moreInfo.find('p',class_="text-left text-sm").text


        companyTagsList=moreInfo.findAll('div',class_="mb-1 flex flex-wrap gap-2 text-xs")

        moreInfoLinkList1=moreInfo.findAll('a',class_="flex items-center space-x-2 rounded-2xl border border-solid border-stone-200 px-2 py-1 text-stone-600 hover:border-stone-600 hover:text-stone-800")

        #Extracting Contact links of Company
        i=True
        crunchbaseLink=None
        for moreInfoLink1 in moreInfoLinkList1:
            if(i):
                CompanywebsiteLink=moreInfoLink1['href']#WebsiteLink
                i = not i
            else:
                crunchbaseLink=moreInfoLink1['href']#CrunchbaseLink#Both have same class in a tag  


        moreInfoLinkList2=moreInfo.findAll('a',class_="flex items-center space-x-2 rounded-2xl border border-solid border-stone-200 p-2 text-stone-600 hover:border-stone-600 hover:text-stone-800")
        i=not i
        for moreInfoLink2 in moreInfoLinkList2:
            if(i):
                twitterLink=moreInfoLink2['href']#TwitterLink
                i= not i
            else:
                linkedInLink=moreInfoLink2['href']#LinkedInLink##Both have same class in a tag

        companyOverview=moreInfo.find('p',class_="mt-4 text-left text-sm")

        companyDetails=moreInfo.findAll('p',class_="text-center text-base font-bold")

        i=0
        for companyDetail in companyDetails:
            if(i==0):
                CompanyStage=companyDetail
                i+=1
            if(i==1):
                TotalFunding=companyDetail
                i+=1
            if(i==2):
                Headquarters=companyDetail
                i+=1
            if(i==3):
                Founded=companyDetail
                i+=1
        CompanyGrowths=moreInfo.find_all('span',class_="text-xl font-bold")
        i=0
        for companyGrowth in CompanyGrowths:
            if(i==0):
                SixMonthGrowthList=[companyGrowth.text,companyGrowth.span.text]
                i+=1
            if(i==1):
                OneYearGrowthList=[companyGrowth.text,companyGrowth.span.text]
                i+=1
            if(i==2):
                TwoYearGrowthList=[companyGrowth.text,companyGrowth.span.text]
                i+=1

        CompanyBenifits=moreInfo.find('div',class_="mt-4 flex flex-col gap-4")

        if(type(CompanyBenifits)!=type(None)):
            CompanyBenifits=CompanyBenifits.findAll('p')
            CompanyBenifitsList=[]#List of Company Benifits
            for CompanyBenifit in CompanyBenifits:
                CompanyBenifitsList.append(CompanyBenifit.text)

            CompanyBenifits=""
            for CompanyBenifit in CompanyBenifitsList:
                CompanyBenifits=CompanyBenifit+","
        else:
            CompanyBenifits=""

        #------------------------------------------Extracting Job Details-------------------------------------------
        JobExperienceLevel=moreInfo.find('p',class_="text-sm font-bold text-secondary-400")
        if(JobExperienceLevel is not None):
            JobExperienceLevel=JobExperienceLevel.text

        JobWorkType=moreInfo.find('p',class_="rounded-full bg-primary-50 px-4 py-2 text-sm text-primary-400")#E.g. - Full Time
        if(JobWorkType is not None):
            JobWorkType=JobWorkType.text


        JobStatus=moreInfo.find('div',class_="rounded bg-red-100 px-2 text-sm font-semibold text-red-600")#E.g. - INACTIVE
        if(type(JobStatus)!=type(None)):
            JobStatus=JobStatus.text

        # JobRequiredSkillsTagList=moreInfo.find('div',class_="mb-3 ml-6 flex flex-wrap justify-start gap-3 text-sm").nextSibling
        # if(type(JobRequiredSkillsTagList)!=type(None)):
        #     JobRequiredSkillsTagList=moreInfo.find('div',class_="mb-3 ml-6 flex flex-wrap justify-start gap-3 text-sm").contents
        #     JobRequiredSkillsList=[]#List of Job Required Skills
        #     for JobRequiredSkillsTag in JobRequiredSkillsTagList:
        #         JobRequiredSkillsList.append(JobRequiredSkillsTag.text)

            JobRequiredSkills=""
            for JobRequiredSkill in JobRequiredSkillsList:
                JobRequiredSkills=JobRequiredSkill+","
        else:
            JobRequiredSkills="NO DATA"


        JobRequirementsTag=moreInfo.find('div',string=re.compile("Requirements")).nextSibling
        JobRequirementsTag=JobRequirementsTag.find('ul').contents
        JobRequirementsList=[]#List of Job Requirements, It may have '\xa0' which is a non breaking space character in unicode so care for it in streamlit
        for JobRequirement in JobRequirementsTag:
            JobRequirementsList.append(JobRequirement.text)

        JobRequirements=""
        for JobRequirement in JobRequirementsList:
            JobRequirements=JobRequirement+","


        JobResponsibilitiesTag=moreInfo.find('div',string=re.compile("Responsibilities"))
        JobResponsibilitiesList=[]
        if (type(JobResponsibilitiesTag)!=type(None)):
            JobResponsibilitiesTag=JobResponsibilitiesTag.nextSibling
            JobResponsibilitiesTag=JobResponsibilitiesTag.find('ul').contents
            #List of Job Responsibilities.It may have '\xa0' which is a non breaking space character in unicode so care for it in streamlit
            for JobResponsibilities in JobResponsibilitiesTag:
                JobResponsibilitiesList.append(JobResponsibilities.text)

            JobResponsibilities=""
            for JobResponsibility in JobResponsibilitiesList:
                JobResponsibilities=JobResponsibility+","
        else:
            JobResponsibilities=""

        JobDescriptionQualificationTag=moreInfo.find('div',class_="description")
        JobDescriptions=JobDescriptionQualificationTag.findAll('p')
        JobDescriptionsList=[]#It may have '\xa0' which is a non breaking space character in unicode so care for it in streamlit
        for JobDescription in JobDescriptions:
            JobDescriptionsList.append(JobDescription.text)

        JobDescriptions=""
        for JobDescription in JobDescriptionsList:
            JobDescriptions=JobDescription+","


        JobQualifications=JobDescriptionQualificationTag.findAll('ul')
        JobQualificationsList=[]#It may have '\xa0' which is a non breaking space character in unicode so care for it in streamlit
        for JobDescription in JobQualifications:
            JobQualificationsList.append(JobDescription.text)

        JobQualifications=""
        for JobQualification in JobQualificationsList:
            JobQualifications=JobQualification+","


#----------------------------------STREAMLIT--------------------------------------------------------------
        expander.markdown(f'<div style ="border:1px solid red  ; border-radius:10px; display:inline-block; padding:10px">{JobWorkType}</div>',unsafe_allow_html=True)
        expander.write(f'Posted on {JobPosted}')
        expander.subheader(jobType)
        expander.divider()
        expander.write(f'COMPANY: **{companyName}**')
        if companyOverview is not None:
            expander.write(companyOverview.text)
        expander.divider()
        expander.write(f'**{JobExperienceLevel}** Level')
        expander.write(f'**{JobLocation}**')
        expander.divider()
        # expander.write("**Required Skills**")
        # expander.write(JobRequiredSkills)
        # expander.divider()
        if(type(JobRequirementsList)!=type(None)):
            expander.write("**Requirements**")
            for JobRequirement in JobRequirementsList:
                expander.write(f'-{JobRequirement}')
        expander.divider()
        if(type(JobResponsibilitiesList)!=type(None)):
            expander.write("**Responsibilities**")
            for JobResponsibility in JobResponsibilitiesList:
                expander.write(f'-{JobResponsibility}')

        #-------------------------------------------------------------------Extracting from Crunchbase link-----------------------------------------------------------------------------

        agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36','Referer':moreInfoLink}
        if crunchbaseLink is not None:
            crunchbaseResponse=request.get(crunchbaseLink,headers=agent)
            crunchbaseHtml=crunchbaseResponse.text
            crunchbasesoup=BeautifulSoup(crunchbaseHtml,"html.parser")

        # ------------------------------------------------------------------------

            with open('crunchbaseContact.html','w',encoding="utf-8") as cbt:
                cbt.write(crunchbaseHtml)

            with open('crunchbaseContact.html','r',encoding="utf-8") as cbhr:
                cb=cbhr.read()

            csoup=BeautifulSoup(cb,'html.parser')
            # ------------------------------------------------------------------------
            JobContactEmail=crunchbasesoup.find('span',string="Contact Email")
            if(type(JobContactEmail)!=type(None)):
                JobContactEmail=JobContactEmail.parent.parent.nextSibling.find('span').text

            JobContactPhone=crunchbasesoup.find('span',string="Phone Number")
            if(type(JobContactPhone)!=type(None)):
                JobContactPhone=JobContactPhone.parent.parent.nextSibling.find('span').text

#----------------------------------------------------------------------------------------STREAMLIT
        companyName_=companyName.replace(" ","")
        var= f"info@{companyName_}.com"
        expander.divider()
        expander.write("Contact Info")
        expander.write(var)
        flag=None
        if(type(var)!=type(None)):
                uploaded_file = st.file_uploader("Upload a PDF file",key=f'upload{job_index}')
                if uploaded_file is not None:
                        try:
                                reader = PdfReader(uploaded_file)
                                if len(reader.pages) > 0:
                                        page = reader.pages[0] 
                                        ResumeInfo = page.extract_text()
                                        flag="Done"
                                else:
                                        st.warning("PDF file does not contain enough pages.")
                        except Exception as e:
                                st.error(f"An error occurred: {e}")
                        if flag is not None:
                                GOOGLE_API_KEY=st.secrets.GeminiAPI.key
                                genai.configure(api_key=GOOGLE_API_KEY)

                                model=genai.GenerativeModel('gemini-pro')

                                response=model.generate_content(f'Generate a Professional E-mail body for tech job of {companyName},{jobType} acccording {ResumeInfo}, the resume should be accurate with no blanks to fill in 500 charcters only')

                                encoded_response = urllib.parse.quote(response.text)

                    
                                # mailto_link = f'<div style="border: 2px solid red; border-radius: 10px; padding: 10px; display: inline-block;"><a href="mailto:{var}?subject={var}&body={encoded_response}" target="_top" style="text-decoration: none; color: grey;">Send Personalised Mail</a></div>'
                                mailto_link=f'<div style="border: 2px solid red; border-radius: 10px; padding: 10px; display: inline-block;"><a href="https://mail.google.com/mail/?view=cm&fs=1&to={var}&su=Job%20Application&body={encoded_response}">Send Personalised Mail</a></div>'
                                st.markdown(mailto_link, unsafe_allow_html=True)
        #--------------------------------------------------------------Gemini AI-------------------------------------------------

