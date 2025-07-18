import soundfile as sf
import numpy as np
import librosa

def isolate_vocals(song_path, instrumental_path, output_path):
    """
    Isolates vocals from a song by subtracting the instrumental track.

    Args:
        song_path (str): Path to the song file.
        instrumental_path (str): Path to the instrumental file.
        output_path (str): Path to save the output vocal file.
    """
    song, sr = sf.read(song_path)
    instrumental, _ = sf.read(instrumental_path)

    # Make sure the arrays have the same length
    min_len = min(len(song), len(instrumental))
    song = song[:min_len]
    instrumental = instrumental[:min_len]

    # Subtract the samples
    vocals = song - instrumental

    # Write the output file
    sf.write(output_path, vocals, sr)


def compare_audio(file1, file2):
    """
    Compares two audio files and returns the root-mean-square error.

    Args:
        file1 (str): Path to the first audio file.
        file2 (str): Path to the second audio file.

    Returns:
        float: The root-mean-square error.
    """
    y1, sr1 = librosa.load(file1)
    y2, sr2 = librosa.load(file2)

    # Make sure the arrays have the same length
    min_len = min(len(y1), len(y2))
    y1 = y1[:min_len]
    y2 = y2[:min_len]

    rmse = np.sqrt(np.mean((y1 - y2)**2))

    return rmse
