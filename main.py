from flask import Flask, jsonify, request
import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.json_util import dumps 

load_dotenv()


app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db["Items"]




BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"

@app.route("/api/hello", methods=['GET'])
def hello():
    return "Hello, World!"

@app.route("/api/item/<id>", methods=['GET'])
def get_item(id):
    item = collection.find_one({"id": id})
    if item:
        return dumps(item), 200
    else:
        return jsonify({"error": f"Item with id {id} not found"}), 404
    
def UpdateFile(filename, content):
    try:
        with open(BASE_DIR+ filename + ".json", 'w') as file:
            json.dump(content, file, indent=2)

    except FileNotFoundError as fnf_error:
        raise FileNotFoundError("error: Failed to create new file.") 
            
       
                

@app.route("/api/item/create", methods=['POST'])
def create_item():
    data = request.json
    item_id = data.get("id")

    if not item_id:
        return jsonify({"error": "Missing 'id' in request"}), 400

    if collection.find_one({"id": item_id}):
        return jsonify({"error": f"Item with id '{item_id}' already exists."}), 409

    try:
        collection.insert_one(data)
        return jsonify({"success": f"Item with id '{item_id}' created."}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500



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


# @app.route("/api/json/<filename>", methods=['DELETE'])
# def deleteJSONContent(filename):
#     data = request.json
#     name = data.get('name')
#     id = str(data.get('id'))

#     try:
#         JSONfile = GetFile(filename)
#     except FileNotFoundError:
#         return jsonify({"error": f"File {filename}.json not found"}), 404

#     for donut in JSONfile:
#         if donut.get("name") == name:
#             batters = donut.get("batters", {}).get("batter", [])
#             original_len = len(batters)
#             new_batters = [b for b in batters if b.get("id") != id]

#             if len(new_batters) == original_len:
#                 return jsonify({"error": f"No batter with id {id} found for donut {name}"}), 404
#             donut["batters"]["batter"] = new_batters

#             try:
#                 UpdateFile(filename, JSONfile)
#             except Exception as e:
#                 return jsonify({"error": str(e)}), 500
            
#             return jsonify({"success": f"Batter with id {id} deleted from {name}"}), 200
        
#     return jsonify({"error": f"Donut named {name} not found."}), 404
    
    
# @app.route("/api/json/<filename>", methods=['PUT'])
# def updateJSONContent(filename):
#     data = request.json
#     name = data.get('name')
#     id = str(data.get('id'))
#     type = data.get('type')
#     try:
#         JSONfile = GetFile(filename)
#     except Exception as e:
#         return {"error": str(e)}
    
#     for donut in JSONfile:
#         found = False
#         if donut.get("name") == name:
#             found = True
#             batter = donut.get("batters", {}).get("batter", [])
            
#             if not any(b.get("id") == id for b in batter):
#                 batter.append({
#                     "id": id,
#                     "type": type
#                 })
#                 try:
#                     UpdateFile(filename, JSONfile)
#                 except Exception as e:
#                     return {"error": str(e)} 
#                 finally: 
#                     return jsonify({"Success": f"Added batter into {name}"}), 200
                
#             else:
#                 return jsonify({"error": f"Batter with id:{id} already exists."}), 409
#     if not found:
#             return jsonify({"error": f"Donut named {name} not found."}), 400

    
if __name__ == "__main__":
    app.run(debug=True)
