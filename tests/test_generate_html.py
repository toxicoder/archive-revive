import unittest
import os
import cv2
import numpy as np
from src.generate_html import create_html_from_alto
from lxml import etree

class TestGenerateHTML(unittest.TestCase):

    def setUp(self):
        """Set up a dummy ALTO XML file and a dummy image for testing."""
        self.alto_path = "test.xml"
        self.output_html_path = "test.html"
        self.image_dir_path = "test_images"
        self.original_scan_path = "test_scan.png"

        # Create a dummy ALTO XML file
        alto_xml = """
<alto xmlns="http://www.loc.gov/standards/alto/ns-v3#">
    <Layout>
        <Page>
            <PrintSpace>
                <TextBlock>
                    <TextLine>
                        <String CONTENT="Hello" HPOS="10" VPOS="20" WIDTH="50" HEIGHT="10"/>
                    </TextLine>
                </TextBlock>
                <Illustration HPOS="100" VPOS="100" WIDTH="200" HEIGHT="150"/>
            </PrintSpace>
        </Page>
    </Layout>
</alto>
"""
        with open(self.alto_path, "w") as f:
            f.write(alto_xml)

        # Create a dummy image
        img = np.zeros((300, 300, 3), dtype=np.uint8)
        cv2.imwrite(self.original_scan_path, img)

        # Create image directory
        os.makedirs(self.image_dir_path, exist_ok=True)

    def tearDown(self):
        """Clean up the created files."""
        if os.path.exists(self.alto_path):
            os.remove(self.alto_path)
        if os.path.exists(self.output_html_path):
            os.remove(self.output_html_path)
        if os.path.exists(self.original_scan_path):
            os.remove(self.original_scan_path)
        if os.path.exists(self.image_dir_path):
            import shutil
            shutil.rmtree(self.image_dir_path)

    def test_create_html_from_alto(self):
        """Test that the HTML file and image are created successfully."""
        success = create_html_from_alto(self.alto_path, self.output_html_path, self.image_dir_path, self.original_scan_path)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(self.output_html_path))

        # Check for illustration image
        expected_image_path = os.path.join(self.image_dir_path, "illustration_0.png")
        self.assertTrue(os.path.exists(expected_image_path))

        # Check HTML content
        parser = etree.HTMLParser()
        tree = etree.parse(self.output_html_path, parser)
        spans = tree.findall(".//span")
        self.assertEqual(len(spans), 1)
        self.assertEqual(spans[0].text, "Hello")

        imgs = tree.findall(".//img")
        self.assertEqual(len(imgs), 1)
        self.assertTrue("illustration_0.png" in imgs[0].get("src"))

if __name__ == '__main__':
    unittest.main()
