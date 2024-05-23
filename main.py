import time
from net import NET
import utils

n = NET(session_name="test",
        symbols=utils.get("symbols"),
        timeframe=1,
        limit=30)

n.new_ohlcv_session()

while True:
    time.sleep(1)
