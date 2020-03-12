# Job-Application-Helper

Applying for jobs can often be a tedious process, especially when it comes to writing cover letters and resumes for speicific jobs. I often find myself reluctant to apply to certain jobs or I end up wasting too much valuable time writing cover letters and resumes. Therefore, I decided to take my top written cover letter and convert it into an all-purpose cover letter. 

I then proceeded by automating the process of editing and generating a PDF from my cover letter written in LaTeX with Python, automating the insertion of a job title, the company name, location, etc. I accomplished this by scrapping LinkedIn’s public job postings to extract the respective information. Once the information is extracted, I can edit the LaTeX file and generate its PDF automatically with a single click, furthermore I added a function to save the LinkedIn’s job description as a PDF for future reference. The files are saved in the working directory, in a folder named "company name", the files themselves are saved as “company name” + “job title”.

This version of the program requires you to have wkhtmltopdf.exe, you can select the LaTeX file that you wish to modify using the GUI when running JobHelper.py. You can download wkhtmltopdf.exe by going to https://wkhtmltopdf.org/downloads.html.

Furthermore, the LaTeX file that you wish to modify requires you to have \VAR{CompanyName}, \VAR{JobTitle} and \VAR{JobLocation} where you wish for the program to make the appropriate edits with the information extracted from LinkedIn job URL that is provided by the user.   

While in the present state this program may have no practical use to anyone outside of my personal use,  I may choose to polish and expand the programs features to create a stand-alone applications that is meant to assist users in creating resumes , cover letters and more. 
