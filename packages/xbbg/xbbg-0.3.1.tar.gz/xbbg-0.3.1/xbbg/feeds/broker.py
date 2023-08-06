import pynng
import trio
import fire

BROKDER_PORT = 9224


async def pubsub_serv(pub, sub):

    while True:
        data = await sub.arecv()
        print(data)
        await pub.asend(data=data)


class Broker(object):

    def __init__(self, sub, pub=BROKDER_PORT):

        self.sub_port = sub
        self.pub_port = pub

    async def run(self):

        if not self.sub_port: return

        pub_url = f'tcp://*:{self.pub_port}'
        pub = pynng.Pub0(listen=pub_url)
        print(f'[{Broker.__name__}] Publishing to {pub_url} ...')

        subs = []
        for dial in self.sub_port:
            dial_url = f'tcp://localhost:{dial}'
            sub = pynng.Sub0(dial=dial_url)
            sub.subscribe(b'')
            print(f'[{Broker.__name__}] Subscribing to {dial_url} ...')
            subs.append(sub)

        try:
            while True:
                try:
                    async with trio.open_nursery() as nursery:
                        for sub in subs:
                            nursery.start_soon(pubsub_serv, pub, sub)
                except pynng.Timeout: pass
                except KeyboardInterrupt: break
        finally:
            pub.close()
            for sub in subs: sub.close()


def run_broker(**kwargs):

    brk = Broker(**kwargs)
    trio.run(brk.run)


if __name__ == '__main__':

    fire.Fire(run_broker)
