import pynng
import json


class DataFeeds(object):

    def __init__(self, pub, univ):

        self.pub_port = pub
        self.univ = univ
        self.data = dict()

    def run(self):

        pub = pynng.Pub0(listen=f'tcp://*:{self.pub_port}')
        pub.close()
