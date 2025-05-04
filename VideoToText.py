import speech_recognition as sr
from moviepy.editor import VideoFileClip

def VidToImg(VideoFile):
# Open the video file and extract the audio
    clip = VideoFileClip(VideoFile)
    audio = clip.audio

# Save the audio to a file
    audio.write_audiofile("audio.wav")

# Create a speech recognition object
    r = sr.Recognizer()

# Open the audio file and transcribe the audio
    with sr.AudioFile("audio.wav") as source:
        audio = r.record(source)
        text = print(r.recognize_google(audio))
        try:
            print("Transcript:", r.recognize_google(audio))
            return text
        except sr.exceptions.UnknownValueError:
            return "Google Speech Recognition could not understand your audio"
        except sr.exceptions.RequestError as e:
            return "Could not request results from Google Speech Recognition service; {0}".format(e)

