import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import socket


class status:
    def __init__(self, status_text: str, status_global: int) -> None:
        self.status_OK: int = 1 if status_text == "インターネット利用可能" else 0
        self.message: str = status_text if status_global else "webサイトに接続できません"
        self.status_OK_global: int = status_global


class wimax:
    def __init__(self) -> None:
        driver = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            options=webdriver.ChromeOptions()
        )
        driver.implicitly_wait(10)
        self.driver = driver
        self.status = status("init", 0)
        self.password = os.environ["WIMAXPASS"]

    def get_status_global(self, Host="8.8.8.8", port=53, timeout=3) -> bool:
        """
        Host: 8.8.8.8 (google-public-dns-a.google.com)
        OpenPort: 53/tcp
        Service: domain (DNS/TCP)
        """
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
                (Host, port))
            return True
        except socket.error as e:
            print(e)
            return False

    def get_status(self) -> None:
        self.driver.get("http://192.168.179.1/cgi-bin/luci/")
        self.driver.set_window_size(644, 723)
        result_elems: list = self.driver.find_elements(
            By.CSS_SELECTOR, "tr:nth-child(3) > td")
        self.status = status(result_elems[0].text, self.get_status_global())

    def restart(self) -> None:
        self.driver.get("http://192.168.179.1/cgi-bin/luci/")
        self.driver.set_window_size(644, 723)
        self.driver.find_element(By.ID, "Password").click()
        self.driver.find_element(By.ID, "Password").send_keys("kamonowimax")
        self.driver.find_element(By.ID, "Password").send_keys(Keys.ENTER)
        self.driver.find_element(By.LINK_TEXT, "再起動").click()
        self.driver.find_element(By.ID, "Restart").click()
        time.sleep(1)
        assert self.driver.switch_to.alert.text == "再起動を行います。よろしいですか？"
        self.driver.switch_to.alert.accept()
        print("再起動します")

    def __del__(self) -> None:
        self.driver.quit()


if __name__ == '__main__':
    wifi = wimax()
    wifi.get_status()
    wifi.restart()
