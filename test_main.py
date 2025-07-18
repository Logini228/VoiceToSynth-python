import os
import unittest
from unittest.mock import patch, MagicMock
from main import main

class TestMain(unittest.TestCase):

    def setUp(self):
        # Create dummy files for testing
        with open("vocal.wav", "w") as f:
            f.write("dummy content")
        with open("vocal1.wav", "w") as f:
            f.write("dummy content")

    def tearDown(self):
        # Clean up dummy files
        if os.path.exists("vocal.wav"):
            os.remove("vocal.wav")
        if os.path.exists("vocal1.wav"):
            os.remove("vocal1.wav")
        if os.path.exists("vocal2.wav"):
            os.remove("vocal2.wav")

    @patch('utils.AudioSegment.from_wav')
    @patch('utils.isolate_vocals')
    def test_filename_increment(self, mock_isolate_vocals, mock_from_wav):
        # Mock the AudioSegment.from_wav to return a dummy AudioSegment
        mock_from_wav.return_value = MagicMock()

        # Run the main script with arguments that will cause it to create a new file
        main_args = ["main.py", "song.wav", "instr.wav", "vocal.wav"]
        with patch('sys.argv', main_args):
            main()

        # Check that isolate_vocals was called with the correct output path
        mock_isolate_vocals.assert_called_with("song.wav", "instr.wav", "vocal2.wav")

if __name__ == '__main__':
    unittest.main()
