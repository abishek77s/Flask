from flask import Flask, jsonify, request

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



@app.route("/api/item/<id>", methods=['DELETE'])
def delete_item(id):
    result = collection.delete_one({"id": id})
    if result.deleted_count == 1:
        return jsonify({"success": f"Item with id '{id}' has been deleted."}), 200
    else:
        return jsonify({"error": f"Item with id '{id}' not found."}), 404

@app.route("/api/item/<id>/batter", methods=['DELETE'])
def delete_batter_from_item(id):
    data = request.json
    batter_id = str(data.get("id"))
    
    if not batter_id:
        return jsonify({"error": "Missing 'id' of batter to delete"}), 400

    item = collection.find_one({"id": id})
    if not item:
        return jsonify({"error": f"Item with id '{id}' not found."}), 404

    batters = item.get("batters", {}).get("batter", [])
    new_batters = [b for b in batters if b.get("id") != batter_id]

    if len(batters) == len(new_batters):
        return jsonify({"error": f"No batter with id '{batter_id}' found."}), 404

    try:
        collection.update_one(
            {"id": id},
            {"$set": {"batters.batter": new_batters}}
        )
        return jsonify({"success": f"Batter with id '{batter_id}' removed from item '{id}'."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@app.route("/api/item/<id>", methods=['PUT'])
def add_batter_to_item(id):
    data = request.json
    batter_id = str(data.get('id'))
    batter_type = data.get('type')

    if not batter_id or not batter_type:
        return jsonify({"error": "Missing 'id' or 'type' in request"}), 400

    item = collection.find_one({"id": id})
    if not item:
        return jsonify({"error": f"Item with id '{id}' not found."}), 404

    batters_list = item.get("batters", {}).get("batter", [])

    if any(batter.get("id") == batter_id for batter in batters_list):
        return jsonify({"error": f"Batter with id '{batter_id}' already exists."}), 409

    batters_list.append({
        "id": batter_id,
        "type": batter_type
    })

    updated_batters = {"batters.batter": batters_list}
    try:
        collection.update_one({"id": id}, {"$set": updated_batters})
        return jsonify({"success": f"Batter with id '{batter_id}' added to item '{id}'."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


    
if __name__ == "__main__":
    app.run(debug=True)
