import sqlite3
import pandas as pd
import os
from datetime import datetime, timedelta, timezone


class Statusdatacls:
    def __init__(self, datapath) -> None:
        JST = timezone(timedelta(hours=+9), 'JST')
        self.datapath = datapath
        dt = datetime.now(JST)
        self.yestarday = str(dt + timedelta(days=-1))[:10] + " 00:00:00.000000"
        self.today = str(dt)[:10] + " 00:00:00.000000"
        self.tommorow = str(dt + timedelta(days=1))[:10] + " 00:00:00.000000"

    def is_exist_img(self) -> bool:
        base = os.path.dirname(os.path.abspath(__file__))
        return os.path.isfile(f"{base}/images/{self.yestarday[:10]}.png")

    def save_img(self) -> None:  # 一日ごとに画像保存
        conn = sqlite3.connect(self.datapath)
        basepath = os.path.dirname(self.datapath)
        df = pd.read_sql_query('SELECT * FROM connection', conn)
        conn.close()

        df.query(
            f"'{self.yestarday}' <= created <= '{self.today}'"
        ).plot(
            x="created", y="status_OK", rot=10, figsize=(10, 2), kind="line"
        ).get_figure().savefig(
            f"{basepath}/images/{self.yestarday[:10]}.png", bbox_inches='tight'
        )


if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    datapath = os.path.normpath(
        os.path.join(base, './data.sqlite3'))
    statusdata = Statusdatacls(datapath)
    if statusdata.is_exist_img():
        print("exist")
    else:
        print("is not exit")
        statusdata.save_img()
