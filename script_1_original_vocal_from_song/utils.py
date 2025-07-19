from pydub import AudioSegment
import numpy as np
import os
import shutil
import torch
import torchaudio
from demucs.apply import apply_model
from demucs.pretrained import get_model

def isolate_vocals(song_path, output_path):
    """
    Isolates vocals from a song using Demucs.

    Args:
        song_path (str): Path to the song file.
        output_path (str): Path to save the output vocal file.
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = get_model(name='htdemucs_ft')
    model.to(device)
    model.eval()

    waveform, sample_rate = torchaudio.load(song_path)
    waveform = waveform.to(device)

    # Normalize the waveform.
    normalized_waveform = waveform / (waveform.std() + 1e-8)

    # The model expects a batch, so we add a dimension.
    batched_waveform = normalized_waveform.unsqueeze(0)

    # Separate the sources
    sources = apply_model(model, batched_waveform, device=device, progress=True)[0]

    # Find the vocal track.
    vocal_idx = model.sources.index('vocals')
    vocal_track_normalized = sources[vocal_idx]

    # Denormalize the output
    vocal_track = vocal_track_normalized * (waveform.std() + 1e-8)

    # torchaudio.save expects a 2D tensor (channels, samples)
    torchaudio.save(output_path, vocal_track.cpu(), sample_rate)

def compare_audio(file1_path, file2_path):
    """
    Compares two audio files and returns a similarity score.

    Args:
        file1_path (str): Path to the first audio file.
        file2_path (str): Path to the second audio file.

    Returns:
        float: Similarity score between the two audio files (0-100).
    """
    audio1 = AudioSegment.from_wav(file1_path)
    audio2 = AudioSegment.from_wav(file2_path)

    # Convert to mono for consistent comparison
    audio1 = audio1.set_channels(1)
    audio2 = audio2.set_channels(1)

    samples1 = np.array(audio1.get_array_of_samples())
    samples2 = np.array(audio2.get_array_of_samples())

    # Trim numpy arrays to same length
    min_len = min(len(samples1), len(samples2))
    samples1 = samples1[:min_len]
    samples2 = samples2[:min_len]

    # Calculate Mean Squared Error
    mse = np.mean((samples1.astype(np.float64) - samples2.astype(np.float64)) ** 2)

    # Use max possible value of the audio data type to normalize MSE
    try:
        # sample_width is in bytes
        max_val = 2**(audio1.sample_width * 8 - 1) - 1
        max_mse = float(max_val**2)
    except Exception:
        # Fallback for safety, assuming 16-bit audio
        max_mse = float((2**15 - 1)**2)

    if max_mse == 0:
        return 100.0 if mse == 0 else 0.0

    similarity = 100 * (1 - mse / max_mse)
    
    return max(0, similarity)