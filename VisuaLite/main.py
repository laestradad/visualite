import logging
from modules.logging_cfg import setup_logger
logger = setup_logger()
logging.info("Visualite Launched")
from modules import gui

if __name__ == "__main__":

    logging.debug("--- Start ---")

    try:

        root = gui.App()
        root.mainloop()

    except Exception as e:
        logging.error("Failed")
        logging.error(e, exc_info=True)
    
    finally:
        logging.debug("--- End ---")