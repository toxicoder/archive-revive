import logging
import os


def setup_logging(log_dir):
    """
    Configures logging to both console and file.
    """
    log_file = os.path.join(log_dir, 'pipeline.log')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    logging.info(f"Logging configured. Log file at: {log_file}")
