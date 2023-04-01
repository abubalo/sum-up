import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

openai_api_key = os.getenv('OPENAI_API_KEY')
# this endpoint recieve url as a post request and use beautifull to scrape the url content and pass it OpenAI fetch endpiont.


@app.route('/scrape', methods=['POST'])
def scrape_url():
    url = request.json.get('scrape')
    if url is None:
        return jsonify({'error': 'Please provide a URL parameter'})

    # send a GET request to the URL
    response = requests.get(url)

    # check if the request was successful
    if response.status_code != 200:
        return jsonify({'error': 'Unable to access URL'})

    # parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # get the heading and paragraph text
    heading = soup.find('h1').text if soup.find(
        'h1') else "No content to be scraped"
    paragraph = soup.find('p').text if soup.find('p') else ""

    # call the open_ai endpoint with the extracted text as a parameter
    return open_ai(paragraph)


@app.route('/openai', methods=['GET'])
def open_ai(text):
    text = request.json['text']
    response = requests.post('https://api.openai.com/v1/completions',
                             headers={'Content-Type': 'application/json',
                                      'Authorization': 'Bearer ' + openai_api_key},
                             json={
                                 'model': 'text-davinci-003',
                                 'prompt': f'Please summarize the following article. Your summary should be approximately 3-4 sentences in length and cover the main points of the article. Use clear, concise language and avoid repeating information. Your summary will be used for a news briefing and should be suitable for a general audience. \n The text I have is:  \n\n{text}',
                                 'max_tokens': 7,
                                 'temperature': 0.5,
                                 'top_p': 1,
                                 'n': 1,
                                 'stream': False,
                                 'logprobs': None,
                                 'stop': '\n',
                             })
    return jsonify(response.json())



if __name__ == '__main__':
    app.run()
