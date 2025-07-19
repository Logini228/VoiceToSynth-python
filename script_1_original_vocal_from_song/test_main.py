import os
import unittest
from unittest.mock import patch
from pydub import AudioSegment
from pydub.generators import Sine
from main import main
from utils import isolate_vocals, compare_audio

class TestMain(unittest.TestCase):

    def setUp(self):
        self.song_path = "song.wav"
        self.instr_path = "instr.wav"
        self.vocal_path = "vocal.wav"
        self.output_path = "output.wav"
        self.file_paths = [self.song_path, self.instr_path, self.vocal_path, self.output_path]

        # Create a sine wave for the vocal part
        vocal_part = Sine(440).to_audio_segment(duration=1000, volume=-10) # 1 second sine wave

        # Create a silent instrumental part
        instr_part = AudioSegment.silent(duration=1000)

        # The "song" is the vocal and instrumental combined
        song = instr_part.overlay(vocal_part)

        # Export the files for the test
        song.export(self.song_path, format="wav")
        instr_part.export(self.instr_path, format="wav")
        vocal_part.export(self.vocal_path, format="wav")


    def tearDown(self):
        # Clean up dummy files
        for path in self.file_paths:
            if os.path.exists(path):
                os.remove(path)

    def test_vocal_isolation_and_comparison(self):
        isolate_vocals(self.song_path, self.instr_path, self.output_path)
        self.assertTrue(os.path.exists(self.output_path))
        similarity = compare_audio(self.output_path, self.vocal_path)
        # The phase inversion should result in a very similar file.
        self.assertGreater(similarity, 95)

    @patch('sys.argv', ['main.py', 'song.wav', 'instr.wav', 'output.wav', 'vocal.wav'])
    @patch('builtins.print')
    def test_main_script_execution(self, mock_print):
        main()
        self.assertTrue(os.path.exists(self.output_path))
        # Check that print was called, which means the similarity was calculated.
        mock_print.assert_called()

if __name__ == '__main__':
    unittest.main()
