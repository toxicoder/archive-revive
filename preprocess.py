import cv2
import numpy as np

def process_image(input_path: str, output_path: str) -> bool:
    """
    Reads an image, deskews it, reduces noise, binarizes it, and saves the result.

    Args:
        input_path: Path to the raw source image.
        output_path: Path where the cleaned image should be saved.

    Returns:
        True if the image was processed and saved successfully, False otherwise.
    """
    try:
        # Read the image from input_path
        image = cv2.imread(input_path)
        if image is None:
            print(f"Error: Could not read image from {input_path}")
            return False

        # Deskew
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        binary = cv2.bitwise_not(gray)
        thresh = cv2.threshold(binary, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        coords = np.column_stack(np.where(thresh > 0))
        angle = cv2.minAreaRect(coords)[-1]

        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

        # Noise Reduction
        denoised = cv2.fastNlMeansDenoisingColored(rotated, None, 10, 10, 7, 21)

        # Binarization
        gray_denoised = cv2.cvtColor(denoised, cv2.COLOR_BGR2GRAY)
        binarized = cv2.adaptiveThreshold(gray_denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

        # Save the final processed image
        cv2.imwrite(output_path, binarized)

        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == '__main__':
    # Create a dummy image for testing
    try:
        dummy_image = np.zeros((200, 400), dtype=np.uint8)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(dummy_image, 'This is a test image.', (10, 100), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        # Introduce a slight rotation
        rows, cols = dummy_image.shape
        M = cv2.getRotationMatrix2D((cols/2,rows/2), 5, 1)
        rotated_dummy = cv2.warpAffine(dummy_image, M, (cols,rows))

        input_filename = 'raw_image.png'
        output_filename = 'cleaned_image.png'

        cv2.imwrite(input_filename, rotated_dummy)

        # Process the dummy image
        if process_image(input_filename, output_filename):
            print(f"Image processed and saved to {output_filename}")
        else:
            print("Image processing failed.")

    except Exception as e:
        print(f"An error occurred during the example run: {e}")
