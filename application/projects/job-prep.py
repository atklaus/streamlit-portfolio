###################################################################
#IMPORT MODULES
###################################################################

import pandas as pd
import numpy as np
import os
from datetime import datetime
import itertools
import inspect
from enum import Enum
import unicodedata
import sys
import re
import docx
from docx import Document
from docx2pdf import convert

###################################################################
#INPUTS
###################################################################

working = '/Users/adamklaus/Documents/Personal/Develop/Career/Resume'
os.chdir(working)

#Create doc object
doc = docx.Document("Adam_Klaus_Cover_Letter.docx")

#Define unique job
manager = 'Hiring Manager'
industry = 'Data Science'
company = "Discover"
role = 'Senior Data Science Analyst'
source = 'LinkedIn'
custom = "This job posting caught my attention because of the incredible reputation of Discover and the opportunity to complete end to end analysis."
skill1 = "I have a strong programming background with an emphasis on writing clean and maintainable code. This ensures that I reduce tech debt on the project I am working on and allows others to easily review my work."
skill2 = "I have more than 2 years of modeling experience and experience working on the Risk and Analytics team in my current role. In these roles I've worked with clients and cross-functional teams and am comfortable presenting my analysis."
# custom = "Additionally, I have a depth of experience working with Qualtrics and their API to create analysis of social science data from a large number of responses."

###################################################################
#Replace
###################################################################

manager_input = '[Hiring Manager]'
company_input = '[Company]'
industry_input = '[Industry]'
role_input = '[Role]'
source_input = '[Source]'
custom_input = '[Custom Text]'
skill1_input = '[Skill 1]'
skill2_input = '[Skill 2]'

#Read in text
all_paras = doc.paragraphs

#Replace inputs
for para in all_paras:
    if company_input in para.text or industry_input in para.text or role_input in para.text or source_input in para.text or custom_input in para.text or manager_input in para.text or skill1_input in para.text or skill2_input in para.text:
        para.text = para.text.replace(manager_input,manager)        
        para.text = para.text.replace(company_input,company)
        para.text = para.text.replace(industry_input,industry)
        para.text = para.text.replace(role_input, role)
        para.text = para.text.replace(source_input,source)
        para.text = para.text.replace(custom_input,custom)
        para.text = para.text.replace(skill1_input,skill1)
        para.text = para.text.replace(skill2_input,skill2)
        
    print(para.text)

file_name = company + '_Cover_Letter'
doc.save(file_name + ".docx")
convert(file_name + ".docx")
# convert(company + ".docx", company + ' Cover Letter' + ".pdf")
os.remove(file_name + ".docx")




