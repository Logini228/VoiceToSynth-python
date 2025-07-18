import argparse
import os
from utils import isolate_vocals

def main():
    parser = argparse.ArgumentParser(description="Isolate vocals from a song.")
    parser.add_argument("song_path", help="Path to the song file.")
    parser.add_argument("instrumental_path", help="Path to the instrumental file.")
    parser.add_argument("output_path", help="Path to save the output vocal file.")
    args = parser.parse_args()

    output_path = args.output_path
    name, ext = os.path.splitext(output_path)
    counter = 1
    while os.path.exists(output_path):
        output_path = f"{name}{counter}{ext}"
        counter += 1

    isolate_vocals(args.song_path, args.instrumental_path, output_path)

if __name__ == "__main__":
    main()
