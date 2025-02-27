import logging
import os
import shutil

# Create log folder in execution path
PATH = os.getcwd()
log_dir = os.path.join(PATH, '__vl.log')
filename = 'visualite_debug.log'

def backup_log():
    # Save last execution log as visualite_backup.log
    log_filename = os.path.join(log_dir, filename)
    if os.path.exists(log_filename):
        backup_filename = log_filename.replace("debug.log", "backup.log")
        if os.path.exists(backup_filename):
            os.remove(backup_filename)
        shutil.move(log_filename, backup_filename)

def setup_logger():
    # Create folder if it does not exits
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    file_path = os.path.join(log_dir, filename)

    #Create and configure logger
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename= file_path,
                        level= logging.DEBUG,
                        format = LOG_FORMAT,
                        filemode='w' #create new logger each execution of App
                        )

    logger = logging.getLogger()
    return logger
