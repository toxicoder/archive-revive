import os
import shutil
import unittest
import cv2
import numpy as np
from main import main


class TestPipeline(unittest.TestCase):

    def setUp(self):
        """Set up test directories and dummy files."""
        self.input_dir = 'test_input'
        self.output_dir = 'test_output'
        self.config_path = 'test_config.ini'

        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

        # Create a dummy image file using OpenCV
        dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.imwrite(os.path.join(self.input_dir, 'test_image.png'),
                    dummy_image)

        # Create a dummy config file
        with open(self.config_path, 'w') as f:
            f.write('[OCR]\n')
            f.write('PSM = 3\n')

    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.input_dir)
        shutil.rmtree(self.output_dir)
        os.remove(self.config_path)

    def test_pipeline_creates_output_files(self):
        """Test that the pipeline runs and creates expected output files."""
        main(self.input_dir, self.output_dir, self.config_path)

        # Check for output directories
        image_output_dir = os.path.join(self.output_dir, 'test_image')
        self.assertTrue(os.path.isdir(os.path.join(self.output_dir, 'logs')))
        self.assertTrue(
            os.path.isdir(os.path.join(image_output_dir, 'preprocessed'))
        )
        self.assertTrue(os.path.isdir(os.path.join(image_output_dir, 'ocr')))
        self.assertTrue(os.path.isdir(os.path.join(image_output_dir, 'rag')))
        self.assertTrue(os.path.isdir(os.path.join(image_output_dir, 'html')))

        # Check for output files
        log_file = os.path.join(self.output_dir, 'logs', 'pipeline.log')
        preprocessed_file = os.path.join(
            image_output_dir, 'preprocessed', 'test_image.png'
        )
        ocr_file = os.path.join(image_output_dir, 'ocr', 'test_image.xml')
        rag_file = os.path.join(image_output_dir, 'rag', 'test_image.json')
        html_file = os.path.join(image_output_dir, 'html', 'test_image.html')

        self.assertTrue(os.path.exists(log_file))
        self.assertTrue(os.path.exists(preprocessed_file))
        self.assertTrue(os.path.exists(ocr_file))
        self.assertTrue(os.path.exists(rag_file))
        self.assertTrue(os.path.exists(html_file))


if __name__ == '__main__':
    unittest.main()
