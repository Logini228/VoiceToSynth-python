import argparse
import json
from pydub import AudioSegment
from audio_utils import load_sound_library, analyze_vocal

def reconstruct_vocal(vocal_path, sound_library_path, output_wav_path, output_json_path):
    """
    Reconstructs a vocal recording using a sound library.
    """
    sound_library = load_sound_library(sound_library_path)
    if not sound_library:
        print(f"Error: Sound library not found or empty at {sound_library_path}")
        return

    analyzed_sounds = analyze_vocal(vocal_path, sound_library)

    reconstructed_audio = AudioSegment.empty()
    json_output = {}
    sound_index = 1

    for sound_info in analyzed_sounds:
        key = (sound_info["language"], sound_info["sound"], sound_info["duration"])
        if key in sound_library:
            reconstructed_audio += sound_library[key]
            json_output[str(sound_index)] = {
                "starttime": f"{int(sound_info['starttime'] // 3600):02}:{int((sound_info['starttime'] % 3600) // 60):02}:{sound_info['starttime'] % 60:02.0f}",
                "endtime": f"{int(sound_info['endtime'] // 3600):02}:{int((sound_info['endtime'] % 3600) // 60):02}:{sound_info['endtime'] % 60:02.0f}",
                "language": sound_info["language"],
                "sound": sound_info["sound"],
                "duration": str(sound_info["duration"])
            }
            sound_index += 1

    reconstructed_audio.export(output_wav_path, format="wav")

    with open(output_json_path, 'w') as f:
        json.dump(json_output, f, indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reconstruct a vocal recording using a sound library.")
    parser.add_argument("vocal_path", help="Path to the vocal.wav file.")
    parser.add_argument("sound_library", help="Name of the sound library to use (e.g., SynthV or Vocaloid).")
    args = parser.parse_args()

    output_wav_path = "reconstructed.wav"
    output_json_path = "reconstructed.json"

    reconstruct_vocal(args.vocal_path, args.sound_library, output_wav_path, output_json_path)
    print(f"Reconstructed audio saved to {output_wav_path}")
    print(f"Reconstruction details saved to {output_json_path}")
