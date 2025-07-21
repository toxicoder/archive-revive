import logging
import os
import cv2
from lxml import etree
from PIL import Image

def create_html_from_alto(alto_path: str, output_html_path: str, image_dir_path: str, original_scan_path: str) -> bool:
    """
    Parses an ALTO XML file and generates an HTML file that visually reconstructs the original page layout.

    Args:
        alto_path: Path to the alto.xml file.
        output_html_path: Path where the final .html file should be saved.
        image_dir_path: Path to the directory where extracted images should be saved.
        original_scan_path: Path to the original scanned image for image extraction.

    Returns:
        True if the HTML was generated successfully, False otherwise.
    """
    logging.info(f"Generating HTML from ALTO file: {alto_path}")
    try:
        # Ensure the output directory for images exists
        os.makedirs(image_dir_path, exist_ok=True)

        # Parse the ALTO XML file
        tree = etree.parse(alto_path)
        xmlns = "http://www.loc.gov/standards/alto/ns-v3#"

        # Create the basic HTML document structure
        html = etree.Element("html")
        head = etree.SubElement(html, "head")
        etree.SubElement(head, "title").text = os.path.basename(output_html_path)
        etree.SubElement(head, "link", rel="stylesheet", href="style.css")
        body = etree.SubElement(html, "body")

        # Process String elements
        for string_element in tree.findall(f".//{{{xmlns}}}String"):
            content = string_element.get("CONTENT")
            hpos = int(float(string_element.get("HPOS")))
            vpos = int(float(string_element.get("VPOS")))
            width = int(float(string_element.get("WIDTH")))
            height = int(float(string_element.get("HEIGHT")))

            span = etree.SubElement(body, "span")
            span.text = content
            span.set("style", f"position: absolute; left: {hpos}px; top: {vpos}px; width: {width}px; height: {height}px;")

        # Process Illustration elements
        original_image = cv2.imread(original_scan_path)
        for i, illust_element in enumerate(tree.findall(f".//{{{xmlns}}}Illustration")):
            hpos = int(float(illust_element.get("HPOS")))
            vpos = int(float(illust_element.get("VPOS")))
            width = int(float(illust_element.get("WIDTH")))
            height = int(float(illust_element.get("HEIGHT")))

            # Crop the image
            cropped_image = original_image[vpos:vpos+height, hpos:hpos+width]

            # Save the cropped image
            image_filename = f"illustration_{i}.png"
            image_path = os.path.join(image_dir_path, image_filename)
            cv2.imwrite(image_path, cropped_image)

            # Create an img tag
            img = etree.SubElement(body, "img")
            img.set("src", os.path.join(os.path.basename(image_dir_path), image_filename))
            img.set("style", f"position: absolute; left: {hpos}px; top: {vpos}px; width: {width}px; height: {height}px;")

        # Add the fixed-position button
        button = etree.SubElement(body, "a", href=original_scan_path, target="_blank")
        button.text = "View Original Scan"
        button.set("class", "view-original-button")

        # Write the complete HTML structure to the output file
        with open(output_html_path, "wb") as f:
            f.write(etree.tostring(html, pretty_print=True, method="html", encoding="utf-8"))

        logging.info(f"HTML file saved to: {output_html_path}")
        return True

    except Exception as e:
        logging.error(f"Error generating HTML from ALTO file: {e}")
        return False
