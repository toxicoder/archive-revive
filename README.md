# Historical Newspaper OCR & Layout Preservation Pipeline

This project is a multi-stage pipeline that processes scanned historical newspaper articles and converts them into two high-value digital formats: a web-optimized HTML representation that preserves the original visual layout, and a structured JSON format optimized for ingestion into a Retrieval-Augmented Generation (RAG) system.

## Core Features

-   **High-Fidelity HTML:** Generates HTML/CSS that visually replicates the original newspaper layout, including columns, headlines, and images.
-   **RAG-Optimized Data:** Produces clean, normalized, and structured JSON, where each entry represents a full article, perfect for AI-powered research.
-   **Image Preprocessing:** Enhances raw scans to improve OCR accuracy by handling skew, noise, and uneven lighting.
-   **Traceability:** Links every piece of generated content back to its source location on the original scanned page.
-   **Open-Source:** Built entirely with open-source tools.

## Technology Stack

| Stage                | Tool/Library      | Purpose                                    |
| -------------------- | ----------------- | ------------------------------------------ |
| **Orchestration** | Python 3.9+       | Master scripting and pipeline control      |
| **Image Processing** | OpenCV-Python     | Deskewing, noise reduction, binarization   |
| **OCR Engine** | Tesseract OCR 5   | Text extraction with layout data (ALTO XML)|
| **HTML Conversion** | lxml (Python)     | Parsing ALTO XML to generate HTML/CSS      |
| **Text Normalization**| spaCy / NLTK    | Cleaning and structuring text for RAG      |
| **Data Storage** | File System / MongoDB | Output file storage and structured data    |


## Getting Started

**Prerequisites:**
-   Python 3.9+
-   Tesseract OCR 5 installed and accessible in your system's PATH.

**Setup (Future):**
1.  Clone the repository: `git clone <repo-url>`
2.  Install dependencies: `pip install -r requirements.txt`
3.  Run the pipeline: `python main.py --input /path/to/your/scan.tiff`

## Project Status

**Pre-alpha:** This is the initial project setup. The scripts are placeholders for development.
