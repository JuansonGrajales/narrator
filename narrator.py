import os
import base64
import time
import simpleaudio as sa
import errno
from elevenlabs import generate, play, set_api_key, voices
from dotenv import load_dotenv
from openai import OpenAI
import io
from PIL import Image

# Load the .env file and set API keys
load_dotenv()
# defaults to getting the key using os.environ.get("OPENAI_API_KEY")
# https://platform.openai.com/docs/quickstart?context=python
client = OpenAI()
set_api_key(os.getenv("ELEVENLABS_API_KEY"))

def encode_image(frame):
    """Encode the image at the given path to base64."""
    try:
        # Convert PIL image to bytes
        img_buffer = io.BytesIO()
        frame.save(img_buffer, format="JPEG")
        byte_data = img_buffer.getvalue()
        return base64.b64encode(byte_data).decode("utf-8")
    except IOError as e:
        if e.errno != errno.EACCES:
            raise
        time.sleep(0.1)  # Wait and try again if the file is temporarily inaccessible

def play_audio(audio):
    """Play the given audio content."""
    unique_id = base64.urlsafe_b64encode(os.urandom(30)).decode("utf-8").rstrip("=")
    dir_path = os.path.join("narration", unique_id)
    os.makedirs(dir_path, exist_ok=True)
    file_path = os.path.join(dir_path, "audio.wav")

    with open(file_path, "wb") as f:
        f.write(audio)
    
    play(audio)

def generate_new_line(base64_image):
    """Generate a new line for the chat with the image."""
    return {
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe the image"},
            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"}
        ]
    }

def analyze_image(frame):
    """Analyze the image and narrate it."""
    base64_image = encode_image(frame)
    script = [
        {
            "role": "system",
            "content": 
            """
            You are Sir David Attenborough. Narrate the picture of the human as if it is a nature documentary.
            Make it snarky and funny. Don't repeat yourself. Make it short. If I do anything remotely interesting, make a big deal about it!
            """
        },
        generate_new_line(base64_image)
    ]

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=script,
        max_tokens=500
    )

    analysis = response.choices[0].message.content
    return analysis

def narrate_frame(frame):
    """The main function to narrate a frame given its path."""
    print("David is watching...")
    analysis = analyze_image(frame)
    print("David says: ", analysis)
    # Generate audio from analysis and play it
    audio_content = generate(analysis, voice=os.getenv("ELEVENLABS_VOICE_ID"))
    play_audio(audio_content)
