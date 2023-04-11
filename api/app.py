import io
import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS
import openai
from reportlab.pdfgen import canvas
from PyPDF2 import PdfFileWriter, PdfFileReader


app = Flask(__name__)
CORS(app)

openai_model_id = "text-davinci-003"
openai_api_key = os.getenv('OPENAI_API_KEY')


@app.route('/scrape', methods=['POST'])
def scrape_url():
    url = request.json.get('scrape')
    if not url:
        return jsonify({'error': 'Please provide a URL parameter'}), 400

    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({'error': 'Unable to access URL'}), 400

    soup = BeautifulSoup(response.content, 'html.parser')
    heading = soup.find('h1').text if soup.find(
        'h1') else "No heading to be scraped"

    # Extract all the paragraph
    paragraphs = soup.find_all('p')
    if paragraphs:
        paragraph_text = "\n\n ".join([p.text for p in paragraphs])
    else:
        paragraph_text = "No paragraph to be scraped"

    return jsonify({'heading': heading, 'paragraph_text': paragraph_text})


@app.route('/openai', methods=['POST'])
def openai_summary():
    text = request.json.get('text')
    if not text:
        return jsonify({'error': 'Please provide a text parameter'}), 400

    try:
        response = openai.Completion.create(
            model=openai_model_id,
            prompt="Summarize key points from the following text in 3-7 sentences: " + text,
            max_tokens=60,
            temperature=0.5,
            api_key=openai_api_key
        )
        summary = response.choices[0].text.strip()

        return jsonify(summary)

    except openai.Error as e:
        return jsonify({'error': str(e)}), 500


@app.route('/generate-pdf', methods=['GET'])
def download_pdf():
    text = response.josn.get("text")

    if text is None:
        return jsonify({"error": "No text to convert"})

    # create a PDF
    packet = io.Bytes();
    can = canvas.canvas(packet)

    # Set the font and write text into PDF
    can.setFont("Helvetical-regular", 14)
    can.drawString(100, 650, text)

    can.save()

    # Move to the begining of the PDF and write text
    packet.seek(0)
    new_pdf = PdfFileWriter(packet)
    output = PdfFileReader()

    # Add PDF to the output
    output.addPage(new_pdf.getPage(0))

    # Write the output to the reponse
    response = make_response(output.writeBytes())

    # Set the content type and disposition;
    response.headers['Content-Type'] = 'application/pdf'
    response.headers["Content-Disposition"] = "attachment; filename=output.pdf"


    return response

if __name__ == '__main__':
    app.run(debug=True)
