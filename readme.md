
# TEI P5 XML Image Transcription using OpenAI

This repository contains a Python script that uses OpenAI's GPT-4o API to transcribe text from an image into TEI P5 XML format. The script processes an input image, extracts its content using AI, and returns the transcribed text formatted as TEI XML.

## Features

- Converts handwritten or printed text in images into **TEI P5 XML**.
- Uses **OpenAI's GPT-4o-mini** model for transcription.
- Automatically encodes images to **Base64** before sending to the API.
- Extracts and prints only the **XML response** from the model.
- Supports various image formats (PNG, JPG, JPEG).

## Prerequisites

Before using this script, ensure you have:

1. Python **3.7+** installed.
2. An **OpenAI API key**.
3. Required Python packages installed (see **Installation** below).

## Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/kmpenner/AI.git
   cd AI
   ```

2. Install dependencies:
   ```sh
   pip install openai argparse
   ```

3. Set up your OpenAI API key as an environment variable:
   - On **Windows** (PowerShell):
     ```powershell
     $env:OPENAI_API_KEY="your-api-key"
     ```
   - On **macOS/Linux** (bash):
     ```sh
     export OPENAI_API_KEY="your-api-key"
     ```

## Usage

Run the script by providing the **path to an image file**:

```sh
python transcribe_image.py path/to/your/image.png
```

Alternatively, if no image is provided, the script will prompt you for one.

### Example:

```sh
python transcribe_image.py C:\Users\JohnDoe\Documents\letter.png
```

### Expected Output:

The script will return the transcribed text in TEI P5 XML format:

```xml
<TEI>
    <text>
        <body>
            <p>Dear sir:</p>
            <p>Your letter of inquiry with its interesting enclosures is before me...</p>
        </body>
    </text>
</TEI>
```

## How It Works

1. **Loads an image** from the specified path.
2. **Encodes** the image in Base64 format.
3. **Sends** the encoded image to OpenAI with the prompt:
   > "Transcribe this image to TEI P5 XML. Respond with only the XML in a code block."
4. **Receives a response** from OpenAI.
5. **Extracts and prints only the XML** content inside the response.

## Troubleshooting

- **Invalid MIME type error:** Ensure your image is in **PNG or JPG** format.
- **API key errors:** Double-check that your API key is correctly set.
- **No XML output:** The image may not contain readable text, or the model may have misinterpreted the request.

## License

This project is licensed under the MIT License. See `LICENSE` for more details.

## Contributing

Pull requests are welcome! If you find issues or want to add features, feel free to submit a PR.

---

⭐ **If you find this useful, give it a star on GitHub!**