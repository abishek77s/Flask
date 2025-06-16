from flask import Flask, jsonify, request
import json
import os



app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"


def GetFile(filename):
    file_path = BASE_DIR+ filename + ".json"
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
    
        with open(file_path, 'r') as file:
                file = json.load(file)
                return file
    except FileNotFoundError as fnf_error:
        raise FileNotFoundError("error: File not found.")
    
def UpdateFile(filename, content):
    try:
        with open(BASE_DIR+ filename + ".json", 'w') as file:
            json.dump(content, file, indent=2)

    except FileNotFoundError as fnf_error:
        raise FileNotFoundError("error: Failed to create new file.") 
            
       
                



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
        if os.path.exists(BASE_DIR+ filename + ".json"):
            return jsonify({"Failed": f"File {filename} already exists."}), 409
        UpdateFile(filename, content)
        return jsonify({"Success": f"File {filename} has been created."}), 200
    except Exception as e:
        return {"error": str(e)} 


@app.route("/api/json/delete", methods=['DELETE'])
def deleteJSON():
    data = request.json
    filename = data.get('filename')
    try:
        if not os.path.exists(BASE_DIR+ filename + ".json"):
            return jsonify({"Failed": f"File {filename} doesn't exists."}), 409
        os.remove(BASE_DIR+ filename + ".json")
        return jsonify({"Success": f"File {filename} has been deleted."}), 200
    except Exception as e:
        return {"error": str(e)} 


@app.route("/api/json/<filename>", methods=['DELETE'])
def deleteJSONContent(filename):
    data = request.json
    name = data.get('name')
    id = str(data.get('id'))

    try:
        JSONfile = GetFile(filename)
    except FileNotFoundError:
        return jsonify({"error": f"File {filename}.json not found"}), 404

    for donut in JSONfile:
        if donut.get("name") == name:
            batters = donut.get("batters", {}).get("batter", [])
            original_len = len(batters)
            new_batters = [b for b in batters if b.get("id") != id]

            if len(new_batters) == original_len:
                return jsonify({"error": f"No batter with id {id} found for donut {name}"}), 404
            donut["batters"]["batter"] = new_batters

            try:
                UpdateFile(filename, JSONfile)
            except Exception as e:
                return jsonify({"error": str(e)}), 500
            
            return jsonify({"success": f"Batter with id {id} deleted from {name}"}), 200
        
    return jsonify({"error": f"Donut named {name} not found."}), 404
    
    
@app.route("/api/json/<filename>", methods=['PUT'])
def updateJSONContent(filename):
    data = request.json
    name = data.get('name')
    id = str(data.get('id'))
    type = data.get('type')
    try:
        JSONfile = GetFile(filename)
    except Exception as e:
        return {"error": str(e)}
    
    for donut in JSONfile:
        found = False
        if donut.get("name") == name:
            found = True
            batter = donut.get("batters", {}).get("batter", [])
            
            if not any(b.get("id") == id for b in batter):
                batter.append({
                    "id": id,
                    "type": type
                })
                try:
                    UpdateFile(filename, JSONfile)
                except Exception as e:
                    return {"error": str(e)} 
                finally: 
                    return jsonify({"Success": f"Added batter into {name}"}), 200
                
            else:
                return jsonify({"error": f"Batter with id:{id} already exists."}), 409
    if not found:
            return jsonify({"error": f"Donut named {name} not found."}), 400

    
if __name__ == "__main__":
    app.run(debug=True)
