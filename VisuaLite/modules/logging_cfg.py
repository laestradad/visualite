import logging
import os
import datetime

def setup_logger():
    PATH = os.getcwd()
    log_dir = os.path.join(PATH, '__vl.log')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    now_dt = datetime.datetime.now()
    format_dt = now_dt.strftime('_%Y-%m-%d')
    file_path = os.path.join(log_dir, 'VisuaLite{}.log'.format(format_dt))

    #Create and configure logger
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename= file_path,
                        level= logging.DEBUG,
                        format = LOG_FORMAT
                        )

    logger = logging.getLogger()
    return logger
