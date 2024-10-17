from flask import Flask, render_template, request, jsonify, send_file
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
API_KEY = '1E9A7767.C56F47D388BB3BCA4BE0E8B8'  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_images():
    description = request.form['description']
    shape = request.form['shape'] 
    api_url = f'https://image.pollinations.ai/prompt/{description} {shape}'
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.url 
        return jsonify([data])  
    else:
        print(f"Error: {response.status_code} - {response.text}")  
        return jsonify({'error': 'Failed to generate images'}), 500

@app.route('/download', methods=['GET'])
def download_image():
    url = request.args.get('url')
    if url:
        # Save the image temporarily
        image_response = requests.get(url)
        if image_response.status_code == 200:
            file_path = os.path.join('static', 'temp_image.jpg')
            with open(file_path, 'wb') as f:
                f.write(image_response.content)
            return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'Image not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)