from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    msg = request.json.get('message')
    response = 'processed msg: ' + msg
    print(response)
    return response

if __name__ == '__main__':
    print('starting flask')
    app.run(port=5000)
