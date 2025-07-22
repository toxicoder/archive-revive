"""
This module contains the image preprocessing functionality.
"""
import logging
import cv2


def preprocess_image(image_path, output_path):
    """
    Applies a series of preprocessing steps to the image.
    """
    logging.info("Preprocessing image: %s", image_path)

    # Read the image
    image = cv2.imread(image_path)

    # For now, just save a copy of the original image
    cv2.imwrite(output_path, image)
    logging.info("Preprocessed image saved to: %s", output_path)
    return output_path
