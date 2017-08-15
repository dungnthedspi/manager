from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

from rq import Queue
from redis import Redis
conn = Redis()

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
        print worker