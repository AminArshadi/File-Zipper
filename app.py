from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from utils.main import zip, unzip

import io
import os

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/upload', methods=['POST'])
def handle_upload():
    files_data = request.json
        
    all_content = ''
    
    for i in range(len(files_data)):
        name = files_data[i]['name']
        content = files_data[i]['content']
        
        all_content += f'<d><n>{name}</n><c>{content}</c></d>' # d: data, n: name, c: content
        
        with open('dnc.txt', 'w') as file:
            file.write(all_content)
        
        zip('dnc.txt', 'result.txt')
    
    return jsonify({"status": "success"})


@app.route('/download', methods=['GET'])
def handle_download():
    
    with open('result.txt', 'r', encoding='iso-8859-1') as file:
        file_content = file.read()
    os.remove('result.txt')
    
    file_bytes = io.BytesIO(file_content.encode('utf-8')) # Convert string to bytes
    file_name = "zipped_data.txt"
    
    return send_file(
        file_bytes,
        as_attachment=True,
        download_name=file_name,
        mimetype='text/plain'
    )

if __name__ == '__main__':
    app.run(debug=True)
