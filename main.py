from flask import Flask, jsonify, request
import json
import os



app = Flask(__name__)


def GetFile(filename):
    file_path = "E:/Flask/"+ filename + ".json"
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
    
def UpdateFile(filename, content):
    try:
        with open("E:/Flask/"+ filename + ".json", 'w') as file:
            json.dump(content, file, indent=2)

    except FileNotFoundError as fnf_error:
        return jsonify({"error": "Failed to create new file."}), 404
            
       
                



@app.route("/api/hello", methods=['GET'])
def hello():
    return "Hello, World!"


@app.route("/api/json/<filename>", methods=['GET'])
def getJSON(filename):
    file = GetFile(filename)
    return file


@app.route("/api/json/create", methods=['POST'])
def createJSON():
    data = request.json
    filename = data.get('filename')
    content = data.get('content')
    try:
        if os.path.exists("E:/Flask/"+ filename + ".json"):
            return jsonify({"Failed": f"File {filename} already exists."}), 409
        status = UpdateFile(filename, content)
        return jsonify({"Success": f"File {filename} has been created."}), 200
    except FileNotFoundError:
        return status

    
@app.route("/api/json/<filename>", methods=['PUT'])
def updateJSON(filename):
    data = request.json
    name = data.get('name')
    id = data.get('id')
    type = data.get('type')
    try:
        JSONfile = GetFile(filename)
    except FileNotFoundError:
        return JSONfile
    
    for donut in JSONfile:
        found = False
        if donut.get("name") == name:
            found = True
            batter = donut.get("batters", {}).get("batter", [])
            
            if not any(b.get("id") == str(id) for b in batter):
                batter.append({
                    "id": str(id),
                    "type": type
                })
                try:
                    status = UpdateFile(filename, JSONfile)
                except:
                    return status
                return jsonify({"Success": f"Added batter into {name}"}), 200
            else:
                return jsonify({"error": f"Batter with id:{id} already exists."}), 409
    if not found:
            return jsonify({"error": f"Donut named {name} not found."}), 400

    
if __name__ == "__main__":
    app.run(debug=True)
