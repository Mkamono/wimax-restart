import os
from store.graph import Statusdatacls
from sqlitemod.migrate import Migration
from network.wimax import wimax
from sqlitemod.base_engine import BaseSession
from sqlitemod.models import Status
import time
from datetime import datetime, timedelta, timezone


class Statuscls(BaseSession):
    def __init__(self, datapath):
        super().__init__(datapath)

    def create(self, stu_OK: int, status_OK_global: int, msg: str):
        JST = timezone(timedelta(hours=+9), 'JST')
        temp = Status(status_OK=stu_OK, status_OK_global=status_OK_global,
                      message=msg, created=datetime.now(JST))
        print(
            f"status_local:{temp.status_OK}, status_global:{temp.status_OK_global} message:{temp.message}, created={temp.created}")
        self.session.add(temp)
        self.session.commit()


if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    datapath = os.path.normpath(
        os.path.join(base, './store/data.sqlite3'))
    time.sleep(10)

    Migration(datapath).status()

    cli = Statuscls(datapath)
    wifi = wimax()

    while True:
        try:
            wifi.get_status()
            cli.create(wifi.status.status_OK,
                       wifi.status.status_OK_global, wifi.status.message)
            if (not wifi.status.status_OK_global):
                wifi.restart()
        except:
            cli.create(0, 0, "ネットワークオフ")
            wifi = wimax()  # 再代入によりデストラクタが実行、wifi接続リセット
            pass
        finally:
            data = Statusdatacls(datapath)
            if data.is_exist_img():
                pass
            else:
                data.save_img()
                print("image saved")
            time.sleep(50)
