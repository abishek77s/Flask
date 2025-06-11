from flask import Flask, jsonify, request
import json
import os

file_path = "E:/Flask/ex5.json"

app = Flask(__name__)


def getFile():
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


@app.route("/api/hello", methods=['GET'])
def hello():
    return "Hello, World!"


@app.route("/api/json", methods=['GET'])
def getJSON():
    ex5 = getFile()
    return ex5
    
    
@app.route("/api/json", methods=['PUT'])
def updateJSON():
    data = request.json
    name = data.get('name')
    id = data.get('id')
    type = data.get('type')

    try:
        ex5 = getFile()
    except FileNotFoundError:
        return ex5
    
    for donut in ex5:
        found = False
        if donut.get("name") == name:
            found = True
            batter = donut.get("batters", {}).get("batter", [])
            
            if not any(b.get("id") == id for b in batter):
                batter.append({
                    "id": str(id),
                    "type": type
                })
                with open(file_path, 'w') as file:
                    json.dump(ex5, file, indent=2)
                return jsonify({"Success": f"Added batter into {name}"}), 200
            else:
                return jsonify({"error": f"Batter with id:{id} already exists."}), 409
    
    if not found:
            return jsonify({"error": f"Donut named {name} not found."}), 400

    
if __name__ == "__main__":
    app.run(debug=True)
