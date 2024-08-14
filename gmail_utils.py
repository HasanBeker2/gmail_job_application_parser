import imaplib
import email
from email.header import decode_header
import re
from datetime import datetime
from bs4 import BeautifulSoup
from email.utils import parsedate_to_datetime

def connect_gmail(username, password):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(username, password)
    return mail

def get_emails_from_folder(mail, folder_name):
    mail.select(folder_name)
    result, data = mail.search(None, "ALL")
    email_ids = data[0].split()
    return email_ids

def fetch_email_content(mail, email_id):
    result, data = mail.fetch(email_id, "(RFC822)")
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)
    
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding if encoding else "utf-8")
    
    from_ = msg.get("From")
    
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if "attachment" not in content_disposition:
                try:
                    if content_type == "text/plain":
                        body += part.get_payload(decode=True).decode("utf-8")
                    elif content_type == "text/html":
                        html = part.get_payload(decode=True).decode("utf-8")
                        # HTML'i düz metne çevir
                        soup = BeautifulSoup(html, "html.parser")
                        body += soup.get_text()
                except UnicodeDecodeError:
                    # UTF-8 başarısız olursa, ISO-8859-1 gibi farklı bir kodlama deneyin
                    try:
                        if content_type == "text/plain":
                            body += part.get_payload(decode=True).decode("ISO-8859-1")
                        elif content_type == "text/html":
                            html = part.get_payload(decode=True).decode("ISO-8859-1")
                            soup = BeautifulSoup(html, "html.parser")
                            body += soup.get_text()
                    except Exception as e:
                        print(f"Error decoding part of email: {e}")
    else:
        content_type = msg.get_content_type()
        try:
            if content_type == "text/plain":
                body = msg.get_payload(decode=True).decode("utf-8")
            elif content_type == "text/html":
                html = msg.get_payload(decode=True).decode("utf-8")
                soup = BeautifulSoup(html, "html.parser")
                body = soup.get_text()
        except UnicodeDecodeError:
            try:
                if content_type == "text/plain":
                    body = msg.get_payload(decode=True).decode("ISO-8859-1")
                elif content_type == "text/html":
                    html = msg.get_payload(decode=True).decode("ISO-8859-1")
                    soup = BeautifulSoup(html, "html.parser")
                    body = soup.get_text()
            except Exception as e:
                print(f"Error decoding email: {e}")
    
    # E-posta tarihini al ve parse et
    email_date = msg.get("Date")
    if email_date:
        try:
            email_date = parsedate_to_datetime(email_date).date()
        except Exception as e:
            print(f"Warning: Could not parse date format: {email_date}, Error: {e}")
            email_date = "Not provided"
    else:
        email_date = "Not provided"
    
    return subject, from_, body, email_date

def extract_info_from_subject(subject):
    parts = subject.split(' - ')
    if len(parts) >= 2:
        job_title = parts[0].strip()
        company_name = parts[1].strip()
    else:
        job_title = "Not provided"
        company_name = "Not provided"

    return job_title, company_name

def extract_company_from_body(body):
    company_match = re.search(r'\b(?:Firma|Company)\b\s*[:\s]\s*(\S+.*)', body, re.IGNORECASE)
    if company_match:
        company_name = company_match.group(1).strip()
    else:
        company_name = "Not provided"
    return company_name

def extract_job_title_from_body(body):
    job_title_match = re.search(r'\b(?:Position|Job Title)\b\s*[:\s]\s*(\S+.*)', body, re.IGNORECASE)
    if job_title_match:
        job_title = job_title_match.group(1).strip()
    else:
        job_title = "Not provided"
    return job_title
