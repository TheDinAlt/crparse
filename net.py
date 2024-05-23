import os
import csv
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import ccxt
import sys
import logging


def setup_logger(name, log_file, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger('net', 'net.log')
logger.info("INIT")


def decorator_error_logger(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Exception: {type(e).__name__}: {str(e)}")

    return wrapper


def cprint(text):
    logger.info(text)


class NET:
    def __init__(self,
                 session_name: str,
                 symbols: list,
                 timeframe: int | str,
                 limit: int):
        self.session_name = session_name
        self.symbols = symbols
        self.timeframe = timeframe
        self.limit = limit
        self.count = 0

    @decorator_error_logger
    def get_ohlcv(self):
        client = ccxt.bybit()
        for symbol in self.symbols:
            ohlcv = client.fetch_ohlcv(symbol=symbol, timeframe=1, limit=1, params={"category": "linear"})[0]
            info = list(map(str, ohlcv[1:]))
            cprint(f"{symbol} || {' '.join(info)}")
            with open(f"./ohlcv_{self.session_name}/{symbol}.csv", "a") as file:
                writer = csv.writer(file)
                writer.writerow(info)
                file.close()
        if self.count == self.limit:
            exit()
        else:
            self.count += 1

    def new_ohlcv_session(self):
        os.chdir("./sessions")
        if not os.path.exists(f"ohlcv_{self.session_name}"):
            os.mkdir(f"ohlcv_{self.session_name}")
        with open(f"./ohlcv_{self.session_name}/settings.txt", "w") as file:
            now = datetime.datetime.now()
            file.write(f"symbols={self.symbols}\nstarttime={now}\ntimeframe={self.timeframe}\nlimit={self.limit}")
            file.close()
        sched = BackgroundScheduler()
        sched.add_job(self.get_ohlcv, trigger="interval", minutes=self.timeframe)
        sched.start()
