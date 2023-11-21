from flask import Flask, request, jsonify
from model import predict

app = Flask(__name__)

@app.route('/' ,  methods=['GET'])
def home():
    return "Hello world!"

@app.route('/predict', methods=['POST'])
def get_prediction():
    data = request.get_json()
    input_text = data['text']
    print(input_text)
    prediction = predict(input_text)
    return jsonify({'prediction': prediction})


if (__name__ == '__main__'):
    app.run()