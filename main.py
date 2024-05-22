import asyncio
from net import NET
import utils

n = NET(session_name="test",
        symbols=utils.get("symbols"),
        timeframe=1,
        limit=30)

asyncio.run(n.new_ohlcv_session())