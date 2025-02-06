import os
import argparse
import base64
import re
from openai import OpenAI  # Import the new OpenAI class

# Create a client using the API key from the environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def extract_code_block(text):
    """Extracts XML content from a response wrapped in a Markdown code block."""
    match = re.search(r"```xml\n(.*?)\n```", text, re.DOTALL)
    return match.group(1) if match else text  # Return the whole text if no match is found

def transcribe_image(image_path):
    try:
        # Read the image file and encode it to base64
        with open(image_path, 'rb') as image_file:
            image_bytes = image_file.read()
            img_b64_str = base64.b64encode(image_bytes).decode('utf-8')
            # Extract the file extension (e.g., "png", "jpg")
            img_ext = os.path.splitext(image_path)[1][1:].lower()

        # Construct the MIME type properly
        mime_type = f"image/{img_ext}"

        # Define the new prompt text
        prompt_text = "Transcribe this image to TEI P5 XML. Respond with only the XML in a code block."

        # Create the message following the new API format
        message = {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt_text},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{img_b64_str}"
                    }
                }
            ]
        }

        # Send the message to the API using the client instance
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[message],
        )

        # Extract and print the XML content from the response
        if response.choices and len(response.choices) > 0:
            message_content = response.choices[0].message.content
            xml_content = extract_code_block(message_content)
            print(xml_content)

    except Exception as e:
        print(f"Error processing image {image_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Transcribe an image into TEI XML using the OpenAI API."
    )
    parser.add_argument("image", nargs="?", help="Path to the image file")
    args = parser.parse_args()

    if args.image:
        transcribe_image(args.image)
    else:
        image_path = input("Please enter the path to the image file: ")
        transcribe_image(image_path)
