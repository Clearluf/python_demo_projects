import json
import sys
import threading
import time
from datetime import datetime
from datetime import time as Time

import requests
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

app = QApplication(sys.argv)

flag_exit = False


def query_stock(code):
    url = "https://hq.sinajs.cn/list=" + code

    payload = {}
    headers = {"Referer": "https://finance.sina.com.cn"}

    response = requests.request("GET", url, headers=headers, data=payload)
    res_txt = response.text
    res_list = res_txt.split("=")[1].replace('"', "").split(",")
    result = (
        "股票名称: "
        + res_list[0]
        + " 最新价格: "
        + res_list[3]
        + " 今日收益率: "
        + str(
            round(
                (float(res_list[3]) - float(res_list[2])) / float(res_list[2]) * 100, 2
            )
        )
    )
    return result


def exit_clicked():
    """
    A function to handle the event when the exit button is clicked.
    No parameters are passed to the function.
    The function does not return anything.
    """
    print("退出按钮被点击")
    global flag_exit
    flag_exit = True
    app.exit()


tray_icon = QSystemTrayIcon()

tray_icon.setParent(app)
tray_icon.setIcon(QIcon("money.png"))
menu = QMenu()
exit_action = QAction("退出")
exit_action.triggered.connect(exit_clicked)
menu.addAction(exit_action)

tray_icon.setContextMenu(menu)
tray_icon.show()


def func():
    global flag_exit

    result = ''
    stocks = json.loads(open("stocks.json", encoding="utf-8").read())
    for stock in stocks:
        code = stock["code"]
        result = result+query_stock(code).split("今日收益率")[0]+"\n"

    today = datetime.now().date()
    # 判断今日是否是工作日
    if today.weekday() > 5:
        while not flag_exit:
            tray_icon.setToolTip("休息日,暂停更新\n"+result)
            time.sleep(5)
    else:
        now = datetime.now()
        morning_start = Time(9, 25)
        morning_end = Time(11, 30)
        afternoon_start = Time(13, 00)
        afternoon_end = Time(15, 00)
        if not (
            (morning_start <= now.time() < morning_end)
            or (afternoon_start <= now.time() < afternoon_end)
        ):
            while not flag_exit:
                tray_icon.setToolTip("闭市了,别看了\n"+result)
                time.sleep(5)
    while not flag_exit:
        result = ''
        stocks = json.loads(open("stocks.json", encoding="utf-8").read())
        for stock in stocks:
            code = stock["code"]
            result = result+query_stock(code)+"\n"
        tray_icon.setToolTip(result)
        time.sleep(5)


tooltip_t = threading.Thread(target=func)
tooltip_t.start()

app.exec()
