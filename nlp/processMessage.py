from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/process-message', methods=['POST'])
def process_message():
  message = request.json['message']
  #do something with the message
  processed_response = f"Processed message: {message}"
  return jsonify({'response': processed_response})

if __name__ == '__main__':
  app.run(debug=True)