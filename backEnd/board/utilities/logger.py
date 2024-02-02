import logging

handler = logging.FileHandler('app.log')
handler.setLevel(logging.INFO)  # Set minimum log level
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)