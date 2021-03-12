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
industry = 'data science'
company = "Civis Analytics"
role = 'senior data scientist'
source = 'LinkedIn'
custom = "This job posting caught my attention because of the opportunity to use my experience to empower progressive advocacy organizations. Over the past year, I have volunteered as the data team lead for the Chicago Hub of Sunrise Movement (a progressive non-profit fighting for climate justice). In this role I have helped create data pipelines to automate tasks, track member growth and created models to understand membership dropoff. With that in mind, helping other progressive organizations in my full-time job is truly my dream career."  
skill1 = "I have a strong programming background and have written code in a production environment. I also have had experience working in a variety of tech stacks to create these solutions."
skill2 = "I have worked in consulting before and have experience working with clients and presenting technical work."
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




