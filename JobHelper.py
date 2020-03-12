import jinja2
import sys, os
import shutil
from jinja2 import Template
import subprocess
import tkinter as tk
from tkinter import *
from bs4 import BeautifulSoup
import requests
import re
import pdfkit
import numpy as np
from tkinter import filedialog

master = tk.Tk() # Initializes interpreter and creates root window
master.title('Cover Letter Generator')
#master.geometry("600x380") # enter size horizontal x vertical
#master.configure(background='white') #set background color

#intro1 = tk.Label(master, text="Enter information manually or enter a valid Linkedin link",fg="blue")
#intro1.grid(column=0,row=0)

# .grid positioning variables for text boxes and their respective labels
starting_row_n = 0
row_start = 0
row_end = 7
# list of typestting options, you must use the correct typesetting in order for the .tex to compile correctly
typesetting_options = [ 'LaTeX', 'pdfLaTeX', 'XeLaTeX', 'LuaLaTeX', 'ConTeXt']
typesetting_var = StringVar(master)
typesetting_var.set(typesetting_options[2]) # default value

# Labels for text boxes
label_0 = tk.Label(master, text="Select LaTeX file using the button :" ,fg='red')
label_1 = tk.Label(master, text="Enter the company name :")
label_2 = tk.Label(master, text="Enter the job title :")
label_3 = tk.Label(master, text="Enter the job address ")
label_4 = tk.Label(master, text="Enter your personal Address :")
label_5 = tk.Label(master, text="Enter your personal email :")
label_6 = tk.Label(master, text="Or just enter the LinkedIn URL :",fg='blue')
label_7 = tk.Label(master, text="Enter the correct typesetting engine", fg='red')
# Adds .grid(row=n......) to every label_n
for i in np.arange(row_start+starting_row_n,row_end+starting_row_n+1):
        eval('label_' + str(i-starting_row_n) +
        '.grid(row=' + str(i+1+starting_row_n) + ', column=0 ,sticky=(N, E, W), padx=5, pady=5'+')')

# This function performs linkedin job posting scrapping for company name, job title and job location
def linkedin():
    box_1.delete(0, tk.END) # Clear entry after button is pressed
    box_2.delete(0, tk.END) # Clear entry after button is pressed
    box_3.delete(0, tk.END) # Clear entry after button is pressed
    urllink = box_6.get()
    # Specify with which URL/web page we are going to be scraping
    url = requests.get(urllink).text
    #Parse the HTML from our URL into the BeautifulSoup parse tree format
    soup = BeautifulSoup(url, "lxml")
    # Retrive job description and convert it into string
    jobdescription = soup.find('title').string
    # Extract Company Name, Job Title, Job Location. Note: The format may change in the future, hence revision will be required.
    company_name = str(re.findall('(.+?) hiring ',jobdescription))[2:-2] # Extracts job title name from the title
    job_title = str(re.findall(' hiring (.+?) in ',jobdescription))[2:-2] # Extracts company name from the title
    job_location = str(re.findall(' in (.+?), United',jobdescription))[2:-2] # Extracts job location from the title
    box_1.insert(10, company_name) # inserts company_name into the first row
    box_2.insert(10, job_title)  # inserts job_title into the first row
    box_3.insert(10, job_location)  # inserts job_location into the first row
    # box_6.delete(0, tk.END) # Clear entry after button is pressed

# Text boxes, this is text box 1
box_0 = tk.Entry(master, text="", width=50)
box_0.insert(10, "C:/Users/Kirill/Desktop/Latex Resume/Pre-Alpha Version/Cover Letter/copy_of_tex_template.tex")
# text box 2
box_1 = tk.Entry(master, text="", width=40)
box_1.insert(10, "Wells Fargo")
# text box 3
box_2 = tk.Entry(master, text="", width=40)
box_2.insert(10, "Data Analyst")
# text box 4
box_3 = tk.Entry(master, text="", width=40)
box_3.insert(10, "Charlotte, NC")
# text box 5
box_4 = tk.Entry(master, text="", width=40)
box_4.insert(10, "Hendersonville, NC")
# text box 6
box_5 = tk.Entry(master, text="", width=40)
box_5.insert(10, "ktsarapk@alumni.unca.edu")
# text box 7
box_6 = tk.Entry(master, text="", width=40)
box_6.insert(10, "LinkedIn URL")
# Adds .grid(row=n .....) to every box_n

for i in np.arange(row_start+starting_row_n,row_end+starting_row_n):
        eval('box_' + str(i-starting_row_n) + '.grid(row=' + str(i+1+starting_row_n) +
        ', column=1 ,sticky=(N, E, W), padx=5, pady=5'+')')

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
	# loader = jinja2.FileSystemLoader(os.path.abspath('.'))
    loader = jinja2.FileSystemLoader(os.path.abspath('.'))
)

# This function allows the user to select .tex file
def get_tex_name(file_select):
    file_name = filedialog .askopenfilename(title = 'Select .tex File',filetypes = (("LaTeX Files","*.tex"),))
    file_select.delete(0,END)
    file_select.insert(0,file_name)

#This function modifies the latex file, creates a new latex files, converts it to pdf and saves it locally
def generate_pdf():
    # Extracts the folder path of a file
    path = os.path.dirname(os.path.abspath(box_0.get()))
    # Creates a folder named using the inputted company name, if it doesn't already exist
    ctd=os.getcwd()+'/' + box_1.get()
    if not os.path.exists(ctd):
        os.mkdir(ctd)
    # Copies .tex file form slected folder to working path and renames it to copy_of_tex_template.tex
    shutil.copy(os.path.join(path , box_0.get()),
    os.path.join(os.getcwd(), 'copy_of_tex_template.tex'))
    # Combines template and variables
    template = latex_jinja_env.get_template('copy_of_tex_template.tex')
    document = template.render(
    CompanyName=box_1.get(),
    jobTitle=box_2.get(),
    JobLocation =box_3.get(),
    MyAddress=box_4.get(),
    Email=box_5.get()
    )
    file_name = 'CL ' +box_1.get() + ' ' + box_2.get()+'.tex'
    # write over the document file that we created
    with open(file_name,'w') as output:
            output.write(document)
    # Creates pdf file from the tex file that we created. Note: alternatively we can use subprocess.check_call to display errors.
    # Must have correct typeseeting engine selected ; LaTeX, pdfTeX, XeTeX, LuaTeX,etc
    pdf = subprocess.call([typesetting_var.get(),
    '-interaction=nonstopmode', # Use this to ignore errors
    file_name])
    # Moves the generated files into their associated folder. This will move and replace if file already exists under the same name.
    output_types = [str('.aux'),str('.pdf'),str('.out'),str('.tex'),str('.log')]
    for output_type in output_types:
        shutil.move(os.path.join(os.getcwd() , 'CL ' +box_1.get() + ' ' + box_2.get()+output_type),
        os.path.join(ctd, 'CL ' +box_1.get() + ' ' + box_2.get()+output_type))

# This function will convert a website to a pdf file and save it on your computer
def html_to_pdf():
    #path = input("Please enter the file path ex. C:\Jim\Desktop")
    # This requires you to have wkhtmltopdf.exe in the same folder as this python code.
    path_wkhtmltopdf = r'wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    if pdfkit.from_url(box_6.get(), box_1.get() + ' ' + box_2.get()+'.pdf'): # Check if method from_url returned True
        print("Sucessfully created PDF")
    else:
        print("[ERROR] Could not generate PDF")
    ctd=os.getcwd()+'/' + box_1.get()
    if not os.path.exists(os.getcwd()+'/' + box_1.get()):
        os.mkdir(ctd)
    shutil.move(os.path.join(os.getcwd() , box_1.get() + ' ' + box_2.get()+'.pdf'),
    os.path.join(ctd, box_1.get() + ' ' + box_2.get()+'.pdf'))

## Buttons on the side -->
# creates a button that calls a function for scrapping a public LinkedIn job profile for job title, location and company name
tk.Button(master, text='Autofill using LinkedIn link',
command=linkedin).grid(row=7, column=2, sticky=(N, E, W), pady=5)
# Creates a button to that calls a quit function to close the window and stop the execution of the code
tk.Button(master, text="Browse...", width=10,
command=lambda:get_tex_name(box_0)).grid(row=1, column=2, sticky=(N, E, W), pady=5)

# Buttons below tex-boxes
# Creates a button to call the function that generates the PDF from a latex file
tk.Button(master, text='Modify the LaTeX file and generate a PDF file ',
command=generate_pdf).grid(row=8, column=2, sticky=(N, E, W), pady=5)
# creates a button that calls a function for scrapping a public LinkedIn job profile for job title, location and company name
tk.Button(master, text='Save LinkedIn job description as PDF',
command=html_to_pdf).grid(row=10, column=1, sticky=(N, E, W), pady=5)
# Creates a button to that calls a quit function to close the window and stop the execution of the code
tk.Button(master, text='Quit',
command=master.quit).grid(row=11,column=1, sticky=(N, E, W), pady=5)
# Slider for the latex typesetting
typesetting_slider = OptionMenu(master, typesetting_var, *typesetting_options)
typesetting_slider.grid(row=8,column=1, sticky=(N, E, W), pady=5)


def ok():
    print(box_0.get())
tk.Button(master, text='Ok',
command=ok).grid(row=13,column=1, sticky=(N, E, W), pady=5)

tk.mainloop()
#
master.mainloop()
