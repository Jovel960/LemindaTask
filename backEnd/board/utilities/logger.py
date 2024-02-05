import logging
def set_app_logger(app) -> None:
    handler = logging.FileHandler('app.log')
    app.logger.setLevel(logging.INFO)  # Set minimum log level
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    return None