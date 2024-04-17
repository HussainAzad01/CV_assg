import re
import pandas as pd

def create_excel_from_text(text_content):
    data = []
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