import os
import shutil
import unittest
from unittest.mock import patch, MagicMock
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
            f.write('[Metadata]\n')
            f.write('PublicationDate = 2024-01-01\n')
            f.write('NewspaperTitle = The Test Times\n')

    def tearDown(self):
        """Clean up after tests."""
        shutil.rmtree(self.input_dir)
        shutil.rmtree(self.output_dir)
        os.remove(self.config_path)

    @patch('shutil.copy')
    @patch('src.generate_html.create_html_from_alto', return_value=True)
    @patch('src.normalize_rag.generate_rag_json', return_value=True)
    @patch('src.ocr.run_ocr')
    @patch('src.preprocess.preprocess_image')
    def test_pipeline_creates_output_files(self, mock_preprocess_image, mock_run_ocr, mock_generate_rag_json, mock_create_html_from_alto, mock_shutil_copy):
        """Test that the pipeline runs and creates expected output files."""
        # Configure mocks
        mock_preprocess_image.return_value = os.path.join(self.output_dir, 'test_image', 'preprocessed', 'test_image.png')
        mock_run_ocr.return_value = os.path.join(self.output_dir, 'test_image', 'ocr', 'test_image.xml')

        # Create dummy output files
        os.makedirs(os.path.join(self.output_dir, 'test_image', 'preprocessed'), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, 'test_image', 'ocr'), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, 'test_image', 'rag'), exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, 'test_image', 'html', 'images'), exist_ok=True)

        with open(mock_preprocess_image.return_value, 'w') as f:
            f.write('')
        with open(mock_run_ocr.return_value, 'w') as f:
            f.write('<xml></xml>')

        main(self.input_dir, self.output_dir, self.config_path)

        # Check for output directories
        image_output_dir = os.path.join(self.output_dir, 'test_image')
        self.assertTrue(os.path.isdir(os.path.join(self.output_dir, 'logs')))
        self.assertTrue(os.path.isdir(os.path.join(image_output_dir, 'preprocessed')))
        self.assertTrue(os.path.isdir(os.path.join(image_output_dir, 'ocr')))
        self.assertTrue(os.path.isdir(os.path.join(image_output_dir, 'rag')))
        self.assertTrue(os.path.isdir(os.path.join(image_output_dir, 'html')))

        # Check that mocks were called
        mock_preprocess_image.assert_called_once()
        mock_run_ocr.assert_called_once()
        mock_generate_rag_json.assert_called_once()
        mock_create_html_from_alto.assert_called_once()


if __name__ == '__main__':
    unittest.main()
