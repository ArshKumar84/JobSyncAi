# JobSync AI

JobSync AI automates your job application process by scraping job listings, analyzing your resume, and generating personalized emails tailored to each job's requirements using AI.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Future Advancements](#future-advancements)
- [Contributing](#contributing)
- [License](#license)

## Introduction

Writing personalized emails that sync with your resume and job requirements every time you apply for a job can be hectic and time-consuming. With JobSync AI, you no longer need to write emails each time you apply for a job.

**JobSync AI** is a complete solution for job applications. It allows users to search for jobs over various databases and leverages the power of AI to send personalized emails that sync with particular job requirements and your resume.

## Features

1. **Job Scraping**: Automatically scrapes job details and application forms from different websites, providing multiple job listings for a particular role along with application facilities.
2. **PDF Reader**: Reads the uploaded resume using Python libraries to provide as input to the AI model for generating personalized emails.
3. **AI Email Generation**: Utilizes AI model APIs to generate personalized emails that sync with your resume and specific job requirements.

## Technologies Used

- **Backend**: Python
  - Libraries: `requests`, `BeautifulSoup`, `re`, `time`, `PyPDF2`, `urllib`, `os`
- **Frontend**: Streamlit
- **AI**: Google Generative AI (Gemini API)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/Arsh164/JobSync-AI.git
   cd JobSync-AI
   ```

2. **Install Required Libraries**

   ```bash
   pip install requests beautifulsoup4 streamlit pypdf2 google-generative-ai
   ```

3. **Set Up API Key**

   - Replace `GOOGLE_API_KEY` with your Google API key in the code.

## Usage

1. **Run the Streamlit Application**

   ```bash
   streamlit run main.py
   ```

2. **Interact with the Application**

   - Enter the job you are looking for in the sidebar.
   - Upload your resume (PDF format).
   - View the job listings and click on "More Info" to get detailed job information.
   - Generate and send personalized emails directly from the application.

## Future Advancements

1. **Job Publish Facility**: Create your own database of jobs and contact details.
2. **Enhanced AI Training**: Train the AI model for faster and more personalized email generation.
3. **Automated Email Sending**: Utilize SMTP protocols for automatic email sending in the background.
4. **User Database Maintenance**: Maintain a user database for job applications.

## Contributing

We welcome contributions! Please read our [contributing guidelines](CONTRIBUTING.md) for more details.


---

Feel free to further customize this README as per your specific requirements and repository structure.
