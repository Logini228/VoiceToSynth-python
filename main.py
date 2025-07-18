import argparse
import random
import os
from utils import isolate_vocals, compare_audio

def main():
    parser = argparse.ArgumentParser(description="Isolate vocals from a song.")
    parser.add_argument("song_path", help="Path to the song file.")
    parser.add_argument("instrumental_path", help="Path to the instrumental file.")
    parser.add_argument("output_path", help="Path to save the output vocal file.")
    parser.add_argument("comparison_path", help="Path to the comparison vocal file.")
    args = parser.parse_args()

    name, ext = os.path.splitext(args.output_path)
    random_number = random.randint(1000, 9999)
    output_path = f"{name}{random_number}{ext}"

    isolate_vocals(args.song_path, args.instrumental_path, output_path)

    similarity = compare_audio(output_path, args.comparison_path)
    print(f"Similarity score: {similarity}")

    # Clean up the generated file
    os.remove(output_path)

if __name__ == "__main__":
    main()
