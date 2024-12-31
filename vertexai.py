
import base64
from openai import OpenAI

client = OpenAI(
    api_key="AIzaSyCMV1RzXC62lSyDxqcqlky-p1UzHqH2XEw",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Getting the base64 string
base64_image = encode_image("img_3 (1).jpg")

response = client.chat.completions.create(
  model="gemini-2.0-flash-exp",
  messages=[
    {
      "role": "user",
      "content": [



        {
          "type": "text",
          "text": "You are given an image. Detect if it is already cooked food or an ingredient. "
        "If it is food, tell me what ingredients are used to make it. If it is an ingredient, "
        "tell me what food can be made with it. Provide a YouTube link to make the suggested food, "
        "and if needed, a Google link. Include directions for making the food."



        },
        {
          "type": "image_url",
          "image_url": {
            "url":  f"data:image/jpeg;base64,{base64_image}"
          },
        },
      ],
    }
  ],
)

print(response.choices[0])

# response.choices[0].message["content"]