import argparse
from utils import isolate_vocals, compare_audio

def main():
    parser = argparse.ArgumentParser(description="Isolate vocals from a song.")
    parser.add_argument("song_path", help="Path to the song file.")
    parser.add_argument("output_path", help="Path to save the output vocal file.")
    parser.add_argument("comparison_path", help="Path to the comparison vocal file.")
    args = parser.parse_args()

    isolate_vocals(args.song_path, args.output_path)

    similarity = compare_audio(args.output_path, args.comparison_path)
    print(f"Similarity score: {similarity:.2f}%")

if __name__ == "__main__":
    main()