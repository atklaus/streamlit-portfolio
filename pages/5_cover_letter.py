import streamlit as st
import docx
from docx import Document
from docx2pdf import convert
import os
from pathlib import Path
from config import BASE_DIR, CREDS
from layout.header import page_header
import streamlit as st
import docx
from docx import Document
from docx2pdf import convert
import os
from io import BytesIO
import streamlit as st
import docx
from docx import Document
from weasyprint import HTML
from io import BytesIO

#REPLACE INFO

page_header('Cover Letter Generator')


def generate_cover_letter(manager, industry, company, role, source, custom, skill1, skill2):
    doc = Document("static/files/Cover_Letter.docx")
    
    manager_input = '[Hiring Manager]'
    company_input = '[Company]'
    industry_input = '[Industry]'
    role_input = '[Role]'
    source_input = '[Source]'
    custom_input = '[Custom Text]'
    skill1_input = '[Skill 1]'
    skill2_input = '[Skill 2]'
    
    all_paras = doc.paragraphs
    
    for para in all_paras:
        if any(keyword in para.text for keyword in [manager_input, company_input, industry_input, role_input, source_input, custom_input, skill1_input, skill2_input]):
            for run in para.runs:
                run.text = run.text.replace(manager_input, manager)
                run.text = run.text.replace(company_input, company)
                run.text = run.text.replace(industry_input, industry)
                run.text = run.text.replace(role_input, role)
                run.text = run.text.replace(source_input, source)
                run.text = run.text.replace(custom_input, custom)
                run.text = run.text.replace(skill1_input, skill1)
                run.text = run.text.replace(skill2_input, skill2)

    # Save DOCX to BytesIO object
    docx_io = BytesIO()
    doc.save(docx_io)
    docx_io.seek(0)
    docx_data = docx_io.read()

    # Convert DOCX to HTML here (this is a placeholder; you'd replace this with actual conversion code)
    html_content = "<html><body><h1>Hello World</h1></body></html>"
    
    # Convert HTML to PDF using WeasyPrint, stored in BytesIO object
    pdf_io = BytesIO()
    HTML(string=html_content).write_pdf(pdf_io)
    pdf_io.seek(0)
    pdf_data = pdf_io.read()

    return docx_data, pdf_data

st.title("Cover Letter Generator")

manager = st.text_input("Hiring Manager", "Hiring Manager")
industry = st.text_input("Industry", "Data Engineering")
company = st.text_input("Company", "Grainger")
role = st.text_input("Role", "Senior Data Engineer")
source = st.text_input("Source", "Caroline from BurtchWorks")
custom = st.text_area("Custom Text", "This role caught my attention because...")
skill1 = st.text_area("Skill 1", "I have experience in each part of the tech stack...")
skill2 = st.text_area("Skill 2", "I'm motivated by learning...")

if st.button("Generate Cover Letter"):
    docx_data, pdf_data = generate_cover_letter(manager, industry, company, role, source, custom, skill1, skill2)
        
    st.download_button(
        label="Download Word",
        data=docx_data,
        file_name=f"{company}_Cover_Letter.docx",  # Update this line
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
        
    st.download_button(
        label="Download PDF",
        data=pdf_data,
        file_name=f"{company}_Cover_Letter.pdf",  # Update this line
        mime="application/pdf"
    )


