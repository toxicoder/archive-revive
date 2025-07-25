import json
import os
import unittest
from src.normalize_rag import generate_rag_json


class TestNormalizeRag(unittest.TestCase):

    def setUp(self):
        self.alto_path = 'test.xml'
        self.output_json_path = 'test.json'
        self.config = {
            "publication_date": "2024-07-21",
            "newspaper_title": "The Daily Test"
        }
        # Create a dummy ALTO XML file
        alto_xml = """
<alto>
    <Layout>
        <Page>
            <PrintSpace>
                <TextBlock ID="ID1">
                    <TextLine>
                        <String CONTENT="test rag normalization script"/>
                    </TextLine>
                </TextBlock>
                <TextBlock ID="ID2">
                    <TextLine>
                        <String CONTENT="another block of text"/>
                    </TextLine>
                </TextBlock>
            </PrintSpace>
        </Page>
    </Layout>
</alto>
"""
        with open(self.alto_path, "w") as f:
            f.write(alto_xml)

    def tearDown(self):
        if os.path.exists(self.alto_path):
            os.remove(self.alto_path)
        if os.path.exists(self.output_json_path):
            os.remove(self.output_json_path)

    def test_generate_rag_json(self):
        result = generate_rag_json(
            self.alto_path, self.output_json_path, self.config
        )
        self.assertTrue(result)
        self.assertTrue(os.path.exists(self.output_json_path))

        with open(self.output_json_path, 'r') as f:
            data = json.load(f)

        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['text'], 'test rag normalization script')
        self.assertEqual(
            data[0]['metadata']['newspaper_title'], 'The Daily Test'
        )
        self.assertEqual(data[1]['text'], 'another block text')


if __name__ == '__main__':
    unittest.main()
