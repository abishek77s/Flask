from flask import Flask, jsonify
import json
import os

file_path = "E:/SkillRank/JSON/ex5.json"

app = Flask(__name__)

@app.route("/api/hello", methods=['GET'])
def hello():
    return "Hello, World!"


@app.route("/api/json", methods=['GET'])
def getJSON():
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
    
        with open(file_path, 'r') as file:
            try:
                ex5 = json.load(file)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON: {e}")
        return ex5
        
    except FileNotFoundError as fnf_error:
        return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
