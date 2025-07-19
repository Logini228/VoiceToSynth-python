from pydub import AudioSegment

# Create a 5-second silent audio file
dummy_vocal = AudioSegment.silent(duration=5000)
dummy_vocal.export("vocal.wav", format="wav")
