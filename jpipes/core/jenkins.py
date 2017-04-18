
import re
import requests


class JenkinsAPI(object):
    def __init__(self, base, auth=None, debug=False):
        self.base = base
        self.session = requests.Session()
        self.debug = debug
        if auth is not None:
            self.session.auth = auth

    def get(self, path):
        path = re.sub(self.base, '', path)
        if self.debug is True:
            print("GET: %s/%s" % (self.base, path))
        return self.session.get("%s/%s" % (self.base, path))

    def post(self, path, data={}):
        path = re.sub(self.base, '', path)
        if self.debug is True:
            print("POST: %s/%s - data:%s" % (self.base, path, data))
        return self.session.post("%s/%s" % (self.base, path), data=data)
