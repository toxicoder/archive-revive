import argparse
import configparser
import logging
import os
from src.utils.logging_config import setup_logging

def main(input_dir, output_dir, config_path):
    """
    Main pipeline to orchestrate the document processing.
    """
    # Create output directories
    logs_dir = os.path.join(output_dir, 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    # Setup logging
    setup_logging(logs_dir)
    logging.info("Starting the document processing pipeline.")

    # Load configuration
    config = configparser.ConfigParser()
    config.read(config_path)

    logging.info(f"Configuration loaded from {config_path}")

    # Process each image in the input directory
    for image_name in os.listdir(input_dir):
        if image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
            image_path = os.path.join(input_dir, image_name)
            base_name = os.path.splitext(image_name)[0]

            # Define output paths for this image
            preprocessed_dir = os.path.join(output_dir, 'preprocessed')
            ocr_dir = os.path.join(output_dir, 'ocr')
            rag_dir = os.path.join(output_dir, 'rag')
            html_dir = os.path.join(output_dir, 'html')

            os.makedirs(preprocessed_dir, exist_ok=True)
            os.makedirs(ocr_dir, exist_ok=True)
            os.makedirs(rag_dir, exist_ok=True)
            os.makedirs(html_dir, exist_ok=True)

            preprocessed_image_path = os.path.join(preprocessed_dir, image_name)

            # --- Preprocessing ---
            from src.preprocess import preprocess_image
            preprocessed_path = preprocess_image(image_path, preprocessed_image_path)

            # --- OCR ---
            from src.ocr import run_ocr
            psm = config.get('OCR', 'PSM', fallback='3')
            alto_path = run_ocr(preprocessed_path, ocr_dir, psm)

            # --- Normalize for RAG ---
            from src.normalize_rag import normalize_for_rag
            normalize_for_rag(alto_path, rag_dir)

            # --- Generate HTML ---
            from src.generate_html import generate_html
            generate_html(alto_path, html_dir)

    logging.info("Pipeline finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Document Processing Pipeline")
    parser.add_argument("--input_dir", required=True, help="Path to the directory containing raw scanned images.")
    parser.add_argument("--output_dir", required=True, help="Path to the root directory where all processed files will be saved.")
    parser.add_argument("--config", required=True, help="Path to a configuration file (e.g., config.ini).")

    args = parser.parse_args()

    main(args.input_dir, args.output_dir, args.config)
