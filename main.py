import argparse
import configparser
import logging
import os
import fitz  # PyMuPDF
from src.utils.logging_config import setup_logging

def process_image(image_path, output_dir, config):
    """
    Processes a single image file (preprocessing, OCR, HTML generation, RAG normalization).
    """
    try:
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        # Define output paths for this image
        preprocessed_dir = os.path.join(output_dir, 'preprocessed')
        ocr_dir = os.path.join(output_dir, 'ocr')
        rag_dir = os.path.join(output_dir, 'rag')
        html_dir = os.path.join(output_dir, 'html')

        os.makedirs(preprocessed_dir, exist_ok=True)
        os.makedirs(ocr_dir, exist_ok=True)
        os.makedirs(rag_dir, exist_ok=True)
        os.makedirs(html_dir, exist_ok=True)

        preprocessed_image_path = os.path.join(preprocessed_dir, os.path.basename(image_path))

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
        from src.generate_html import create_html_from_alto
        html_output_path = os.path.join(html_dir, f"{base_name}.html")
        image_dir_path = os.path.join(html_dir, 'images')
        create_html_from_alto(alto_path, html_output_path, image_dir_path, preprocessed_path)

        # --- Copy CSS file ---
        import shutil
        css_source_path = 'src/style.css'
        css_dest_path = os.path.join(html_dir, 'style.css')
        if os.path.exists(css_source_path):
            shutil.copy(css_source_path, css_dest_path)

        logging.info(f"Successfully processed image: {image_path}")

    except Exception as e:
        logging.error(f"Error processing image {image_path}: {e}")


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

    # Process each file in the input directory
    for file_name in os.listdir(input_dir):
        file_path = os.path.join(input_dir, file_name)
        base_name = os.path.splitext(file_name)[0]

        try:
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp')):
                logging.info(f"Processing image file: {file_name}")
                image_output_dir = os.path.join(output_dir, base_name)
                os.makedirs(image_output_dir, exist_ok=True)
                process_image(file_path, image_output_dir, config)

            elif file_name.lower().endswith('.pdf'):
                logging.info(f"Processing PDF file: {file_name}")
                pdf_output_dir = os.path.join(output_dir, base_name)
                os.makedirs(pdf_output_dir, exist_ok=True)

                # Open the PDF
                pdf_document = fitz.open(file_path)
                for page_num in range(len(pdf_document)):
                    page = pdf_document.load_page(page_num)
                    image_bytes = page.get_pixmap().tobytes("png")

                    # Save the page as an image
                    page_image_path = os.path.join(pdf_output_dir, f"page_{page_num + 1:03}.png")
                    with open(page_image_path, "wb") as img_file:
                        img_file.write(image_bytes)

                    logging.info(f"Processing page {page_num + 1} of {file_name}")
                    process_image(page_image_path, pdf_output_dir, config)

                pdf_document.close()

        except Exception as e:
            logging.error(f"Error processing file {file_name}: {e}")


    logging.info("Pipeline finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Document Processing Pipeline")
    parser.add_argument("--input_dir", required=True, help="Path to the directory containing raw scanned images.")
    parser.add_argument("--output_dir", required=True, help="Path to the root directory where all processed files will be saved.")
    parser.add_argument("--config", required=True, help="Path to a configuration file (e.g., config.ini).")

    args = parser.parse_args()

    main(args.input_dir, args.output_dir, args.config)
