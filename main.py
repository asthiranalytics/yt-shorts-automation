import openai
import moviepy.editor as mp
import os
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip, TextClip, concatenate_videoclips

# 1. Load prompt
with open("prompt.txt", "r") as f:
    prompt = f.read()

# 2. Generate story
openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
)
story = response['choices'][0]['message']['content']

# 3. Convert story to voice
tts = openai.audio.speech.create(
    model="tts-1",
    voice="shimmer",
    input=story
)
with open("voice.mp3", "wb") as out:
    out.write(tts.read())

# 4. Combine background, voice, music
background = VideoFileClip("background.mp4").subclip(0, 60)
voice = AudioFileClip("voice.mp3")
music = AudioFileClip("music.mp3").volumex(0.1)
final_audio = mp.CompositeAudioClip([voice, music.set_duration(voice.duration)])
background = background.set_audio(final_audio)

# 5. Export video
background.write_videofile("final.mp4", fps=30)

# 6. Upload to YouTube
from upload import upload_to_youtube
upload_to_youtube("final.mp4", story)
