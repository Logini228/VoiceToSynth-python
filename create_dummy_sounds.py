from pydub import AudioSegment
import os

def create_dummy_sound(path, duration_ms):
    sound = AudioSegment.silent(duration=duration_ms)
    sound.export(path, format="wav")

# Create SynthV sounds
synthv_path = "SynthV"
os.makedirs(synthv_path, exist_ok=True)
create_dummy_sound(os.path.join(synthv_path, "spanish-la-half.wav"), 500)
create_dummy_sound(os.path.join(synthv_path, "spanish-la-quarter.wav"), 250)

# Create Vocaloid sounds
vocaloid_path = "Vocaloid"
os.makedirs(vocaloid_path, exist_ok=True)
create_dummy_sound(os.path.join(vocaloid_path, "english-oh-half.wav"), 500)
create_dummy_sound(os.path.join(vocaloid_path, "english-oh-quarter.wav"), 250)
