import base64
from openai import OpenAI
import os

class OpenAIClient:
    def __init__(self, api_key, base_url):
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def create_completion(self, model, messages):
        return self.client.chat.completions.create(model=model, messages=messages)

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
        prompt = "You are given an image of food ingredient. Tell me what ingredient you see and what food can be made with it."
        response = self.client.create_completion(
            model="gemini-2.0-flash-exp",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                    ],
                }
            ],
        )
        return response.choices[0].message.content

    def manual_prompt(self, user_input):
        ingredients = [ingredient.strip() for ingredient in user_input.split(',')]
        prompt = (
            f"You are given a list of food ingredient:'{ingredients}'"
            f" Tell me you see and what food can be made with it."
        )
        response = self.client.create_completion(
            model="gemini-2.0-flash-exp",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ])
        return response.choices[0].message.content

    def get_food_suggestions(self, initial_prompt_result):
        prompt = (f"Extract just the food suggestions from this and return them as a list separated by commas if there is 'or' separate the different food and make them different : "
                  f"{initial_prompt_result}.")
        response = self.client.create_completion(
            model="gemini-2.0-flash-exp",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content.split(", ")

    def get_cooking_instructions_and_ingredients(self, initial_prompt, user_choice):

        print(user_choice)
        prompt = (
            f"Based on the ingredient analysis: '{initial_prompt}', generate step-by-step instructions to make {user_choice}. "
            f"Also, suggest any additional ingredients needed to make this meal if the provided ingredients are insufficient."
        )
        response = self.client.create_completion(
            model="gemini-2.0-flash-exp",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content

class InteractiveSession:
    def __init__(self, client):
        self.analyzer = IngredientAnalyzer(client)

    def run(self, auto, ingredients_input=None):
        if auto:
            ingredient_analysis = self.analyzer.auto_detect('img.png')
        else:
            ingredient_analysis = self.analyzer.manual_prompt(ingredients_input)

        # print(ingredient_analysis)
        food_suggestions = self.analyzer.get_food_suggestions(ingredient_analysis)
        print(food_suggestions)

        # print(food_suggestions[0])

        user_choice = int(input("Enter the food you want to make: "))
        # print("You chose: ", user_choice)

        cooking_instructions = self.analyzer.get_cooking_instructions_and_ingredients(ingredient_analysis, food_suggestions[user_choice])
        print(cooking_instructions)

if __name__ == '__main__':
    api_key = "AIzaSyCMV1RzXC62lSyDxqcqlky-p1UzHqH2XEw"
    base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    client = OpenAIClient(api_key, base_url)
    session = InteractiveSession(client)

    auto_mode = True  # Set this to True or False based on your requirement
    ingredients_input = None

    if not auto_mode:
        ingredients_input = input("Enter ingredients separated by commas: ")

    session.run(auto_mode, ingredients_input)




