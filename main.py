import csv
import os
from dotenv import load_dotenv
from gmail_utils import connect_gmail, get_emails_from_folder, fetch_email_content, extract_info_from_subject, extract_company_from_body

from openai_utils import extract_info_with_openai

load_dotenv()

def save_to_csv(data, filename="job_applications.csv"):
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Application Date", "Job Title", "Company Name", "Result"])
        for row in data:
            writer.writerow(row)

def parse_openai_response(response_text):
    lines = response_text.split('\n')
    data = {"Job Title": "Not provided", "Company Name": "Not provided", "Result": "Not provided"}
    
    for line in lines:
        if "Job Title:" in line:
            data["Job Title"] = line.split(":", 1)[1].strip()
        elif "Company Name:" in line:
            data["Company Name"] = line.split(":", 1)[1].strip()
        elif "Result:" in line:
            data["Result"] = line.split(":", 1)[1].strip()

    return data

def main():
    username = os.getenv("GMAIL_USERNAME")
    password = os.getenv("GMAIL_PASSWORD")
    folder_name = "basvurular"
    api_key = os.getenv("OPENAI_API_KEY")

    mail = connect_gmail(username, password)
    email_ids = get_emails_from_folder(mail, folder_name)

    email_ids = email_ids[:50]  # İlk 10 e-postayı işleme al

    extracted_data = []
    
    for email_id in email_ids:
        subject, from_, body, email_date = fetch_email_content(mail, email_id)
        
        # Tarihi doğrudan e-posta gönderim tarihinden al
        application_date = email_date
        
        # Diğer bilgileri OpenAI API'si ile al
        truncated_body = body[:1000]  # İlk 10.000 karakteri işleme al
        
        try:
            response_text = extract_info_with_openai(truncated_body, api_key)
            print("Extracted Info:", response_text)
            extracted_info = parse_openai_response(response_text)
            
            extracted_data.append([
                application_date,
                extracted_info["Job Title"],
                extracted_info["Company Name"],
                extracted_info["Result"],
            ])
        except Exception as e:
            print(f"Error extracting info: {e}")
            break

    save_to_csv(extracted_data)
    print(f"Data saved to CSV.")

if __name__ == "__main__":
    main()
