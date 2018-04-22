import logging
import threading
from client import MuggleClientThread
from queue import Queue
import json


class Strategy():
    def __init__(self, name):
        self.name = name
        self.msgqueue = Queue()
        self.client = MuggleClientThread(self.name, self.msgqueue)

    def run(self):
        logger = logging.getLogger()
        logger.info("start strategy: %s %s" % (self.name, threading.current_thread()))

        self.client.start()
        ready = self.msgqueue.get()

        self.before_run()
        while True:
            msg = self.msgqueue.get()
            self.handle_msg(msg)

        self.client.join()

    def before_run(self):
        pass

    def handle_msg(self, msg):
        pass

    # 登陆
    def login(self, user, passwd, reqid=""):
        self.client.ws.send(json.dumps({
            "msg": "login",
            "reqid": reqid,
            "data": {
                "user": user,
                "passwd": passwd,
            }
        }))

    # 订阅
    def sub(self, market, symbol, table, reqid=""):
        self.client.ws.send(json.dumps({
            "msg": "sub",
            "reqid": reqid,
            "data": {
                "market": market,
                "symbol": symbol,
                "table": table,
            }
        }))

    # 下单
    def order_insert(self, symbol, market, dir, type, price, amount):
        """
        下单
        :param symbol: 要交易的品种
        :param market: 市场
        :param dir: 方向 "buy" or "sell"
        :param type: 类型 "market" or "limit"
        :param price: 价格 (市价单忽略)
        :param amount: 数量 (限价单表示下单数量，市价买单表示买多少钱，市价卖单表示卖多少币)
        :return:
        """
        self.client.ws.send(json.dumps({
            "op": "orderinsert",
            "data": {
                "symbol": symbol,
                "market": market,
                "dir": dir,
                "type": type,
                "price": price,
                "amount": amount,
                "strategy": self.name,
            }
        }))