import jinja2
import os
from jinja2 import Template
import subprocess
import tkinter as tk
from bs4 import BeautifulSoup
import requests
import re
import pdfkit
import numpy as np


master = tk.Tk() # Initializes interpreter and creates root window
master.title('Cover Letter Generator')
master.geometry("500x380") # enter size horizontal x vertical
intro1 = tk.Label(master, text="Enter information manually",fg="blue")
intro1.grid(column=0,row=0)
intro2 = tk.Label(master, text=" or enter a valid Linkedin link",fg="blue")
intro2.grid(column=0,row=1)

# Labels for text boxes
label_1 = tk.Label(master, text="Company Name")
label_2 = tk.Label(master, text="Job Title")
label_3 = tk.Label(master, text="Job Address")
label_4 = tk.Label(master, text="Personal Address")
label_5 = tk.Label(master, text="Personal Email")
label_6 = tk.Label(master, text="Or Enter LinkedIn URL")
# Adds .grid(row=n) to every label_n
for i in np.arange(1,7):
        eval('label_' + str(i) + '.grid(row=' + str(i+1) + ')')

# This function performs linkedin job posting scrapping for company name, job title and job location
def linkedin():
    e1.delete(0, tk.END) # Clear entry after button is pressed
    e2.delete(0, tk.END) # Clear entry after button is pressed
    e3.delete(0, tk.END) # Clear entry after button is pressed
    urllink = e6.get()
    # Specify with which URL/web page we are going to be scraping
    url = requests.get(urllink).text
    #Parse the HTML from our URL into the BeautifulSoup parse tree format
    soup = BeautifulSoup(url, "lxml")
    # Retrive job description and convert it into string
    jobdescription = soup.find('title').string
    print(jobdescription)
    # Extract Company Name, Job Title, Job Location
    company_name = str(re.findall('(.+?) hiring ',jobdescription))[2:-2] # Extracts job title name from the title
    job_title = str(re.findall(' hiring (.+?) in ',jobdescription))[2:-2] # Extracts company name from the title
    job_location = str(re.findall(' in (.+?), United',jobdescription))[2:-2] # Extracts job location from the title
    e1.insert(10, company_name) # inserts company_name into the first row
    e2.insert(10, job_title)  # inserts job_title into the first row
    e3.insert(10, job_location)  # inserts job_location into the first row
    e6.delete(0, tk.END) # Clear entry after button is pressed

# This function will convert a website to a pdf file and save it on your computer
def html_to_pdf():
    #path = input("Please enter the file path ex. C:\Jim\Desktop")
    # This requires you to have wkhtmltopdf.exe in the same folder as this python code.
    path_wkhtmltopdf = r'wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    if pdfkit.from_url(e6.get(), e1.get() + ' ' + e2.get()+'.pdf'): # Check if method from_url returned True
        print("Sucessfully created pdf from url")
    else:
        print("Something went wrong")

# Text boxes
e1 = tk.Entry(master)
e1.insert(10, "Wells Fargo")
e1.grid(row=2, column=1)
e2 = tk.Entry(master)
e2.insert(10, "Data Analyst")
e2.grid(row=3, column=1)
e3 = tk.Entry(master)
e3.insert(10, "Charlotte, NC")
e3.grid(row=4, column=1)
e4 = tk.Entry(master)
e4.insert(10, "Hendersonville, NC")
e4.grid(row=5, column=1)
e5 = tk.Entry(master)
e5.insert(10, "ktsarapk@alumni.unca.edu")
e5.grid(row=6, column=1)
e6 = tk.Entry(master)
e6.insert(10, "LinkedIn URL")
e6.grid(row=7, column=1)

# Change the Jinja environment to mimic the LaTeX environment
latex_jinja_env = jinja2.Environment(
	block_start_string = '\BLOCK{',
	block_end_string = '}',
	variable_start_string = '\VAR{',
	variable_end_string = '}',
	comment_start_string = '\#{',
	comment_end_string = '}',
	line_statement_prefix = '%%',
	line_comment_prefix = '%#',
	trim_blocks = True,
	autoescape = False,
	loader = jinja2.FileSystemLoader(os.path.abspath('.'))
)
# Select which tex file you want to modify
template = latex_jinja_env.get_template('coverletter.tex')

# This function modifies the latex file, creates a new latex files, converts it to pdf and saves it locally
def generate_pdf():
    # combine template and variables
    document = template.render(CompanyName=e1.get(),
    jobTitle=e2.get(),
    JobLocation =e3.get(),
    MyAddress=e4.get(),
    Email=e5.get())
    file_name = 'CL ' +e1.get() + ' ' + e2.get()+'.tex'
    # write over the document file that we created
    with open(file_name,'w') as output:
        output.write(document)

    # create pdf file from the tex file that we created
    # make sure to specify latex type ; LaTeX, pdfTeX, XeTeX, LuaTeX,etc
    pdf = subprocess.check_call(['XeLaTeX',
    '-interaction=nonstopmode', # Use this to ignore errors
    file_name])

# Creates a button to call the function that generates the PDF from a latex file
tk.Button(master, text='Modify the LaTeX file and generate a PDF file ',command=generate_pdf).grid(row=9,
                                                                column=0,
                                                                sticky=tk.W,
                                                                pady=4)
# creates a button that calls a function for scrapping a public LinkedIn job profile for job title, location and company name
tk.Button(master, text='Autofill using LinkedIn link', command=linkedin).grid(row=10,
                                                        column=0,
                                                        sticky=tk.W,
                                                         pady=4)
# create a button that calls a function to convert a website to pdf and store it locally
tk.Button(master, text='Save LinkedIn job description as PDF', command=html_to_pdf).grid(row=11,
                                                        column=0,
                                                        sticky=tk.W,
                                                         pady=4)
# Creates a button to that calls a quit function to close the window and stop the execution of the code
tk.Button(master, text='Quit', command=master.quit).grid(row=12,
                                                        column=0,
                                                        sticky=tk.W,
                                                         pady=4)

master.mainloop()
tk.mainloop() # haults the executution of the python
