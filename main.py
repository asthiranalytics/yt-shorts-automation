import os
from generate_script import generate_story
from upload import upload_to_youtube
from gtts import gTTS  # You can replace with ElevenLabs or DeepSeek TTS
import subprocess

def save_story_as_voice(text, filename="voice.mp3"):
    tts = gTTS(text)
    tts.save(filename)

def create_video():
    # 1. Generate story
    print("Generating story...")
    story = generate_story()
    with open("story.txt", "w", encoding="utf-8") as f:
        f.write(story)

    # 2. Convert story to voice
    print("Generating voiceover...")
    save_story_as_voice(story, "voice.mp3")

    # 3. Combine assets into final video
    print("Creating final video...")
    cmd = [
        "ffmpeg",
        "-y",
        "-i", "background.mp4",
        "-i", "music.mp3",
        "-i", "voice.mp3",
        "-filter_complex", "[0:v]scale=1080:1920,setsar=1[v]",
        "-map", "[v]",
        "-map", "2:a",  # voiceover
        "-map", "1:a",  # background music
        "-c:v", "libx264",
        "-c:a", "aac",
        "-shortest",
        "final_video.mp4"
    ]
    subprocess.run(cmd, check=True)

    print("Video created: final_video.mp4")
    return story

if __name__ == "__main__":
    story_text = create_video()
    title = story_text.split("\n")[0][:100]  # use first line as YouTube title
    print("Uploading video...")
    upload_to_youtube("final_video.mp4", title)
