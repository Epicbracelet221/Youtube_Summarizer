import os
from pytube import YouTube
from pydub import AudioSegment
import speech_recognition as sr
from transformers import pipeline

# 1. Download YouTube Video
def download_video(url):
    print("Downloading the video...")
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension="mp4").first()
    video_path = stream.download(filename="video.mp4")
    print("Video downloaded.")
    return video_path

# 2. Extract Audio from the Video (using pydub)
def extract_audio_from_video(video_path):
    print("Extracting audio...")
    video = AudioSegment.from_file(video_path, format="mp4")  # Load video as an audio file
    audio_path = "audio.wav"
    video.export(audio_path, format="wav")  # Export the audio as a .wav file
    print("Audio extracted.")
    return audio_path

# 3. Convert Audio to Text using Speech Recognition
def audio_to_text(audio_path):
    print("Converting audio to text...")
    recognizer = sr.Recognizer()
    audio = sr.AudioFile(audio_path)
    with audio as source:
        audio_data = recognizer.record(source)
    
    text = recognizer.recognize_google(audio_data)
    print("Audio converted to text.")
    return text

# 4. Summarize the Text using Hugging Face AI model
def summarize_text(text):
    print("Summarizing text...")
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']

# Main function to tie everything together
def summarize_youtube_video(url):
    # Step 1: Download video from YouTube
    video_path = download_video(url)
    
    # Step 2: Extract audio from video using pydub
    audio_path = extract_audio_from_video(video_path)
    
    # Step 3: Convert audio to text
    text = audio_to_text(audio_path)
    
    # Step 4: Summarize the text
    summary = summarize_text(text)
    
    # Clean up: Remove the downloaded files
    os.remove(video_path)
    os.remove(audio_path)
    
    # Print the summary
    print("Summary of the video:")
    print(summary)

# Test the function with a YouTube video URL
video_url = "https://youtu.be/lYfsaSHQTCc"  # Example URL
summarize_youtube_video(video_url)

