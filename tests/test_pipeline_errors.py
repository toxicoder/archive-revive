import os
import shutil
import unittest
from main import main


class TestPipelineErrors(unittest.TestCase):

    def setUp(self):
        """Set up test directories and dummy files."""
        self.input_dir = 'test_input'
        self.output_dir = 'test_output'
        self.config_path = 'test_config.ini'

        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists(self.input_dir):
            shutil.rmtree(self.input_dir)
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
        if os.path.exists(self.config_path):
            os.remove(self.config_path)

    def test_pipeline_invalid_input_dir(self):
        """Test that the pipeline logs an error with an invalid input directory."""
        with self.assertLogs('root', level='ERROR') as cm:
            main('non_existent_dir', self.output_dir, self.config_path)
        self.assertIn("No such file or directory: 'non_existent_dir'", cm.output[0])

    def test_pipeline_invalid_config_file(self):
        """Test that the pipeline logs an error with an invalid config file."""
        import cv2
        import numpy as np
        dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.imwrite(os.path.join(self.input_dir, 'test_image.png'),
                    dummy_image)
        with open(self.config_path, 'w') as f:
            f.write('[OCR]\n')
            f.write('psm = not_an_integer\n')
        with self.assertLogs('root', level='ERROR') as cm:
            main(self.input_dir, self.output_dir, self.config_path)
        self.assertTrue(
            any("invalid literal for int() with base 10: 'not_an_integer'"
                in s for s in cm.output)
        )  # noqa: E501


if __name__ == '__main__':
    unittest.main()
