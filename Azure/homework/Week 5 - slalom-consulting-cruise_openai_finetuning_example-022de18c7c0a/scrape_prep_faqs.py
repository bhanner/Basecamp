import requests
from bs4 import BeautifulSoup
import json

# This script scrapes the FAQ page of Norwegian Cruise Line and 
# prepares the data in the legacy format expected by OpenAI.
# Once the data has been created you need to run the dataset-preparer.py script to convert it to the new format.

# Define the URL
url = 'https://www.ncl.com/faq'

# Send a GET request to the URL
response = requests.get(url)

# Define the separator and stop sequence
separator = '\n\n###\n\n'
stop_sequence = '###'

# If the request was successful, proceed
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all the questions
    questions = soup.find_all('div', class_='faq-question')
    
    # Find all the answers
    answers = soup.find_all('div', class_='faq-answer')
    
    # Prepare the data
    data = []
    for q, a in zip(questions, answers):
        # Get the question text
        question_text = q.text.strip() + separator
        
        # Get the answer text and add whitespace at the beginning, remove any extra stop sequences
        answer_text = ' ' + a.get_text(strip=True).replace(stop_sequence, '') + '\n' + stop_sequence
        
        # Prepare the data in the desired format
        data.append({"prompt": question_text, "completion": answer_text})
        
    # Save the data to a JSONL file
    with open('faq_data_before_prep.jsonl', 'w') as json_file:
        for entry in data:
            json.dump(entry, json_file)
            json_file.write('\n')

else:
    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')
