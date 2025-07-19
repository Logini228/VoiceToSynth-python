import pretty_midi
import sys
import numpy as np

def compare_midi_files(file1, file2):
    midi1 = pretty_midi.PrettyMIDI(file1)
    midi2 = pretty_midi.PrettyMIDI(file2)

    # Get the piano roll representations of the MIDI files
    pr1 = midi1.get_piano_roll(fs=100)
    pr2 = midi2.get_piano_roll(fs=100)

    # Pad the shorter piano roll to match the length of the longer one
    if pr1.shape[1] < pr2.shape[1]:
        pr1 = np.pad(pr1, ((0, 0), (0, pr2.shape[1] - pr1.shape[1])), 'constant')
    elif pr2.shape[1] < pr1.shape[1]:
        pr2 = np.pad(pr2, ((0, 0), (0, pr1.shape[1] - pr2.shape[1])), 'constant')

    # Calculate the similarity
    similarity = np.sum(pr1 == pr2) / pr1.size
    print(f"Similarity: {similarity:.2f}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python compare_midi.py <file1.mid> <file2.mid>")
        sys.exit(1)

    compare_midi_files(sys.argv[1], sys.argv[2])
