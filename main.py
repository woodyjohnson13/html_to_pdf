import requests
import pdfkit
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/hello', methods=['POST'])
def hello():
    return "Hello World!"

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.get_json()
        url = data['url']
        
        # Fetch the content of the URL
        response = requests.get(url)
        html_content = response.text
        
        # Convert HTML to PDF
        pdfkit.from_string(html_content, 'static/current_invoice.pdf')
        pdf_link = 'http://localhost:5000/static/output.pdf'
        
        return jsonify({'message': 'PDF generated successfully', 'pdf_link': pdf_link})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
