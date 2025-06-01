import requests
import json
import openai
import os
from dotenv import load_dotenv

# Setup environment variables
# Note for Google I had to setup a PSE, Project, Billing Account and then create a key to remove Ads in PSE dashboard)
# NOTE: If you do not add a CR after the last parameter you will get a 400 error from Google.
load_dotenv(dotenv_path ='apikey.env.txt')
CHATGPT_API_KEY = os.getenv('ChatGPT-APIKEY')
GOOGLE_API_KEY = os.getenv('Google-APIKEY')
CX = os.getenv('CX')

# Setup our OpenAI API
openai.api_key = CHATGPT_API_KEY

def google_search(query):
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={CX}&q={query}"
    response = requests.get(url)
    response.raise_for_status()

    return response.json()

def extract_data(google_response):
    items = google_response.get('items', [])
    result = {}
    for item in items:
        site_name = item.get('title')
        site_info = {
            'url': item.get('link'),
            'description': item.get('snippet')
        }
        result[site_name] = site_info

    return result

def send_to_chatgpt(data):
    system_content = (f"Act like a member of a granting committee at a non-profit funding organizations and answer the questions of the user based on the provided data in json format:{data}.")
    user_content = ("Explore the provided list and provide a summary of their key strengths that can help us make granting decisions.")

    system = {"role":"system", "content": system_content}
    user = {"role":"user", "content": user_content}

    response = openai.ChatCompletion.create(
        model = 'gpt-4',
        messages = [system,user],
        max_tokens = 1200
    )

    return(response.choices[0].message.content)


def main():
    query = "List 10 non-profit organisations in Victoria,BC,Canada"
    google_response = google_search(query)
    site_data = extract_data(google_response)
    chatgpt_response = send_to_chatgpt(site_data)

    #Print the responses
    print(chatgpt_response)

if __name__ == "__main__":
    main()
