import time
import requests
import logging


class RequestWrap():
    def __init__(self, logger=None):
        if not logger:
            self.logger = logging.getLogger(__name__)
        else:
            self.logger = logger

    def get(self, url, params=None, **kwargs):
        _start = time.time()
        try:
            res = requests.get(url, params, **kwargs)
        except Exception as e:
            e.status_code = -1
            e.text = str(e.message)
            res = e
            self.logger.error('requests.exceptions.ConnectionError. Error detail:' + str(e.message))
        _end = time.time()
        self.logger.info('remote GET call: uri = %s, params = %s, time cost = %sms' % (url, str(params), (_end - _start) * 1000))
        return res

    def post(self, url, data=None, json=None, **kwargs):
        _start = time.time()
        try:
            res = requests.post(url, data, json, **kwargs)
        except Exception as e:
            e.status_code = -1
            e.text = str(e.message)
            res = e
            self.logger.error('requests.exceptions.ConnectionError. Error detail:' + str(e.message))
        _end = time.time()
        self.logger.info('remote POST call: uri = %s, json = %s, time cost = %sms' % (url, str(json), (_end - _start) * 1000))
        return res

    def put(self, url, data=None, **kwargs):
        _start = time.time()
        try:
            res = requests.put(url, data, **kwargs)
        except Exception as e:
            e.status_code = -1
            e.text = str(e.message)
            res = e
            self.logger.error('requests.exceptions.ConnectionError. Error detail:' + str(e.message))
        _end = time.time()
        self.logger.info('remote PUT call: uri = %s, data = %s, time cost = %sms' % (url, str(data), (_end - _start) * 1000))
        return res

    def delete(self, url, **kwargs):
        _start = time.time()
        try:
            res = requests.delete(url, **kwargs)
        except Exception as e:
            e.status_code = -1
            e.text = str(e.message)
            res = e
            self.logger.error('requests.exceptions.ConnectionError. Error detail:' + str(e.message))
        _end = time.time()
        self.logger.info('remote DELETE call: uri = %s, time cost = %sms' % (url, (_end - _start) * 1000))
        return res


