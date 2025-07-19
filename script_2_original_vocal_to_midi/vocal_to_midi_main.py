import argparse
from vocal_to_midi_utils import audio_to_midi

def main():
    parser = argparse.ArgumentParser(description='Convert a vocal WAV file to a MIDI file.')
    parser.add_argument('input_wav', help='Input WAV file path')
    parser.add_argument('output_midi', help='Output MIDI file path')
    args = parser.parse_args()

    audio_to_midi(args.input_wav, args.output_midi)

if __name__ == '__main__':
    main()
