#!/usr/bin/env python3

import subprocess
import threading
import requests
from time import sleep
from telegram.ext import Updater, CommandHandler

import config as cfg


class Pinger(threading.Thread):
    def __init__(self, hosts, interval, check_func):
        super().__init__()
        self._interval = interval
        self._hosts = {}
        self._check = check_func
        self._init_hosts

    def _init_hosts(hosts):
        for host in hosts:
            hosts[host] = False

    def get_hosts(self):
        return self._hosts

    def run(self):
        while True:
            for host in cfg.ICMP_HOSTS:
                self._hosts[host] = self._check(host)

            sleep(self._interval)

def wat(bot, update):
    update.message.reply_text('wat')

class Checker():
    def __init__(self, cfg):
        self._cfg = cfg
        self._icmp = None
        self._http = None
        self._telegram = None

    def _init_icmp(self):
        self._icmp = Pinger(self._cfg.ICMP_HOSTS, self._cfg.ICMP_INTERVAL, self.icmp_ping)
        self._icmp.start()

    def _init_http(self):
        pass

    def _init_telegram(self):
        self._telegram = Updater(self._cfg.TELEGRAM_TOKEN)
        self._telegram.dispatcher.add_handler(CommandHandler('check', wat))
        self._telegram.start_polling()

    def icmp_ping(host):
        with open('/dev/null', 'w') as devnull:
            exit_code = subprocess.call(
                    ['/usr/bin/ping', '-c1', '-w1', host],
                    stdout=devnull)
        return not exit_code

    def http_ping(host):
        r = requests.get(host)

    def check_respond(bot, update):
        update.message.reply_text('wat')


def main():
    checker = Checker(cfg)
    while True:
        sleep(1)


if __name__ == '__main__':
    main()

