"""
This module contains the image preprocessing functionality.
"""
import logging
import cv2


def preprocess_image(image_path, output_path):
    """
    Applies a series of preprocessing steps to the image.
    """
    logging.info(f"Preprocessing image: {image_path}")

    # Read the image
    image = cv2.imread(image_path)

    # TODO: Add actual preprocessing steps here

    # For now, just save a copy of the original image
    cv2.imwrite(output_path, image)
    logging.info(f"Preprocessed image saved to: {output_path}")
    return output_path
