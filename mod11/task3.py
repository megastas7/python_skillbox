import logging
import random
import threading
import time

TOTAL_TICKETS = 10
ALL_PLACES = 20
MAX_TICKETS_ON_STATIONS = 10

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Seller(threading.Thread):

    def __init__(self, semaphore: threading.Semaphore, lock: threading.Lock):
        super().__init__()
        self.sem = semaphore
        self.lock = lock
        self.tickets_sold = 0
        logger.info('Seller started work')

    def run(self):
        global TOTAL_TICKETS
        global ALL_PLACES
        is_running = True
        while is_running:
            self.random_sleep()
            with self.lock:
                if TOTAL_TICKETS <= 4:
                    logger.info('Director is printing tickets...')
                    self.wait_five_seconds()
                    logger.info('Director added tickets up to 10')
                    TOTAL_TICKETS += MAX_TICKETS_ON_STATIONS - TOTAL_TICKETS

            with self.sem:
                if ALL_PLACES <= 0:
                    logger.info('All places are taken')
                    break

                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                ALL_PLACES -= 1
                logger.info(f'{self.name} sold one; {TOTAL_TICKETS} left; free places- {ALL_PLACES}')

        logger.info(f'Seller {self.name} sold {self.tickets_sold} tickets')

    def random_sleep(self):
        time.sleep(random.randint(0, 1))

    def wait_five_seconds(self):
        time.sleep(5)


def main():
    semaphore = threading.Semaphore()
    lock = threading.Lock()
    sellers = []

    for _ in range(4):
        seller = Seller(semaphore, lock)
        seller.start()
        sellers.append(seller)

    for seller in sellers:
        seller.join()


if __name__ == '__main__':
    main()
