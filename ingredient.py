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
            api_key = os.getenv('API_KEY'),
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
            "}\n"
            "\n"
            "If no ingredients are detected, return:\n"
            '{\n  "ingredients": [],\n  "food_suggestions": []\n}'
        )

        response = self.client.create_completion(
            model="gpt-4-vision-preview",  # Azure OpenAI model name
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

        # Parse the JSON response
        response_data = response.choices[0].message.content

        # response_data = response_data.strip().split('```json')[1].strip().rstrip('```')
        # if response_data:  # Ensure there's content to parse
        #     response_data = json.loads(response_data)  # Parse the JSON string
        # else:
        #     raise ValueError("Received empty response data from the API.")
        #
        # ingredients = response_data.get("ingredients", [])
        # food_suggestions = response_data.get("food_suggestions", [])

        try:
            # Ensure response_data is a string before processing
            if not isinstance(response_data, str):
                raise ValueError("Response data is not a string.")

            # Extract JSON block if it exists
            if "```json" in response_data:
                try:
                    response_data = response_data.strip().split("```json", 1)[1].strip().rstrip("```")
                except IndexError:
                    raise ValueError("Failed to extract JSON block from response.")

            # Ensure we have valid content
            if not response_data.strip():
                raise ValueError("Received empty response data from the API.")

            # Parse the JSON string
            try:
                response_data = json.loads(response_data)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON format: {e}. Raw response: {repr(response_data)}")

            # Extract ingredients and food suggestions
            ingredients = response_data.get("ingredients", [])
            food_suggestions = response_data.get("food_suggestions", [])

        except Exception as e:
            print(f"Error processing API response: {e}")
            response_data = {}  # Default to an empty dictionary if there's an error
            ingredients = ['Retry.......']
            food_suggestions = ['Retry.....']

        # Store them as class variables for use elsewhere
        self.ingredients = ingredients
        self.food_suggestions = food_suggestions

        return self.ingredients, self.food_suggestions  # Return the parsed JSON object

    def manual_prompt(self, user_input):
        ingredients = [ingredient.strip() for ingredient in user_input.split(',')]

        prompt = (
            f"You are given a list of food ingredient:'{ingredients}'. Please respond in JSON format with the following keys:\n"
            "'food_suggestions': A list of food that can be made with the ingredient.\n"
            "If you cannot see any ingredients, use an empty list for 'ingredients' and 'food_suggestions'."
        )

        response = self.client.create_completion(
            model="gpt-4",  # Azure OpenAI model name
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ])

        response_data = response.choices[0].message.content

        response_data = response_data.strip().split('```json')[1].strip().rstrip('```')
        if response_data:  # Ensure there's content to parse
            response_data = json.loads(response_data)  # Parse the JSON string
        else:
            raise ValueError("Received empty response data from the API.")

        food_suggestions = response_data.get("food_suggestions", [])

        return ingredients, food_suggestions  # Return the parsed JSON object

    def get_cooking_instructions_and_ingredients(self, ingredient_list, user_choice):

        print(user_choice)

        prompt = (
          
        f"""
        You are a helpful chef assistant.

        You are given a list of food ingredients: *{ingredient_list}*

        Create a recipe for **{user_choice}**.

        **Instructions**:
        Give a clear, step-by-step guide using numbered steps. Start each step with a number like '1.', '2.', etc. Include relevant emojis to make the instructions fun and engaging.

        **Ingredients**:
        - First, list the provided ingredients.
        - Then, suggest any *additional ingredients* that would enhance or complete the recipe if needed.

        **Format your response using the following rules**:
        - Use **double asterisks** for section titles like **Ingredients**, **Instructions**, etc.
        - Use *single asterisks* for items in a list (e.g., ingredients).
        - Start each instruction step with a number followed by a dot (e.g., 1.).
        """

      )

        response = self.client.create_completion(
            model="gpt-4",  # Azure OpenAI model name
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ])

        response_data = response.choices[0].message.content
        return response_data

        # response_data = response_data.strip().split('```json')[1].strip().rstrip('```')
        # if response_data:  # Ensure there's content to parse
        #     response_data = json.loads(response_data)  # Parse the JSON string
        # else:
        #     raise ValueError("Received empty response data from the API.")
        #
        # food_suggestions = response_data.get("step-by-step-instructions", [])
        # Additional_ingredient = response_data.get("Additional_ingredient", [])
        #
        # return Additional_ingredient, food_suggestions  # Return the parsed JSON object


# Check for the food and identify it


class Food_Analyzer:
    def __init__(self, client):
        self.client = client

    def food_detect(self, image_path):
        base64_image = ImageProcessor.encode_image(image_path)
        prompt = ("You are given an image of food . Tell me what food you are seeing,"
                  "list the ingredient that is used to make it."
                  f"Based on the ingredient analysis,, generate step-by-step instructions to make the food. "

                  )
        response = self.client.create_completion(
            model="gpt-4-vision-preview",  # Azure OpenAI model name
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
            # f",if there is 'or' separate the different food and make them different "
            f"{initial_prompt_result}.")
        response = self.client.create_completion(
            model="gpt-4",  # Azure OpenAI model name
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

        # print(ingredient_analysis)
        food_suggestions = self.analyzer.get_food_suggestions(ingredient_analysis)
        print(food_suggestions)

        # print(food_suggestions[0])

        user_choice = int(input("Enter the food you want to make: "))
        # print("You chose: ", user_choice)

        cooking_instructions = self.analyzer.get_cooking_instructions_and_ingredients(ingredient_analysis,
                                                                                      food_suggestions[user_choice])
        print(cooking_instructions)


if __name__ == '__main__':
    # Azure OpenAI configuration

    client = OpenAIClient()
    model = IngredientAnalyzer(client)

    session = model.auto_detect('/Users/danielsamuel/PycharmProjects/MealLensAI/AI/okra-stew-ingredients-copy.jpg')
    # print(session)

    inst = model.get_cooking_instructions_and_ingredients(session[0],'rice')
    print(inst)










    # session1 = Food_Analyzer(client)
    #
    # result = session1.food_detect('/Users/danielsamuel/PycharmProjects/MealLensAI/AI/okra-stew-ingredients-copy.jpg')
    # print(result)

    # food_detected = session1.get_food_suggestions('/Users/danielsamuel/PycharmProjects/MealLensAI/AI/img.jpg')
    # print(food_detected)

    # auto_mode = True  # Set this to True or False based on your requirement
    # ingredients_input = None
    #
    # if not auto_mode:
    #     ingredients_input = input("Enter ingredients separated by commas: ")
    #
    # session.run(auto_mode, ingredients_input)




