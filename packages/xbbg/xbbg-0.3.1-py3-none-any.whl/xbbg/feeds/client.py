import pynng
import json
import trio
import fire

BROKDER_PORT = 9224


class DataClient(object):

    def __init__(self, sub=BROKDER_PORT):

        self.sub_port = sub
        self.data = dict()

    async def run(self):

        sub_url = f'tcp://localhost:{self.sub_port}'
        sub = pynng.Sub0(dial=sub_url)
        sub.subscribe(b'')
        print(f'[{DataClient.__name__}] Subscribing to {sub_url} ...')
        try:
            while True:
                try:
                    raw = await sub.arecv()
                    data = json.loads(raw.decode('utf-8'))
                    print(data)
                    self.data.update(data)
                except KeyboardInterrupt: break
        finally: sub.close()


def run_client(**kwargs):

    dc = DataClient(**kwargs)
    trio.run(dc.run)


if __name__ == '__main__':

    fire.Fire(run_client)
