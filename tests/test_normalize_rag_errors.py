import unittest
from unittest.mock import patch, mock_open
import os
from src.normalize_rag import generate_rag_json
from lxml import etree

class TestNormalizeRagErrors(unittest.TestCase):

    def setUp(self):
        self.alto_path = "test.xml"
        self.output_json_path = "test.json"
        self.config = {"publication_date": "2024-07-21", "newspaper_title": "The Daily Test"}
        # Create a dummy alto file
        with open(self.alto_path, "w") as f:
            f.write("<alto></alto>")

    def tearDown(self):
        if os.path.exists(self.alto_path):
            os.remove(self.alto_path)
        if os.path.exists(self.output_json_path):
            os.remove(self.output_json_path)

    def test_generate_rag_json_file_not_found(self):
        """Test that generate_rag_json returns False when the ALTO file is not found."""
        result = generate_rag_json("non_existent_file.xml", self.output_json_path, self.config)
        self.assertFalse(result)

    @patch('builtins.open', side_effect=Exception("Test error"))
    def test_generate_rag_json_read_error(self, mock_open):
        """Test that generate_rag_json returns False on file read error."""
        result = generate_rag_json(self.alto_path, self.output_json_path, self.config)
        self.assertFalse(result)

    @patch('lxml.etree.fromstring', side_effect=etree.XMLSyntaxError("Test error", 1, 1, 1))
    def test_generate_rag_json_xml_syntax_error(self, mock_fromstring):
        """Test that generate_rag_json returns False on XML syntax error."""
        result = generate_rag_json(self.alto_path, self.output_json_path, self.config)
        self.assertFalse(result)

    @patch('json.dump', side_effect=IOError("Test error"))
    def test_generate_rag_json_write_error(self, mock_dump):
        """Test that generate_rag_json returns False on file write error."""
        result = generate_rag_json(self.alto_path, self.output_json_path, self.config)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
