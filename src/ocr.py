"""
This module contains the OCR functionality for the project.
"""
import logging
import os
import pytesseract
from PIL import Image


def run_ocr(image_path, output_dir, psm):
    """
    Runs Tesseract OCR on the given image and saves the ALTO XML output.
    """
    logging.info("Running OCR on %s with PSM %s", image_path, psm)

    # Construct the output path
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    alto_path = os.path.join(output_dir, f"{base_name}.xml")

    # Run Tesseract
    try:
        xml_output = pytesseract.image_to_alto_xml(
            Image.open(image_path), config=f'--psm {int(psm)}'
        )
        with open(alto_path, 'wb') as f:
            f.write(xml_output)
        logging.info("ALTO XML saved to: %s", alto_path)
    except pytesseract.TesseractNotFoundError:
        logging.error("Tesseract is not installed or not in your PATH.")
        raise
    except (Exception, ValueError) as e:
        logging.error("Error during OCR processing: %s", e)
        raise

    return alto_path
