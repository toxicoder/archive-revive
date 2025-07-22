import unittest
from unittest.mock import patch
import os
from src.generate_html import create_html_from_alto
from lxml import etree


class TestGenerateHtmlErrors(unittest.TestCase):

    def setUp(self):
        self.alto_path = "test.xml"
        self.output_html_path = "test.html"
        self.image_dir_path = "test_images"
        self.original_scan_path = "test_scan.png"
        # Create a dummy alto file
        with open(self.alto_path, "w") as f:
            f.write("<alto></alto>")
        # Create a dummy image
        import numpy as np
        import cv2
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.imwrite(self.original_scan_path, img)

    def tearDown(self):
        if os.path.exists(self.alto_path):
            os.remove(self.alto_path)
        if os.path.exists(self.output_html_path):
            os.remove(self.output_html_path)
        if os.path.exists(self.original_scan_path):
            os.remove(self.original_scan_path)
        if os.path.exists(self.image_dir_path):
            import shutil
            shutil.rmtree(self.image_dir_path)

    @patch('lxml.etree.parse', side_effect=etree.ParseError("Test error", None, 1, 1))
    def test_create_html_from_alto_error(self, mock_parse):
        """Test that create_html_from_alto returns False on error."""
        result = create_html_from_alto(
            self.alto_path, self.output_html_path, self.image_dir_path,
            self.original_scan_path
        )
        self.assertFalse(result)

    @patch('cv2.imread', return_value=None)
    def test_create_html_from_alto_no_image(self, mock_imread):
        """
        Test that create_html_from_alto returns False when the image
        cannot be read.
        """
        result = create_html_from_alto(
            self.alto_path, self.output_html_path, self.image_dir_path,
            self.original_scan_path
        )
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
