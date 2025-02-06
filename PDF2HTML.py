import os
import base64
import requests
import argparse
from pdf2image import convert_from_path

# Function to load API key from a file
def load_api_key(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# Function to encode the image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

# Function to send image to OpenAI GPT-4 vision API and retrieve HTML
def image_to_html(base64_image, api_key):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Convert this image to HTML. Respond with only the HTML."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 3000  # Adjust as needed
    }

    response = requests.post(url, headers=headers, json=payload)
    response_data = response.json()
    
    # Adjust based on the actual response structure
    return response_data['choices'][0]['message']['content']

# Function to convert PDF to images and process them
def convert_pdf_to_html(pdf_path, output_html_path, api_key):
    output_folder = "pdf_images"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Step 1: Convert PDF pages to images
    images = convert_from_path(pdf_path)
    combined_html = ""
    
    # Step 2: Process each image
    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"page_{i + 1}.png")
        image.save(image_path, "PNG")
        
        # Step 3: Convert image to base64 and get HTML
        print(f"Processing page {i + 1}...")
        base64_image = encode_image(image_path)
        html_content = image_to_html(base64_image, api_key)
        
        # Step 4: Combine the HTML output
        combined_html += html_content + "\n"
    
    # Step 5: Write combined HTML to output file
    with open(output_html_path, "w", encoding="utf-8") as html_file:
        html_file.write(combined_html)
    
    print(f"HTML output saved to {output_html_path}")

# Main function to handle command-line arguments
def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Convert PDF to HTML using OpenAI Vision API.')
    parser.add_argument('input_pdf', type=str, help='Path to the input PDF file')
    parser.add_argument('output_html', type=str, help='Path to the output HTML file')
    parser.add_argument('--api_key_file', type=str, default=r'P:\openai-api.key.txt', help='Path to the OpenAI API key file')

    # Parse the arguments
    args = parser.parse_args()

    # Load the API key
    api_key = load_api_key(args.api_key_file)

    # Convert the PDF to HTML
    convert_pdf_to_html(args.input_pdf, args.output_html, api_key)

if __name__ == "__main__":
    main()
