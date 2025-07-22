import json
import logging
import re
from lxml import etree
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def generate_rag_json(
    alto_path: str, output_json_path: str, config: dict
) -> bool:
    """
    Processes an ALTO XML file to produce a clean, structured JSON file for
    RAG ingestion.
    """
    logging.info(f"Normalizing ALTO XML for RAG: {alto_path}")

    try:
        with open(alto_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()
    except FileNotFoundError:
        logging.error(f"ALTO XML file not found at: {alto_path}")
        return False
    except Exception as e:
        logging.error(f"Error reading ALTO XML file: {e}")
        return False

    # Remove the default namespace declaration for easier parsing
    xml_content = re.sub(' xmlns="[^"]+"', '', xml_content, count=1)

    try:
        root = etree.fromstring(xml_content.encode('utf-8'))
    except etree.XMLSyntaxError as e:
        logging.error(f"Error parsing ALTO XML: {e}")
        return False

    articles = []
    stop_words = set(stopwords.words('english'))

    for text_block in root.findall('.//TextBlock'):
        raw_text = ' '.join(
            string.get('CONTENT') for string in text_block.findall('.//String')
        )

        # Hyphenation correction
        cleaned_text = re.sub(r'-\s+', '', raw_text)

        # Artifact removal
        cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', cleaned_text)

        # Normalization
        cleaned_text = cleaned_text.lower()
        tokens = word_tokenize(cleaned_text)
        tokens = [word for word in tokens if word not in stop_words]
        cleaned_text = ' '.join(tokens)

        article_object = {
            "text": cleaned_text,
            "metadata": {
                "publication_date": config.get("publication_date"),
                "newspaper_title": config.get("newspaper_title"),
                "id": text_block.get('ID'),
                "height": text_block.get('HEIGHT'),
                "width": text_block.get('WIDTH'),
                "x": text_block.get('HPOS'),
                "y": text_block.get('VPOS'),
            }
        }
        articles.append(article_object)

    try:
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=4)
    except IOError as e:
        logging.error(f"Error writing JSON to file: {e}")
        return False

    logging.info(f"RAG-ready JSON saved to: {output_json_path}")
    return True
