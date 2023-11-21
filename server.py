from flask import Flask, request, jsonify
from model import predict
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "http://localhost:3000"}})  # Allow only requests from http://localhost:3000

@app.route('/', methods=['GET'])
def home():
    return "Hello world!"

@app.route('/predict', methods=['POST'])
def get_prediction():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file provided'})

    audio_file = request.files['audio_file']

    if audio_file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Example: Save the file to a folder named 'uploads'
    audio_file.save('uploads/' + audio_file.filename)
    audio_file.filename = "./uploads/" + audio_file.filename
    prediction = predict( audio_file.filename )

    # Add CORS headers to the response
    response = jsonify({'prediction': prediction})
    # Add CORS headers to the response 
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    return response

if __name__ == '__main__':
    app.run()
