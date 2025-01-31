from flask import Flask, request, jsonify
from flask_cors import CORS
from agent import interact_with_agent

app = Flask(__name__)
CORS(app) 

@app.route('/api/submit', methods=['POST'])
def submit_input():
    data = request.json
    user_input = data.get('user_input', '')
    response =interact_with_agent(user_input)
    print(response)
    return jsonify({"message": f"{response}"})


if __name__ == '__main__':
       app.run()
