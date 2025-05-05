

from typing import Tuple
from flask import Flask, request, jsonify

import google_search
from  google_search import GoogleSearch
from ingredient import OpenAIClient, IngredientAnalyzer,Food_Analyzer
import os
import tempfile
import json
import uuid
import youtube_search
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Initialize the OpenAI client
api_key = os.getenv('API_KEY')
youtube_api_key = 'AIzaSyCgbgyVCdZy4oBTw8UvL3_UmD6tVi0ovyw'
google_search_api_key = 'AIzaSyDHvkvp4jGmkIHntqrZ2HQGWC3HGqGtt_4'
cx = '13a96d83a84c64f2d'

client = OpenAIClient()
analyzer = IngredientAnalyzer(client)
food_analyzer = Food_Analyzer(client)

# Directory to store JSON files
storage_dir = 'analysis_data'
os.makedirs(storage_dir, exist_ok=True)

def save_analysis_to_file(analysis_id, data):
    file_path = os.path.join(storage_dir, f"{analysis_id}.json")
    with open(file_path, 'w') as f:
        json.dump(data, f)

def load_analysis_from_file(analysis_id):
    file_path = os.path.join(storage_dir, f"{analysis_id}.json")
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r') as f:
        return json.load(f)

@app.route('/')
def home():
    return jsonify(message="Welcome to your Flask API with HTTPS!")

@app.route('/process', methods=['POST'])
def process():
    # Step 1: Check for image or ingredient list
    if 'image_or_ingredient_list' not in request.form:
        return jsonify({"error": "Parameter 'image or ingredient_list' is required"}), 400

    image_or_text = request.form.get('image_or_ingredient_list')
    if image_or_text == 'image':
        # Handle image processing
        if 'image' not in request.files:
            return jsonify({"error": "Image file is required"}), 400

        image_file = request.files['image']
        if image_file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            image_file.save(temp_file.name)
            temp_file_path = temp_file.name

        result = analyzer.auto_detect(temp_file_path)

        # result = result[0]

        os.remove(temp_file_path)
    elif image_or_text == 'ingredient_list':
        # Handle ingredient list processing
        if 'ingredient_list' not in request.form:
            return jsonify({"error": "ingredient_list input is required"}), 400

        text_input = request.form.get('ingredient_list')
        result = analyzer.manual_prompt(text_input)

    else:
        return jsonify({"error": "Invalid 'image_or_ingredient_list' value. Must be 'image' or 'text'"}), 400

    # Generate a unique ID and store the result in a JSON file
    analysis_id = str(uuid.uuid4())
    save_analysis_to_file(analysis_id, result[0])

    # Step 2: Get food suggestions
    food_suggestions = result[1]

    # Step 3: Return food suggestions and wait for user choice
    return jsonify({"analysis_id": analysis_id, "response": result[0], "food_suggestions": food_suggestions})




@app.route('/instructions', methods=['POST'])
def instructions():
    # Step 4: Get user choice and generate instructions
    user_choice = request.form.get('food_choice_index')
    chat_id = request.form.get('food_analysis_id')
    json_file_name = f"{chat_id}.json"

    initial_prompt = load_analysis_from_file(chat_id)

    print(json_file_name,user_choice)
    print(initial_prompt)

    if not initial_prompt or not user_choice:
        return jsonify({"error": "Food suggestions and user choice are required"}), 400

    instructions = analyzer.get_cooking_instructions_and_ingredients(initial_prompt, user_choice)

    user_choice = f"How to make {user_choice}"


    YT = youtube_search.YouTubeSearch(youtube_api_key)
    GS = google_search.GoogleSearch()

    YT = YT.main(user_choice)
    GS = GS.main(user_choice)

    os.remove(f"analysis_data/{json_file_name}")

    return jsonify({"instructions": instructions, "YoutubeSearch": YT,"GoogleSearch": GS})


@app.route('/food_detect', methods=['POST'])
def food_detect():

        if 'image' not in request.files:
            return jsonify({"error": "Image file is required"}), 400

        image_file = request.files['image']

        if image_file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            image_file.save(temp_file.name)
            temp_file_path = temp_file.name

        result = food_analyzer.get_food_suggestions(temp_file_path)
        food_detected = result[1]
        # print(food_detected)
        YT_result = []
        GS_result = []

        inst = "How to make"
        for i in food_detected:
            print(i)

            YT = youtube_search.YouTubeSearch(youtube_api_key)
            GS = google_search.GoogleSearch()
            YT = YT.main(f"How to make {i}",5)
            GS = GS.main(f"How to make {i}")
            YT_result.append(YT)
            GS_result.append(GS)


        return jsonify({"instructions": result[0], "YoutubeSearch": YT_result, "GoogleSearch": GS_result})


if __name__ == '__main__':
    app.run(


    )