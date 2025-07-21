import logging
import os

def run_ocr(image_path, output_dir, psm):
    """
    Runs Tesseract OCR on the given image and saves the ALTO XML output.
    """
    logging.info(f"Running OCR on {image_path} with PSM {psm}")

    # Construct the output path
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    alto_path = os.path.join(output_dir, f"{base_name}.xml")

    # TODO: Add actual Tesseract command here

    # For now, create a dummy ALTO XML file
    with open(alto_path, 'w') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<alto xmlns="http://www.loc.gov/standards/alto/ns-v3#"></alto>\n')

    logging.info(f"ALTO XML saved to: {alto_path}")
    return alto_path
