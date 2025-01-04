import base64
from openai import OpenAI
import json
import os
import  os
import youtube_search as YT

# Initialize the OpenAI client
client = OpenAI(
    api_key="AIzaSyCMV1RzXC62lSyDxqcqlky-p1UzHqH2XEw",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")



def auto_detect(image: os.path) -> str:
    base64_image = encode_image(image)

    # Initial prompt
    prompt = "You are given an image of food ingredient. Tell me what ingredient you see and what food can be made with it."
    response = client.chat.completions.create(
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

    response = response.choices[0].message.content
    return response

def manual_prompt(user_input: str) -> str:
    ingredients = [ingredient.strip() for ingredient in user_input.split(',')]

    prompt = (
        f"You are given a list of food ingredient:'{ingredients}'"
        f" Tell me you see and what food can be made with it."
    )

    # Send the image and prompt
    response = client.chat.completions.create(
        model="gemini-2.0-flash-exp",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ])
    response = response.choices[0].message.content
    return response

def get_food_suggestions(initial_prompt_result: str) -> list:
    prompt = (f"Extract just the food suggestions from this and return them as a list separated by commas if there is 'or' separate the different food and make them different : "
              f"{initial_prompt_result}.")
    response = client.chat.completions.create(
        model="gemini-2.0-flash-exp",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return response.choices[0].message.content.split(", ")



def get_cooking_instructions_and_ingredients(initial_prompt, user_choice):
    prompt = (
        f"Based on the ingredient analysis: '{initial_prompt}', generate step-by-step instructions to make {user_choice}. "
        f"Also, suggest any additional ingredients needed to make this meal if the provided ingredients are insufficient."
    )

    # Send the image and prompt
    response = client.chat.completions.create(
        model="gemini-2.0-flash-exp",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Extract and clean the response
    full_response = response.choices[0].message.content


    return  full_response



def main(auto: bool):


    if auto:
        ingredient_analysis = auto_detect('img.png')

    else:
        ingredients_input = input("Enter ingredients separated by commas: ")
        ingredient_analysis = manual_prompt(ingredients_input)

    print(ingredient_analysis)
    food_suggestions = get_food_suggestions(ingredient_analysis)
    print(food_suggestions)

    user_choice = int(input("Enter the food you want to make: "))

    print("You chose: ", user_choice)

    cooking_instructions=get_cooking_instructions_and_ingredients(ingredient_analysis,user_choice)

    print(cooking_instructions)



if __name__ == '__main__':
    main(True)


