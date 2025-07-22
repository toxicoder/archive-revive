import logging
import os
import pytesseract
from PIL import Image


def run_ocr(image_path, output_dir, psm):
    """
    Runs Tesseract OCR on the given image and saves the ALTO XML output.
    """
    logging.info(f"Running OCR on {image_path} with PSM {psm}")

    # Construct the output path
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    alto_path = os.path.join(output_dir, f"{base_name}.xml")

    # Run Tesseract
    try:
        xml_output = pytesseract.image_to_alto_xml(
            Image.open(image_path), config=f'--psm {psm}'
        )
        with open(alto_path, 'wb') as f:
            f.write(xml_output)
        logging.info(f"ALTO XML saved to: {alto_path}")
    except pytesseract.TesseractNotFoundError:
        logging.error("Tesseract is not installed or not in your PATH.")
        raise
    except Exception as e:
        logging.error(f"Error during OCR processing: {e}")
        raise

    return alto_path
