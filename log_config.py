import logging
def log(name):
    # create logger
    logger = logging.getLogger(name)
  #  logger.setLevel(logging.INFO)
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
   # ch.setLevel(logging.DEBUG)
    fh = logging.FileHandler('log.txt')

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    # add ch to logger
    logger.addHandler(ch)
    return logger