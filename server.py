from flask import Flask, request, jsonify
from model import predict
from flask_cors import CORS
from pydub import AudioSegment
AudioSegment.ffmpeg = "C:/Users/bhave/Downloads/ffmpeg-6.1/ffmpeg-6.1"

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
    file_path = "uploads/" + audio_file.filename

    # Check if the file is an MP3 and convert it to WAV
    if audio_file.filename.lower().endswith('.mp3'):
        print(file_path)
        audio = AudioSegment.from_mp3('uploads/' + audio_file.filename)
        wav_file_path = 'uploads/' + audio_file.filename.replace('.mp3', '.wav')
        audio.export(wav_file_path, format='wav')
        file_path = wav_file_path  # Update the file path to the converted WAV file

    prediction = predict( file_path )

    # Add CORS headers to the response
    response = jsonify({'prediction': prediction})
    # Add CORS headers to the response 
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    return response

if __name__ == '__main__':
    app.run()
