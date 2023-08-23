from modules.logging_cfg import setup_logger, backup_log
# Backup the previous log before starting the application
backup_log()
# Create new log file
logger = setup_logger()
logger.info("Visualite Launched")

from modules import gui

if __name__ == "__main__":

    logger.debug("--- Start ---")

    try:
        root = gui.App()
        root.mainloop()

    except Exception as e:
        logger.error("--- Tkinter failed ---")
        logger.error(e, exc_info=True)
    
    finally:
        logger.debug("--- End ---")