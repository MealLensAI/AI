import base64
import google.generativeai as genai

# Configure the Gemini AI API with your API key
API_KEY = "AIzaSyCMV1RzXC62lSyDxqcqlky-p1UzHqH2XEw"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Function to encode an image into base64
def encode_image(image_path):
    """
    Encodes the given image file into a base64 string.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Base64-encoded image string.
    """
    try:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_image
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None

# Set up the model configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the generative model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

# Function to create and manage a chat session
def start_chat_with_gemini(image_path, user_message):
    """
    Starts a chat session with Gemini AI using a provided local image and user message.

    Args:
        image_path (str): Path to the local image file.
        user_message (str): User's text input for the AI.

    Returns:
        str: The AI's response text.
    """
    # Encode the image
    encoded_image = encode_image(image_path)
    if not encoded_image:
        return "Failed to encode the image. Please check the file path and try again."

    # Create a chat session with the local image
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    {"mime_type": "image/png", "inline_data": encoded_image},
                    {"text": user_message},
                ],
            }
        ]
    )

    # Send a follow-up message to the chat session (optional)
    response = chat_session.send_message(user_message)

    # Return the response text
    return response.text

# Example usage
if __name__ == "__main__":
    image_path = "img.png"  # Replace with the path to your local image
    user_message = (
        "You are given an image. Detect if it is already cooked food or an ingredient. "
        "If it is food, tell me what ingredients are used to make it. If it is an ingredient, "
        "tell me what food can be made with it. Provide a YouTube link to make the suggested food, "
        "and if needed, a Google link. Include directions for making the food."
    )

    # Start the chat and print the response
    response = start_chat_with_gemini(image_path, user_message)
    print("AI Response:\n", response)
