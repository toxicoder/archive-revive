import os
import shutil
import unittest
from main import main
from unittest.mock import patch


class TestPipelineWithPDF(unittest.TestCase):

    def setUp(self):
        self.input_dir = "test_input"
        self.output_dir = "test_output"
        self.config_path = "test_config.ini"
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        # Create a dummy config file
        with open(self.config_path, 'w') as f:
            f.write('[OCR]\n')
            f.write('PSM = 3\n')

    def tearDown(self):
        shutil.rmtree(self.input_dir)
        shutil.rmtree(self.output_dir)
        os.remove(self.config_path)

    @patch('src.generate_html.create_html_from_alto')
    @patch('src.normalize_rag.generate_rag_json')
    @patch('src.ocr.run_ocr')
    @patch('src.preprocess.preprocess_image')
    @patch('fitz.open')
    def test_pdf_processing(self, mock_fitz_open, mock_preprocess_image, mock_run_ocr, mock_generate_rag_json, mock_create_html_from_alto):
        # Mock the PDF processing
        mock_doc = unittest.mock.MagicMock()
        mock_page = unittest.mock.MagicMock()
        mock_fitz_open.return_value = mock_doc
        mock_doc.__len__.return_value = 1
        mock_doc.load_page.return_value = mock_page

        mock_page.get_pixmap.return_value.tobytes.return_value = b"dummy image"

        def preprocess_image_mock(image_path, output_path):
            with open(output_path, "w") as f:
                f.write("dummy preprocessed image")
            return output_path

        def run_ocr_mock(image_path, output_dir, psm):
            path = os.path.join(output_dir, "page_001.xml")
            with open(path, "w") as f:
                f.write("dummy xml")
            return path

        def generate_rag_json_mock(alto_path, output_json_path, config):
            with open(output_json_path, "w") as f:
                f.write("dummy json")
            return True

        def create_html_from_alto_mock(alto_path, output_html_path, image_dir_path, original_scan_path):
            with open(output_html_path, "w") as f:
                f.write("dummy html")
            return True

        mock_preprocess_image.side_effect = preprocess_image_mock
        mock_run_ocr.side_effect = run_ocr_mock
        mock_generate_rag_json.side_effect = generate_rag_json_mock
        mock_create_html_from_alto.side_effect = create_html_from_alto_mock

        # Create a dummy PDF file to trigger the PDF processing branch
        with open(os.path.join(self.input_dir, "dummy.pdf"), "w") as f:
            f.write("dummy content")

        main(self.input_dir, self.output_dir, self.config_path)

        # Check that the output directory for the PDF was created
        pdf_output_dir = os.path.join(self.output_dir, "dummy")
        self.assertTrue(os.path.isdir(pdf_output_dir))

        # Check that the page image was created
        page_image_path = os.path.join(pdf_output_dir, "page_001.png")
        self.assertTrue(os.path.isfile(page_image_path))

        # Check that the preprocessed image was created
        preprocessed_dir = os.path.join(pdf_output_dir, "preprocessed")
        preprocessed_image_path = os.path.join(
            preprocessed_dir, "page_001.png"
        )
        self.assertTrue(os.path.isfile(preprocessed_image_path))

        # Check that the OCR output was created
        ocr_dir = os.path.join(pdf_output_dir, "ocr")
        alto_xml_path = os.path.join(ocr_dir, "page_001.xml")
        self.assertTrue(os.path.isfile(alto_xml_path))

        # Check that the RAG output was created
        rag_dir = os.path.join(pdf_output_dir, "rag")
        rag_file_path = os.path.join(rag_dir, "page_001.json")
        self.assertTrue(os.path.isfile(rag_file_path))

        # Check that the HTML output was created
        html_dir = os.path.join(pdf_output_dir, "html")
        html_file_path = os.path.join(html_dir, "page_001.html")
        self.assertTrue(os.path.isfile(html_file_path))


if __name__ == '__main__':
    unittest.main()
