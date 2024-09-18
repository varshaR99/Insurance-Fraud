from docx2pdf import convert
import pdfplumber
from main import *
import joblib
import numpy as np



word_file_path = "insurance_form_creator.docx"
pdf_file_path = "final2.pdf"
convert(word_file_path, pdf_file_path)


    





