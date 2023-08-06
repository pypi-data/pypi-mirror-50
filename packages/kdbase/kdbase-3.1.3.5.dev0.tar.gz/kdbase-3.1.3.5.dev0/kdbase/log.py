# -*- coding:utf-8 -*-

import logging
import os
import shutil
import time
import sys

initialized = False
formatter = logging.Formatter('%(asctime)s %(levelname)s %(process)d' '[%(filename)s:%(lineno)d %(funcName)s]: %(message)s')


class Configer():
    def __init__(self):
        self.__log_path = ""
        self.__file_handler = None
        self.__console_handler = None
        self.__pure_path = "./log.txt"
        self.__time_format = "%Y%m%d%H%M"
        self.__time_format = "%Y%m%d"

    inst = None

    @staticmethod
    def get():
        if Configer.inst == None:
            Configer.inst = Configer()
        return Configer.inst

    def set_file_handler(self):
        date_str = time.strftime(self.__time_format)
        self.__log_path = self.__pure_path + '.' + date_str

        fh = logging.FileHandler(self.__log_path)
        fh.setFormatter(formatter)
        self.__file_handler = fh
        logging.getLogger('').addHandler(fh)

    def set_console_handler(self):
        if not self.__console_handler:
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            console.setFormatter(formatter)
            self.__console_handler = console
            logging.getLogger('').addHandler(console)
            logging.getLogger('').setLevel(logging.INFO)

    def del_console_handler(self):
        logging.getLogger('').removeHandler(self.__console_handler)
        del self.__console_handler
        self.__console_handler = None

    def del_file_handler(self):
        logging.getLogger('').removeHandler(self.__file_handler)
        del self.__file_handler
        self.__file_handler = None

    def rotate(self):
        date_str = time.strftime(self.__time_format)
        path = self.__pure_path + '.' + date_str
        self.__log_path

        if path == self.__log_path:
            return
        sys.stdout.flush()
        sys.stderr.flush()
        self.del_file_handler()
        self.set_file_handler()

    def init(self, level, path="./log.txt", quiet=False):
        self.__pure_path = path
        if quiet:
            self.del_console_handler()

        if not quiet and not self.__console_handler:
            self.set_console_handler()
        self.set_file_handler()

        cmd = str("logging.getLogger("").setLevel(logging.%s)" % (level.upper()))
        exec cmd


class Logger():
    def __init__(self, elk=False, hosts=None, topic=None):
        self.elk = elk
        if self.elk:
            self.hosts = hosts
            self.topic = topic

        #self.info = logging.info
        #self.debug = logging.debug
        #self.warning = logging.warning
        #self.error = logging.error
        #self.critical = logging.critical
        #Configer.get().del_console_handler()
        #Configer.get().set_console_handler()

    def info(self, msg, *args, **kwargs):
        if self.elk:
            log_elk(self.hosts, self.topic, msg % args)
        logging.info(msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        if self.elk:
            log_elk(self.hosts, self.topic, msg % args)
        logging.debug(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.elk:
            log_elk(self.hosts, self.topic, msg % args)
        logging.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.elk:
            log_elk(self.hosts, self.topic, msg % args)
        logging.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.elk:
            log_elk(self.hosts, self.topic, msg % args)
        logging.critical(msg, *args, **kwargs)


def log_elk(hosts, topic, msg):
    try:
        from kafka_utils import kafka_produce
        kafka_produce(hosts, topic, msg)
    except:
        logging.info('fail to log elk of hosts: [%s], topic: [%s]', 
            hosts, topic)
        import traceback
        err_msg = traceback.format_exc()
        logging.error(err_msg)


def log_init(level, path="./log.txt", quiet=True, 
        elk=False, hosts=None, topic=None):
    global initialized
    if initialized: return
    Configer.get().init(level, path, quiet)
    
    if elk:
        global g_logger
        g_logger = Logger(elk, hosts, topic)

    #initialized = True


g_logger = Logger()


def logger():
    Configer.get().rotate()
    return g_logger


def log(log_dir, log_level='info', quiet=False, elk=True, hosts=None, topic=None):
    def decorator(func):
        def wrapper(*args, **kw):
            log_init(log_level, log_dir, quiet=quiet, elk=elk, hosts=hosts, topic=topic)
            return func(*args, **kw)
        return wrapper
    return decorator



@log('./log2.txt', elk=False, hosts='dev-01:9092,dev-02:9092,dev-03:9092', topic='elk-logstash-dev')
def f():
    logger().info('fffffff')


if __name__ == '__main__':
    log_init('info', './log.txt', quiet=False, 
            elk=False, hosts='dev-01:9092,dev-02:9092,dev-03:9092', topic='elk-logstash-dev')
    while True:
        l = logger()
        import random
        l.info('info:abc, %s', random.randint(1, 1000))
        f()
        #l.error('error:abc')
        #l.debug('debug:abc')
        time.sleep(1)


