from pydub import AudioSegment

def isolate_vocals(song_path, instrumental_path, output_path):
    """
    Isolates vocals from a song by subtracting the instrumental track.

    Args:
        song_path (str): Path to the song file.
        instrumental_path (str): Path to the instrumental file.
        output_path (str): Path to save the output vocal file.
    """
    song = AudioSegment.from_wav(song_path)
    instrumental = AudioSegment.from_wav(instrumental_path)

    vocals = song.overlay(instrumental, position=0, gain_during_overlay=-1.0)

    vocals.export(output_path, format="wav")
