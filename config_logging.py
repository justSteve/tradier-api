import logging
import os

def setup(filename):
    # Extract just the base filename without the extension
    base_filename = os.path.splitext(os.path.basename(filename))[0]
    log_file = f"_logs/{base_filename}_app.log"

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                        handlers=[logging.FileHandler(log_file), logging.StreamHandler()])

