import logging
import logging.config
import os
import json
import strategy


def init_log():
    if not os.path.exists('./log'):
        os.mkdir('./log')
    logging.config.fileConfig('./conf/log.conf')


class MyStrategy(strategy.Strategy):
    def __init__(self, name):
        strategy.Strategy.__init__(self, name)
        self.logger = logging.getLogger()

    def before_run(self):
        self.logger.info('start rocking')
        # TODO: 在这里，加入你开始策略之前的准备

    def handle_msg(self, msg):
        self.logger.info('%s' % msg)
        # TODO: 在这里开始编写你的策略


if __name__ == '__main__':
    init_log()
    strategy = MyStrategy('hello')
    strategy.run()
