import os
import openai
import json
from upload import upload_to_youtube

# 1. Load prompt
with open("prompt.txt") as f:
    prompt = f.read()

# 2. Generate story
openai.api_key = os.environ["OPENAI_API_KEY"]
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
story = response['choices'][0]['message']['content']

# 3. Convert story to voice
tts = openai.audio.speech.create(
    model="tts-1",
    voice="shimmer",
    input=story
)
with open("voice.mp3", "wb") as f:
    f.write(tts.read())

# 4. Create video with background, voice, music
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
bg = VideoFileClip("background.mp4").subclip(0, 60)
voice = AudioFileClip("voice.mp3")
music = AudioFileClip("music.mp3").volumex(0.1)
audio = CompositeAudioClip([voice, music.set_duration(voice.duration)])
video = bg.set_audio(audio)
video.write_videofile("final.mp4", fps=30)

# 5. Loop through tokens and upload to each channel
token_dir = "./tokens"
for filename in os.listdir(token_dir):
    if filename.endswith(".json"):
        token_path = os.path.join(token_dir, filename)
        try:
            upload_to_youtube("final.mp4", story, token_path)
        except Exception as e:
            print(f"❌ Upload failed for {filename}: {e}")
