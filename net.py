import os
import csv
import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import ccxt.async_support as ccxt


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

    async def get_ohlcv(self):
        client = ccxt.bybit()
        async for symbol in self.symbols:
            ohlcv = await client.fetch_ohlcv(symbol=symbol, timeframe=1, limit=1, params={"category": "linear"})[0]
            print(f"{symbol} || {' '.join(ohlcv[2:])}")
            with open(f"./ohlcv_{self.session_name}/{symbol}.csv", "a") as file:
                writer = csv.writer(file)
                writer.writerow(*ohlcv[2:])
                file.close()
        if self.count == self.limit:
            exit()
        else:
            self.count += 1
        await client.close()

    async def new_ohlcv_session(self):
        os.chdir("./sessions")
        os.mkdir(f"ohlcv_{self.session_name}")
        with open(f"./ohlcv_{self.session_name}/settings.txt", "w") as file:
            now = datetime.datetime.now()
            file.write(f"symbols={self.symbols}\nstarttime={now}\ntimeframe={self.timeframe}\nlimit={self.limit}")
            file.close()
        sched = AsyncIOScheduler()
        sched.add_job(self.get_ohlcv, trigger="interval", minute=self.timeframe)
