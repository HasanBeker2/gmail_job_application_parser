### README.md for "Gmail Job Application Parser"

---

# Gmail Job Application Parser

This project is a Python-based tool that connects to your Gmail account, retrieves emails from a specific folder (label), and extracts key information related to job applications. The extracted information includes the application date, job title, company name, and the result of the application (whether positive, negative, or not provided). The tool uses the OpenAI API to help parse and summarize the content of the emails.

## Features

- **Connect to Gmail:** The tool securely connects to your Gmail account using IMAP.
- **Extract Job Information:** Retrieves emails from a specified label (e.g., "applications") and extracts important details such as the job title, company name, and the result of your application.
- **Date Extraction:** Automatically fetches the date the email was received.
- **OpenAI API Integration:** Uses OpenAI's GPT model to parse email content and determine the result of the application.
- **CSV Output:** Saves the extracted data into a CSV file for easy analysis and record-keeping.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or later installed on your local machine.
- A Gmail account with [Less Secure App Access](https://myaccount.google.com/lesssecureapps) enabled (or use an App Password if 2FA is enabled).
- An OpenAI API key to access GPT models.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/gmail-job-application-parser.git
   cd gmail-job-application-parser
   ```

2. **Set up a virtual environment (optional but recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install the required Python packages:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables:**

   Create a `.env` file in the root directory of your project with the following variables:

   ```env
   GMAIL_USERNAME=your_email@gmail.com
   GMAIL_PASSWORD=your_password_or_app_password
   OPENAI_API_KEY=your_openai_api_key
   ```

   **Note:** For security reasons, avoid hardcoding sensitive information. Always use environment variables.

## Usage

1. **Run the main script:**

   ```bash
   python main.py
   ```

2. **CSV Output:**

   The extracted data will be saved in a `job_applications.csv` file in the root directory. The CSV will have the following columns:

   - Application Date
   - Job Title
   - Company Name
   - Result

## Code Structure

- **gmail_utils.py:**
  - Handles Gmail connection, email fetching, and content extraction.
  - Includes functions for parsing email subjects, handling HTML content, and decoding various email formats.

- **openai_utils.py:**
  - Integrates with OpenAI API to analyze and summarize email content, focusing on determining the result of the job application.

- **main.py:**
  - The main script that ties everything together. It connects to Gmail, retrieves emails, processes them, and saves the results to a CSV file.

- **requirements.txt:**
  - Lists all the Python libraries required for the project.

## Error Handling

- **Date Parsing Issues:**
  - The script handles various date formats and attempts to parse them. If a date cannot be parsed, the date field is set to "Not provided".
  
- **Unicode Decoding Errors:**
  - The script includes error handling for character encoding issues, trying different encodings if UTF-8 fails.

## Limitations

- **IMAP Connection:**
  - Requires access to Gmail through IMAP. Ensure IMAP is enabled in your Gmail settings.
  
- **OpenAI API Usage:**
  - OpenAI API calls may incur costs depending on usage, and rate limits apply.

- **Email Structure:**
  - The script assumes that job-related information can be found in either the subject line or the body of the email. Highly unstructured emails may not yield accurate results.

## Contributing

Contributions are welcome! Please fork this repository, create a new branch for your feature or bugfix, and submit a pull request. 

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenAI](https://www.openai.com) for providing the GPT models used in this project.
- The [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) library for HTML parsing.
- The Python community for the many libraries that made this project possible.
