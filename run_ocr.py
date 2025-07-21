import subprocess
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def perform_ocr(input_path: str, output_alto_path: str, psm: int = 3) -> bool:
    """
    Executes Tesseract OCR on a preprocessed image to generate a structured ALTO XML file.

    This function uses the Tesseract command-line interface to perform OCR. It is configured
    to produce an ALTO XML file, which contains detailed layout information and recognized text.

    Args:
        input_path (str): The path to the cleaned input image file.
        output_alto_path (str): The desired path for the final ALTO XML output file.
        psm (int): The Page Segmentation Mode (PSM) to be used by Tesseract.
                     Defaults to 3 (fully automatic page segmentation).

    Returns:
        bool: True if the OCR process completes successfully and the output file is created,
              False otherwise.
    """
    # Tesseract requires the output path without the extension, as it adds '.xml' automatically.
    output_basename = os.path.splitext(output_alto_path)[0]

    # Construct the Tesseract command.
    command = [
        "tesseract",
        input_path,
        output_basename,
        "alto",
        "-psm",
        str(psm)
    ]

    logging.info(f"Executing Tesseract OCR for {input_path} with PSM={psm}.")
    logging.debug(f"Tesseract command: {' '.join(command)}")

    try:
        # Execute the Tesseract command.
        result = subprocess.run(
            command,
            check=True,       # Raises CalledProcessError if the command returns a non-zero exit code.
            capture_output=True, # Captures stdout and stderr.
            text=True         # Decodes stdout and stderr as text.
        )
        logging.info("Tesseract execution successful.")
        logging.debug(f"Tesseract stdout: {result.stdout}")

        # The expected output from Tesseract.
        tesseract_output_path = f"{output_basename}.xml"

        # Check if Tesseract produced the output file and rename it to the desired final path.
        if os.path.exists(tesseract_output_path):
            os.rename(tesseract_output_path, output_alto_path)
            logging.info(f"Successfully created and renamed ALTO XML to {output_alto_path}")
            return True
        else:
            logging.error(f"Tesseract did not produce the expected output file: {tesseract_output_path}")
            return False

    except subprocess.CalledProcessError as e:
        # This error is raised when Tesseract returns a non-zero exit code (i.e., an error occurred).
        logging.error(f"Tesseract execution failed with return code {e.returncode}.")
        logging.error(f"Tesseract stderr: {e.stderr}")
        return False
    except FileNotFoundError:
        # This error is raised if the 'tesseract' command is not found.
        logging.error("Tesseract is not installed or not found in your system's PATH.")
        return False
    except Exception as e:
        # Catch any other unexpected errors.
        logging.error(f"An unexpected error occurred during OCR: {e}")
        return False
