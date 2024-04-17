import os
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import PyPDF2
import re
import pandas as pd

def index(request):

    if request.method == "POST" and 'file_data' in request.FILES:
        data = []
        for resume in request.FILES.getlist('file_data'):
            if ".doc" or ".docx" in str(resume):
                return HttpResponse("Insert only in pdf format please")
            if resume:
                pdf_reader = PyPDF2.PdfReader(resume)
                text_content = ''
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    text_content += page.extract_text()

                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                phone_pattern = r'\+?[1-9][0-9]{7,14}'
                emails = re.findall(email_pattern, text_content)
                phone_numbers = re.findall(phone_pattern, text_content)
                if emails and phone_numbers:
                    for email, phone_number in zip(emails, phone_numbers):
                        row = {'phone_number': phone_number, 'email': email, 'text': text_content}
                        data.append(row)

                elif emails:
                    phone_numbers = ["No phone number provided"]
                    for email, phone_number in zip(emails, phone_numbers):
                        row = {'phone_number': phone_number, 'email': email, 'text': text_content}
                        data.append(row)

                else:
                    emails = ["No email provided"]
                    for email, phone_number in zip(emails, phone_numbers):
                        row = {'phone_number': phone_number, 'email': email, 'text': text_content}
                        data.append(row)

        df = pd.DataFrame(data)
        excel_file = 'output.xlsx'
        df.to_excel(excel_file, index=False)
        try:
            with open('output.xlsx', 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/msexcel')
                response['Content-Disposition'] = f'inline; filename="final-output.xlsx"'
                return response

        except:
            return render(request, 'index.html')
    return render(request, 'index.html')
