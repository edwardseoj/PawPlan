import logging

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers = [
            logging.StreamHandler(),  # prints to console
            logging.FileHandler("../pawplan.log", mode="a"),  # also writes to a file
        ],
    )