import base64
from openai import AzureOpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()


class OpenAIClient:
    def __init__(self):
        base_url = "https://azureai3111594496.openai.azure.com/openai/deployments/MeallensAI/chat/completions?api-version=2025-01-01-preview"
        api_version = "2024-02-15-preview"  # Use the latest API version

        self.client = AzureOpenAI(
            api_key=os.getenv('API_KEY'),
            api_version=api_version,
            azure_endpoint=base_url
        )

    def create_completion(self, model, messages):
        return self.client.chat.completions.create(
            model=model,
            messages=messages
        )


class ImageProcessor:
    @staticmethod
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")


class IngredientAnalyzer:
    def __init__(self, client):
        self.client = client

    def auto_detect(self, image_path):
        base64_image = ImageProcessor.encode_image(image_path)
        prompt = (
            "You are given an image of food ingredients. Please respond strictly in JSON format. "
            "Ensure that:\n"
            "- All keys and string values use double quotes (\"\").\n"
            "- The JSON structure follows proper formatting.\n"
            "\n"
            "Return a JSON object with the following keys:\n"
            "{\n"
            '  "ingredients": [list of detected ingredients],\n'
            '  "food_suggestions": [list of possible food dishes]\n'
            '  "cooking_duration":[give me the time taken to cook each food]\n'
            "}\n"
            "\n"
            "If no ingredients are detected, return:\n"
            '{\n  "ingredients": [],\n  "food_suggestions": []\n}'
        )

        response = self.client.create_completion(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        )

        response_data = response.choices[0].message.content

        try:
            if not isinstance(response_data, str):
                raise ValueError("Response data is not a string.")

            if "```json" in response_data:
                try:
                    response_data = response_data.strip().split("```json", 1)[1].strip().rstrip("```")
                except IndexError:
                    raise ValueError("Failed to extract JSON block from response.")

            if not response_data.strip():
                raise ValueError("Received empty response data from the API.")

            try:
                response_data = json.loads(response_data)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON format: {e}. Raw response: {repr(response_data)}")

            ingredients = response_data.get("ingredients", [])
            food_suggestions = response_data.get("food_suggestions", [])
            cooking_duration = response_data.get("cooking_duration", [])

        except Exception as e:
            print(f"Error processing API response: {e}")
            response_data = {}
            ingredients = ['Retry.......']
            food_suggestions = ['Retry.....']
            cooking_duration = []

        self.ingredients = ingredients
        self.food_suggestions = food_suggestions
        self.cooking_duration = cooking_duration

        return self.ingredients, self.food_suggestions, self.cooking_duration

    def manual_prompt(self, user_input):
        ingredients = [ingredient.strip() for ingredient in user_input.split(',')]

        prompt = (
            f"You are given a list of food ingredient:'{ingredients}'. Please respond in JSON format with the following keys:\n"
            "'food_suggestions': A list of food that can be made with the ingredient.\n"
            "'cooking_duration': The time it takes to prepare the food.\n"
            "If you cannot see any ingredients, use an empty list for 'ingredients' and 'food_suggestions'."
        )

        response = self.client.create_completion(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ])

        response_data = response.choices[0].message.content
        response_data = response_data.strip().split('```json')[1].strip().rstrip('```')

        if response_data:
            response_data = json.loads(response_data)
        else:
            raise ValueError("Received empty response data from the API.")

        food_suggestions = response_data.get("food_suggestions", [])
        cooking_duration = response_data.get("cooking_duration", [])

        return ingredients, food_suggestions, cooking_duration

    def get_cooking_instructions_and_ingredients(self, ingredient_list, user_choice):
        prompt = (
            f"""
You are a helpful chef assistant.

You are given a list of food ingredients: *{ingredient_list}*

Create a recipe for **{user_choice}**.

Respond strictly in valid JSON format using this structure:
{{
  "ingredients_provided": [list of ingredients],
  "additional_ingredients": [list of any extra ingredients needed],
  "cooking_time": "Total cooking time in minutes or hours",
  "cooking_instructions": [
    "Step 1...",
    "Step 2...",
    ...
  ]
}}

Make the response easy to parse, use only double quotes, and avoid extra commentary outside the JSON.
"""
        )

        response = self.client.create_completion(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ])

        response_data = response.choices[0].message.content

        try:
            if "```json" in response_data:
                response_data = response_data.split("```json")[1].split("```")[0].strip()

            parsed_data = json.loads(response_data)
            ingredients_provided = parsed_data.get("ingredients_provided", [])
            additional_ingredients = parsed_data.get("additional_ingredients", [])
            cooking_time = parsed_data.get("cooking_time", "")
            cooking_instructions = parsed_data.get("cooking_instructions", [])

            return {
                "ingredients_provided": ingredients_provided,
                "additional_ingredients": additional_ingredients,
                "cooking_time": cooking_time,
                "cooking_instructions": cooking_instructions
            }

        except Exception as e:
            print(f"Error parsing cooking instructions JSON: {e}")
            return {}


class Food_Analyzer:
    def __init__(self, client):
        self.client = client

    def food_detect(self, image_path):
        base64_image = ImageProcessor.encode_image(image_path)
        prompt = (f"""
You are an expert food analyst.

You are given an image of food. Tell me what food you are seeing.

Then:

**1.** Identify the food name clearly.  
**2.** List the ingredients used to make it. 
**3.** identify the time taken to cook the food. 
Use *single asterisks* for each ingredient in the list.  
**4.** Generate step-by-step cooking instructions based on the ingredients.  
Start each step with a number followed by a dot (e.g., 1., 2., etc.).  
Add fun and relevant emojis to make it engaging.  

**Formatting rules**:
- Use **double asterisks** for section titles like **Food Name**, **Ingredients**, **Instructions**.
- Use *single asterisks* for ingredients or listed items.
- Start each cooking step with a number and a dot (e.g., 1.).
"""
        )

        response = self.client.create_completion(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ]
        )
        return response.choices[0].message.content

    def get_food_suggestions(self, image):
        initial_prompt_result = self.food_detect(image)
        prompt = (
            f"Extract just the name of the food being seen from this and return it to me and return it as a list separated by commas"
            f"{initial_prompt_result}."
        )

        response = self.client.create_completion(
            model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return initial_prompt_result, response.choices[0].message.content.split(", ")


class InteractiveSession:
    def __init__(self, client):
        self.analyzer = IngredientAnalyzer(client)

    def run(self, auto, ingredients_input=None):
        if auto:
            ingredient_analysis = self.analyzer.auto_detect('img.png')
        else:
            ingredient_analysis = self.analyzer.manual_prompt(ingredients_input)

        food_suggestions = self.analyzer.get_food_suggestions(ingredient_analysis)
        print(food_suggestions)

        user_choice = int(input("Enter the food you want to make: "))
        cooking_instructions = self.analyzer.get_cooking_instructions_and_ingredients(
            ingredient_analysis, food_suggestions[user_choice]
        )
        print(cooking_instructions)


if __name__ == '__main__':
    client = OpenAIClient()
    model = IngredientAnalyzer(client)

    session = model.auto_detect('C:/Users/USER/Desktop/mealai/AI/okra-stew-ingredients-copy.jpg')
    inst = model.get_cooking_instructions_and_ingredients(session[0], 'rice')
    print(inst)
