import unittest
import sys
import os

# Add the parent directory to sys.path so we can import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app

class TestApp(unittest.TestCase):
    def test_import(self):
        self.assertTrue(hasattr(app, 'main'))

if __name__ == '__main__':
    unittest.main()
