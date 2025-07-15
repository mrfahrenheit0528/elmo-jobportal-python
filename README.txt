CCCS 105 - Information Management 1  
Final Project (Group Project)  
Group 10 - JobSync: Streamlining the Path from Unemployed to Employed  

YouTube Link:  
https://youtu.be/PdGMR-shesM  

=========================================================
-------------------------SETUP---------------------------
=========================================================

--------------------DATABASE SETUP-----------------------

Install XAMPP, then follow these steps:

Step 1:  
In XAMPP, start the MySQL module, open the shell, and change directory to database folder.

Step 2:  
Log in as root.

Step 3:  
Create a new database named CCCS105, then exit.

Step 4:  
Import the schema.sql using this command:

    mysql -u root -p new_database_name < schema.sql

(Remember to replace 'new_database_name' with your actual database name.)

Step 5:  
Import the initial_data.sql using this command:

    mysql -u root -p new_database_name < initial_data.sql

(Remember to replace 'new_database_name' with your actual database name.)



----------------ENVIRONMENT PREPARATION------------------

Ensure you have Python installed, then follow these steps:

Step 1:  
Open CMD or any terminal.

Step 2:  
Install the following dependencies:
    - pip install customtkinter pillow
    - pip install mysql-connector-python python-dotenv

Step 3:  
Finally, open the main.py file from the source_code folder.

Once the application is launched, explore its features below:


=========================================================
---------------------INITIAL DATA------------------------
=========================================================
username:	password:	
taylor		12345678	jobseeker

elmo		123456789	jobseeker

senbie		12345678	jobseeker

abscbn		123456789	employer

cspc		12345678	employer

gma		123456789	employer




=========================================================
------------------------FEATURES-------------------------
=========================================================
==Job Search (Job Seeker)==  
Features:
- Search Jobs: Filter and search for job listings by title, location, or category.
- View Job Details: Access comprehensive job descriptions including requirements, benefits, and company information.
- Apply for Jobs: Submit applications along with personalized cover letters directly through the portal.

==Application Tracking (Job Seeker)==  
Features:
- Track Application Status: Monitor the status of your job applications (e.g., Pending, Accepted, Rejected).
- Receive Notifications: Get real-time updates and messages from employers regarding your applications.
- Review Application History: Maintain a record of past applications for future reference and career planning.

==Job Posting & Management (Employer)==  
Features:
- Post New Jobs: Create and publish job listings with detailed descriptions, requirements, and company information.
- Edit Job Postings: Update or modify existing job listings as needed.
- Remove Job Postings: Easily retire obsolete or filled job listings to keep the portal current.

==Applicant Review & Decision (Employer)==  
Features:
- Review Applications: Access detailed profiles of job applicants including resumes, cover letters, and contact information.
- Process Applications: Evaluate candidate suitability by updating application statuses (e.g., Accepted, Rejected) and adding personalized messages.
- Communicate with Candidates: Use the integrated messaging system to schedule interviews or provide feedback.

==Reporting & Analytics (Employer)==  
Features:
- Dashboard Reports: View key recruitment metrics such as the number of applicants per job, overall application trends, and hiring timelines.
- Export Data: Generate and export recruitment reports for further analysis and strategic planning.
