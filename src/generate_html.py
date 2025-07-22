"""
This module contains the functionality to generate an HTML page from an ALTO XML file.
"""
import logging
import os
import cv2
from lxml import etree


XMLNS = "http://www.loc.gov/standards/alto/ns-v3#"


def create_html_from_alto(
    alto_path: str,
    output_html_path: str,
    image_dir_path: str,
    original_scan_path: str
) -> bool:
    """
    Parses an ALTO XML file and generates an HTML file that visually
    reconstructs the original page layout.

    Args:
        alto_path: Path to the alto.xml file.
        output_html_path: Path where the final .html file should be saved.
        image_dir_path: Path to the directory where extracted images
                        should be saved.
        original_scan_path: Path to the original scanned image for image
                            extraction.

    Returns:
        True if the HTML was generated successfully, False otherwise.
    """
    logging.info("Generating HTML from ALTO file: %s", alto_path)
    try:
        # Ensure the output directory for images exists
        os.makedirs(image_dir_path, exist_ok=True)

        # Create the basic HTML document structure
        html = etree.Element("html")
        head = etree.SubElement(html, "head")
        etree.SubElement(head, "title").text = os.path.basename(
            output_html_path
        )
        etree.SubElement(head, "link", rel="stylesheet", href="style.css")
        body = etree.SubElement(html, "body")

        tree = etree.parse(alto_path)

        for string_element in tree.findall(f".//{{{XMLNS}}}String"):
            _process_string_element(string_element, body)

        original_image = cv2.imread(original_scan_path)
        if original_image is None:
            logging.error("Could not read image: %s", original_scan_path)
            return False

        for i, illust_element in enumerate(
            tree.findall(f".//{{{XMLNS}}}Illustration")
        ):
            _process_illustration_element(
                illust_element, body, original_image, image_dir_path, i
            )

        # Add the fixed-position button
        button = etree.SubElement(
            body, "a", href=original_scan_path, target="_blank"
        )
        button.text = "View Original Scan"
        button.set("class", "view-original-button")

        # Write the complete HTML structure to the output file
        with open(output_html_path, "wb") as f:
            f.write(
                etree.tostring(
                    html, pretty_print=True, method="html", encoding="utf-8"
                )
            )

        logging.info("HTML file saved to: %s", output_html_path)
        return True

    except (IOError, etree.ParseError) as e:
        logging.error("Error generating HTML from ALTO file: %s", e)
        return False


def _process_string_element(string_element, body):
    attrs = {
        "content": string_element.get("CONTENT"),
        "hpos": int(float(string_element.get("HPOS"))),
        "vpos": int(float(string_element.get("VPOS"))),
        "width": int(float(string_element.get("WIDTH"))),
        "height": int(float(string_element.get("HEIGHT"))),
    }

    span = etree.SubElement(body, "span")
    span.text = attrs["content"]
    style = (
        "position: absolute; "
        f"left: {attrs['hpos']}px; top: {attrs['vpos']}px; "
        f"width: {attrs['width']}px; height: {attrs['height']}px;"
    )
    span.set("style", style)


def _process_illustration_element(illust_element, body, original_image, image_dir_path, i):
    attrs = {
        "hpos": int(float(illust_element.get("HPOS"))),
        "vpos": int(float(illust_element.get("VPOS"))),
        "width": int(float(illust_element.get("WIDTH"))),
        "height": int(float(illust_element.get("HEIGHT"))),
    }

    # Crop the image
    cropped_image = original_image[
        attrs["vpos"] : attrs["vpos"] + attrs["height"],
        attrs["hpos"] : attrs["hpos"] + attrs["width"],
    ]

    # Save the cropped image
    image_filename = f"illustration_{i}.png"
    image_path = os.path.join(image_dir_path, image_filename)
    cv2.imwrite(image_path, cropped_image)

    # Create an img tag
    img = etree.SubElement(body, "img")
    img.set(
        "src",
        os.path.join(os.path.basename(image_dir_path), image_filename)
    )
    img.set(
        "style",
        "position: absolute; "
        f"left: {attrs['hpos']}px; top: {attrs['vpos']}px; "
        f"width: {attrs['width']}px; height: {attrs['height']}px;"
    )
