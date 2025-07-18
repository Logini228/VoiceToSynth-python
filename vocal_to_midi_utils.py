import librosa
import mido
import numpy as np
from scipy.signal import medfilt

def audio_to_midi(input_wav, output_midi):
    y, sr = librosa.load(input_wav)
    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))

    # Get the best pitch from each frame
    notes = []
    for i, pitch in enumerate(f0):
        if voiced_flag[i] and voiced_probs[i] > 0.5:
            notes.append(librosa.hz_to_midi(pitch))
        else:
            notes.append(0)

    # Apply median filtering to smooth the notes
    notes = medfilt(notes, kernel_size=5)

    # Create a MIDI file
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)

    # Set tempo
    track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(120)))

    # Add notes to the track
    last_note = 0
    last_time = 0
    time_per_frame = librosa.get_duration(y=y, sr=sr) / len(f0)
    min_note_duration = 0.08  # seconds

    for i, note in enumerate(notes):
        time = i * time_per_frame
        note = int(round(note)) if note > 0 else 0

        if note != last_note:
            if last_note != 0:
                duration = time - last_time
                if duration >= min_note_duration:
                    delta_time = time - last_time
                    ticks = int(mido.second2tick(delta_time, mid.ticks_per_beat, mido.bpm2tempo(120)))
                    track.append(mido.Message('note_off', note=last_note, velocity=64, time=ticks))
                    last_time = time

            if note != 0:
                track.append(mido.Message('note_on', note=note, velocity=64, time=0))
            last_note = note

    # Add a final note_off for the last note
    if last_note != 0:
        duration = (len(notes) * time_per_frame) - last_time
        if duration >= min_note_duration:
            delta_time = (len(notes) * time_per_frame) - last_time
            ticks = int(mido.second2tick(delta_time, mid.ticks_per_beat, mido.bpm2tempo(120)))
            track.append(mido.Message('note_off', note=last_note, velocity=64, time=ticks))

    mid.save(output_midi)
    print(f"MIDI file saved to {output_midi}")
