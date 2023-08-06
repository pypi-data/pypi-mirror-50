import os
import datetime
import logging
from tools_examples.scheduler import scheduler
from gmail_forwarding.functions import init_sender, update_timestamp, \
    update_subscribers, listen_and_deliver, add_subscribers


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.WARNING)


def run_once(sender, sender_path, init_timestamp=False):
    logging.warning(f"Running - {str(datetime.datetime.now())}")
    s = sender, sender_path
    if not os.path.isdir(sender_path):
        init_sender(*s)
        if init_timestamp:
            update_timestamp(*s)
    else:
        update_subscribers(sender_path)
        listen_and_deliver(*s)
        update_timestamp(*s)
        logging.info(f"Waiting {str(datetime.datetime.now())}")


def run_process(sender, send_first=False):
    sender_path = os.path.join(os.getcwd(), sender)
    s = sender, sender_path

    def update():
        run_once(*s, init_timestamp=not send_first)

    scheduler.add_job(update, 'interval', hours=1)
    scheduler.start()


def run_one_shot(sender, subscribers):
    sender_path = os.path.join(os.getcwd(), sender)
    s = sender, sender_path
    run_once(*s, init_timestamp=False)
    add_subscribers(sender_path, subscribers)
    run_once(*s)
