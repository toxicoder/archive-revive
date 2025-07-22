import unittest
from unittest.mock import patch, MagicMock
import os
from src.ocr import run_ocr
import pytesseract
from PIL import Image


class TestRunOCR(unittest.TestCase):

    def setUp(self):
        self.image_path = "test_image.png"
        self.output_dir = "test_output"
        os.makedirs(self.output_dir, exist_ok=True)
        # Create a dummy image
        img = Image.new('RGB', (100, 100), color='black')
        img.save(self.image_path)

    def tearDown(self):
        if os.path.exists(self.image_path):
            os.remove(self.image_path)
        if os.path.exists(self.output_dir):
            import shutil
            shutil.rmtree(self.output_dir)

    @patch('pytesseract.image_to_alto_xml', return_value=b"<xml></xml>")
    def test_run_ocr_success(self, mock_image_to_alto_xml):
        """Test the successful execution of run_ocr."""
        alto_path = run_ocr(self.image_path, self.output_dir, 3)
        self.assertTrue(os.path.exists(alto_path))
        with open(alto_path, 'rb') as f:
            self.assertEqual(f.read(), b"<xml></xml>")

    @patch('pytesseract.image_to_alto_xml',
           side_effect=pytesseract.TesseractNotFoundError)
    def test_run_ocr_tesseract_not_found(self, mock_image_to_alto_xml):
        """
        Test that run_ocr raises TesseractNotFoundError when Tesseract
        is not found.
        """
        with self.assertRaises(pytesseract.TesseractNotFoundError):
            run_ocr(self.image_path, self.output_dir, 3)

    @patch('pytesseract.image_to_alto_xml',
           side_effect=ValueError("Test error"))
    def test_run_ocr_value_error(self, mock_image_to_alto_xml):
        """Test that run_ocr raises a ValueError."""
        with self.assertRaises(ValueError):
            run_ocr(self.image_path, self.output_dir, 3)

    @patch('pytesseract.image_to_alto_xml',
           side_effect=Exception("Test error"))
    def test_run_ocr_general_exception(self, mock_image_to_alto_xml):
        """Test that run_ocr raises a general exception."""
        with self.assertRaises(Exception):
            run_ocr(self.image_path, self.output_dir, 3)


if __name__ == '__main__':
    unittest.main()
