import os
import shutil
import unittest
from main import main

class TestPipelineWithPDF(unittest.TestCase):

    def setUp(self):
        self.input_dir = "tests/input"
        self.output_dir = "tests/output"
        self.config_path = "tests/config.ini"
        os.makedirs(self.input_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)
        # Create a dummy PDF
        import fitz
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((50, 72), "Hello, world!")
        doc.save(os.path.join(self.input_dir, "dummy.pdf"))
        doc.close()

    def tearDown(self):
        shutil.rmtree(self.input_dir)
        shutil.rmtree(self.output_dir)

    def test_pdf_processing(self):
        main(self.input_dir, self.output_dir, self.config_path)

        # Check that the output directory for the PDF was created
        pdf_output_dir = os.path.join(self.output_dir, "dummy")
        self.assertTrue(os.path.isdir(pdf_output_dir))

        # Check that the page image was created
        page_image_path = os.path.join(pdf_output_dir, "page_001.png")
        self.assertTrue(os.path.isfile(page_image_path))

        # Check that the preprocessed image was created
        preprocessed_dir = os.path.join(pdf_output_dir, "preprocessed")
        preprocessed_image_path = os.path.join(preprocessed_dir, "page_001.png")
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
