# narrator

## Description
Narrator is a Python project that combines the power of [ChatGPT](https://chat.openai.com/auth/login) and [ElevenLabs](https://elevenlabs.io/) to provide narration for videos with a specific voice. Imagine having a video of a day at the office narrated by the iconic voice of [David Attenborough](https://en.wikipedia.org/wiki/David_Attenborough). This tool brings that possibility to life, allowing for creative and engaging video presentations.

## Set Up
### Prerequisites
- Ensure you have Python3.x installed on your system
- An account with OpenAI and ElevenLabs is required to access their APIs

### Installation
1. **Install FFmpeg:** 
[FFmpeg](https://ffmpeg.org/) is crucial for processing video and audio files. Install it using the following commands:
```sh
sudo apt update
sudo apt install ffmpeg
```
2. **Set Up a Virtual Environment (Recommended):**
It's best practice to use a virtual environment for Python projects. This keeps dependencies organized and separate from your global Python installation. To set up and activate a virtual environment:
```sh
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
```
3. **Clone the Repository and Install Dependencies:**
After setting up your virtual environment, clone this repository and install the required dependencies:
```sh
git clone <repository-url>
cd narrator
pip install -r requirements.txt
```
4. **Configure API Keys:**
You'll need to set up environment variables for your [OpenAI](https://beta.openai.com/) and [ElevenLabs](https://elevenlabs.io) API keys. Additionally, identify the voice ID you want to use from ElevenLabs:
```sh
export OPENAI_API_KEY='your_openai_api_key_here'
export ELEVENLABS_API_KEY='your_elevenlabs_api_key_here'
export ELEVENLABS_VOICE_ID='your_elevenlabs_voice_id_here'
```
To find a new voice ID, utilize ElevenLabs' [Get Voices](https://elevenlabs.io/docs/api-reference/voices) API or select a voice directly from the VoiceLab tab on their platform.

## Source
[cbh123 narrator](https://github.com/cbh123/narrator)



