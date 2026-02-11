###################################################################
#IMPORT MODULES
###################################################################

import pandas as pd
import numpy as np
import os
from pathlib import Path
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

#Create doc object
DOC_PATH = Path(__file__).resolve().parent / "assets" / "Cover_Letter.docx"
doc = docx.Document(str(DOC_PATH))

#Define unique job
manager = 'Hiring Manager'
industry = 'data engineering'
company = "Grainger"
role = 'Senior Data Engineer'
source = 'Caroline from BurtchWorks'
custom = "This role caught my attention because of the incredible reputation of Grainger, as someone who graduated from the Grainger school of business at UW-Madison I've always had a lot respect for the company."  
skill1 = "I have experience in each part of the tech stack from sourcing data to deploying models to building self-service analytics."
skill2 = "I'm motivated by learning and will continue to refine my skills and keep up with new technology."

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



