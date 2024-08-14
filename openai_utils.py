import openai

def extract_info_with_openai(email_body, api_key):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that extracts specific information from an email."},
            {"role": "user", "content": f"From the following email, extract the following information: 1) Application Date, 2) Job Title, 3) Company Name, 4) Result (Positive or Negative). Email: {email_body}"}
        ],
        max_tokens=50,
        temperature=0.0,  # Düşük sıcaklık daha kesin cevaplar verir
    )
    
    return response.choices[0].message['content'].strip()
