import unittest
import os
from run_ocr import perform_ocr
from PIL import Image

class TestPerformOCR(unittest.TestCase):

    def setUp(self):
        """Set up a dummy image for testing."""
        self.test_image_path = "test_image.png"
        self.output_alto_path = "test_output.xml"
        # Create a simple black image
        img = Image.new('RGB', (100, 100), color = 'black')
        img.save(self.test_image_path)

    def tearDown(self):
        """Clean up the created files."""
        if os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)
        if os.path.exists(self.output_alto_path):
            os.remove(self.output_alto_path)
        if os.path.exists("test_output.xml"):
            os.remove("test_output.xml")


    def test_perform_ocr_success(self):
        """Test that perform_ocr runs successfully and creates the output file."""
        # Assuming Tesseract is installed and in the PATH
        success = perform_ocr(self.test_image_path, self.output_alto_path)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(self.output_alto_path))

if __name__ == '__main__':
    unittest.main()
