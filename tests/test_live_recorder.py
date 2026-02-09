import unittest
from unittest.mock import MagicMock
import os
import time
from src.data_downloader import LiveRecorder

class TestLiveRecorder(unittest.TestCase):
    def setUp(self):
        self.filename = "test_live_data.csv"
        self.recorder = LiveRecorder("dummy_token", self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_recording(self):
        # Mock _fetch_snapshot
        self.recorder._fetch_snapshot = MagicMock(return_value={'best_bid': 0.5, 'best_ask': 0.6})

        # Run for 2 seconds, interval 1 second
        self.recorder.start_recording(duration_seconds=2.5, interval_seconds=1)

        # Check if file exists and has content
        self.assertTrue(os.path.exists(self.filename))
        with open(self.filename, 'r') as f:
            lines = f.readlines()
            self.assertGreater(len(lines), 1) # Header + at least 1 row
            self.assertEqual(lines[0].strip(), "timestamp,best_bid,best_ask")

            # Check data row
            data_parts = lines[1].strip().split(',')
            self.assertEqual(data_parts[1], "0.5")
            self.assertEqual(data_parts[2], "0.6")

if __name__ == '__main__':
    unittest.main()
