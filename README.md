# Meallens AI Backend API Documentation

This document provides a detailed overview of the endpoints available in the Meallens AI backend Flask application (`app.py`). This API powers the frontend applications for ingredient analysis and food detection.

## Getting Started

To run the application locally, ensure you have Python installed and the required libraries.

1.  **Clone the repository (if applicable) or save the `app.py`, `ingredient.py`, `google_search.py`, `youtube_search.py` files.**
2.  **Install dependencies:** You will likely need `Flask`, `requests`, and potentially other libraries depending on the `ingredient` and search modules. A `requirements.txt` is recommended.
    ```bash
    pip install Flask requests # Add other dependencies as needed
    ```
3.  **Set environment variables:** The application requires API keys for OpenAI, YouTube, and Google Custom Search.
    ```bash
    export API_KEY='your_openai_api_key'
    export YOUTUBE_API_KEY='your_youtube_api_key' # Note: The code has a hardcoded key, consider using the environment variable instead.
    export GOOGLE_SEARCH_API_KEY='your_google_search_api_key' # Note: The code has a hardcoded key, consider using the environment variable instead.
    export CX='your_google_search_cx' # Note: The code has a hardcoded CX, consider using the environment variable instead.
    ```
4.  **Run the Flask application:**
    ```bash
    python app.py
    ```
    The application will run on `http://127.0.0.1:5000/` by default in debug mode.

## API Endpoints

### 1. `/`

*   **Method:** `GET`
*   **Description:** A simple welcome endpoint to confirm the API is running.
*   **Parameters:** None
*   **Response:**
    *   `200 OK`
    *   `application/json`
    ```json
    {
      "message": "Welcome to your Flask API with HTTPS!"
    }
    ```

### 2. `/process`

*   **Method:** `POST`
*   **Description:** Processes either an ingredient image or a list of ingredients to detect ingredients and suggest food possibilities. This is typically used by the ingredient analysis part of the application.
*   **Parameters:**
    *   `image_or_ingredient_list`: String (`'image'` or `'ingredient_list'`) - Specifies whether the input is an image or a text list of ingredients. (Required)
    *   If `image_or_ingredient_list` is `'image'`:
        *   `image`: File - The image file containing ingredients. (Required)
    *   If `image_or_ingredient_list` is `'ingredient_list'`:
        *   `ingredient_list`: String - A text input listing the ingredients. (Required)
*   **Response:**
    *   `200 OK`
    *   `application/json`
    *   Returns an `analysis_id`, the AI's initial response (detected ingredients), and a list of food suggestions based on the ingredients.
    ```json
    {
      "analysis_id": "unique_id_string",
      "response": ["ingredient 1", "ingredient 2", ...],
      "food_suggestions": ["Food Suggestion 1", "Food Suggestion 2", ...]
    }
    ```
    *   `400 Bad Request`
    *   `application/json`
    *   Returns an error message if required parameters are missing or the `image_or_ingredient_list` value is invalid.
    ```json
    {
      "error": "Error message"
    }
    ```

### 3. `/instructions`

*   **Method:** `POST`
*   **Description:** Generates cooking instructions for a specific food suggestion based on a previous `/process` analysis. This is used by the ingredient analysis part after the user selects a food suggestion.
*   **Parameters:**
    *   `food_choice_index`: String - The food suggestion chosen by the user (e.g., "Orange Chicken"). (Required)
    *   `food_analysis_id`: String - The `analysis_id` received from the `/process` endpoint. (Required)
*   **Response:**
    *   `200 OK`
    *   `application/json`
    *   Returns the cooking instructions for the chosen food.
    ```json
    {
      "instructions": "Step 1: ...\nStep 2: ..."
    }
    ```
    *   `400 Bad Request`
    *   `application/json`
    *   Returns an error message if `food_choice_index` or `food_analysis_id` are missing or if the `analysis_id` is not found (e.g., file expired).
    ```json
    {
      "error": "Error message"
    }
    ```

### 4. `/resources`

*   **Method:** `POST`
*   **Description:** Fetches YouTube video tutorials and Google search results for a single food item. This is primarily used by the ingredient analysis part after instructions are generated.
*   **Parameters:**
    *   `food_choice_index`: String - The food item to search resources for (e.g., "Orange Chicken"). (Required)
*   **Response:**
    *   `200 OK`
    *   `application/json`
    *   Returns lists of YouTube and Google search results.
    ```json
    {
      "YoutubeSearch": [
        {"title": "Video Title 1", "link": "Video URL 1"},
        ...
      ],
      "GoogleSearch": [
        {"title": "Article Title 1", "description": "Snippet 1", "link": "Article URL 1"},
        ...
      ]
    }
    ```
    *   `400 Bad Request`
    *   `application/json`
    *   Returns an error message if `user_choice` is missing.
    ```json
    {
      "error": "user choice is required"
    }
    ```

### 5. `/food_detect`

*   **Method:** `POST`
*   **Description:** Processes an image to detect food items and generate cooking instructions for one of the detected foods. This is the initial endpoint for the food detection part of the application.
*   **Parameters:**
    *   `image`: File - The image file containing the food. (Required)
*   **Response:**
    *   `200 OK`
    *   `application/json`
    *   Returns cooking instructions (likely for the main detected food) and an array of all detected food names.
    ```json
    {
      "instructions": "Instructions text...",
      "food_detected": ["Detected Food 1", "Detected Food 2", ...]
    }
    ```
    *   `400 Bad Request`
    *   `application/json`
    *   Returns an error message if the image file is missing.
    ```json
    {
      "error": "Error message"
    }
    ```

### 6. `/food_detect_resources`

*   **Method:** `POST`
*   **Description:** Fetches YouTube video tutorials and Google search results for a list of food items. This endpoint is specifically designed to be called after the `/food_detect` endpoint to get resources for all detected foods.
*   **Parameters:**
    *   `food_detected`: JSON Array of Strings - An array containing the names of the detected food items (typically the `food_detected` array from the `/food_detect` response). (Required)
*   **Request Body Example:**
    ```json
    {
      "food_detected": ["Orange Chicken", "Pounded Yam"]
    }
    ```
*   **Response:**
    *   `200 OK`
    *   `application/json`
    *   Returns nested lists of YouTube and Google search results, where each inner list corresponds to a food item in the `food_detected` input array. The order of results in the inner lists corresponds to the order of foods in the input array.
    ```json
    {
      "YoutubeSearch": [
        [{"title": "Video Title for Food 1", "link": "Video URL 1"}, ...], // Resources for food_detected[0]
        [{"title": "Video Title for Food 2", "link": "Video URL 2"}, ...], // Resources for food_detected[1]
        ...
      ],
      "GoogleSearch": [
        [{"title": "Article Title for Food 1", "description": "Snippet 1", "link": "Article URL 1"}, ...], // Resources for food_detected[0]
        [{"title": "Article Title for Food 2", "description": "Snippet 2", "link": "Article URL 2"}, ...], // Resources for food_detected[1]
        ...
      ]
    }
    ```
    *   `400 Bad Request`
    *   `application/json`
    *   Returns an error message if the `food_detected` list is missing or not in the correct format.
    ```json
    {
      "error": "food_detected list is required"
    }
    ```

## Workflow Examples

*   **Ingredient Analysis:**
    1.  User provides image or ingredient list to `/process`.
    2.  Frontend displays detected ingredients and food suggestions from the `/process` response.
    3.  User selects a food suggestion.
    4.  Frontend calls `/instructions` with the chosen suggestion and `analysis_id` to get cooking instructions.
    5.  Frontend calls `/resources` with the chosen suggestion to get YouTube and Google resources for that specific food.

*   **Food Detection:**
    1.  User provides an image to `/food_detect`.
    2.  Frontend displays the instructions and notes the `food_detected` array from the `/food_detect` response.
    3.  Frontend calls `/food_detect_resources` with the `food_detected` array.
    4.  Frontend displays the aggregated YouTube and Google resources from the `/food_detect_resources` response.

This documentation should provide a clear guide for anyone looking to understand or use your backend API. Let me know if you need any adjustments or further details!