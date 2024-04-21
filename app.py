from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from utils.main import zip, unzip

import xml.etree.ElementTree as ET
import gzip
import io
import os

# import mimetypes
# def get_mime_type(file_name):
#     mime_type, _ = mimetypes.guess_type(file_name)
#     return mime_type

app = Flask(__name__)
CORS(app)


@app.route('/upload&zip', methods=['POST'])
def handle_upload_and_zip():
    files_data = request.json
    all_content = ''
    for i in range(len(files_data)):
        print(files_data[i])
        name = files_data[i]['name']
        type = files_data[i]['type']
        content = files_data[i]['content']
        all_content += f'<d><n>{name}</n><t>{type}</t><c>{content}</c></d>' # d: data, n: name, t:type c: content
        
    with open('dntc.txt', 'w') as file:
        file.write(all_content)
    
    zip('dntc.txt', 'result.txt')
        
    os.remove('dntc.txt')
    
    return jsonify({"status": "success"})


@app.route('/upload&unzip', methods=['POST'])
def handle_upload_and_unzip():
    files = request.files.getlist('files')
    if not files:
        return jsonify({"status": "failure", "message": "No files uploaded"}), 400
    
    unzipped_files = []
    for file in files:
        compressed_file = file.read()
        decompressed_data = io.BytesIO(compressed_file)
        
        with gzip.GzipFile(fileobj=decompressed_data, mode='rb') as gz:
            binary_data = gz.read()        

        with open('content.txt', 'wb') as file:
            file.write(binary_data)
            
        unzip('content.txt', 'dntc.txt')

        os.remove('content.txt')
        
        with open('dntc.txt', 'r') as file:
            data = file.read()
                
        xml_data = '<root>' + data + '</root>'
        root = ET.fromstring(xml_data)
        
        for d in root.findall('d'):
            name = d.find('n').text
            type = d.find('t').text
            content = d.find('c').text
            unzipped_files.append({"name": name, "type": type, "content": content})
                    
        os.remove('dntc.txt')
    
    return jsonify({"status": "success", "files": unzipped_files})


@app.route('/download', methods=['GET'])
def handle_download():
    with open('result.txt', 'rb') as file:
        binary_data = file.read()
        
    compressed_data = io.BytesIO()
    
    with gzip.GzipFile(fileobj=compressed_data, mode='wb') as gz:
        gz.write(binary_data)
        
    compressed_data.seek(0)
    
    os.remove('result.txt')
    
    return send_file(
        compressed_data,
        mimetype='application/gzip',
        download_name='zipped_data.gz',
        as_attachment=True
    )
    

if __name__ == '__main__':
    app.run(debug=True)
