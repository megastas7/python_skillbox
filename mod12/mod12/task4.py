import logging
from datetime import datetime
import time
from threading import Thread
import requests

url = 'http://127.0.0.1:8080/timestamp/'

logging.basicConfig(
    filename='timestamp.log', filemode='w',
    format="%(threadName)s %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_timestamp():
    for _ in range(20):
        current = datetime.now().timestamp()
        result = requests.get(url + str(current))
        logger.info(f"{current} {result.text}")
        time.sleep(1)


if __name__ == '__main__':
    start = time.time()
    threads = [Thread(target=get_timestamp) for _ in range(10)]
    for t in threads:
        t.start()
        time.sleep(1)

    for t in threads:
        t.join()
    print(f'время- {time.time()-start}')
