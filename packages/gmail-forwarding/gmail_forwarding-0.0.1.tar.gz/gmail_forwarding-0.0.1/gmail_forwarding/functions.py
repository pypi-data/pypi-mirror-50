import os
import base64
import email
import logging
from gmail_forwarding.constants import *
from tools_examples.gmail_service import service, user_id
from gmail_forwarding.gmail_message import ListMessagesMatchingQuery, GetMessage


def init_sender(sender, sender_path):
    os.mkdir(sender_path)
    last_time = get_timestamp(sender_path)
    with open(os.path.join(sender_path, timestamp_file), 'w+') as f:
        f.write(str(int(last_time)))

    with open(os.path.join(sender_path, key_file), 'w+') as f:
        f.write(sender + sub_key + '\n')
        f.write(sender + unsub_key + '\n')

    open(os.path.join(sender_path, subscribers_file), 'w+').close()


def update_timestamp(sender, sender_path):
    timestamp = get_ref_timestamp(sender_path)
    new_timestamp = get_timestamp(sender, timestamp=timestamp)
    set_ref_timestamp(sender_path, new_timestamp)
    logging.info(f"Old Timestamp {timestamp}")
    logging.info(f"New Timestamp {new_timestamp}")


def get_ref_timestamp(sender_path):
    with open(os.path.join(sender_path, timestamp_file)) as f:
        try:
            return int(f.readline())
        except ValueError:
            return None


def set_ref_timestamp(sender_path, timestamp):
    with open(os.path.join(sender_path, timestamp_file), 'w+') as f:
        f.write(str(int(timestamp)))


def get_timestamp(sender, timestamp=None):
    msgs = list_messages(sender, timestamp)
    if len(msgs) == 0:
        return timestamp if timestamp is not None else 0
    # print(len(msgs), msgs[-1])
    # print(len(msgs), msgs[0])
    # print(GetMessage(service=service, user_id=user_id,
    #                  msg_ids=[msgs[0]['id']]))
    # print(GetMessage(service=service, user_id=user_id,
    #                  msg_ids=[msgs[0]['id']]
    #                  )[0]['internalDate'])
    # print(GetMessage(service=service, user_id=user_id,
    #                  msg_ids=[msgs[-1]['id']]
    #                  )[0]['internalDate'])
    return int(GetMessage(service=service, user_id=user_id,
                          msg_ids=[msgs[0]['id']]
                          )[0]['internalDate']
               ) // 1000


def list_messages(sender, timestamp):
    query = "from:{}".format(sender)
    if timestamp is not None:
        query += " after:{}".format(str(timestamp + 10))  # don't get the last one
    mmm = ListMessagesMatchingQuery(service=service,
                                    user_id=user_id,
                                    q=query)
    logging.info(f"ListMsg {str(len(mmm))}")
    return mmm


def get_stamped_mime_messages(sender, sender_path):
    msgs = list_messages(sender, get_ref_timestamp(sender_path))
    if len(msgs) == 0:
        return []

    msgs_content = GetMessage(service=service, user_id=user_id,
                              msg_ids=[m['id'] for m in msgs],
                              format="raw"
                              )

    logging.info(f"Mime {str(len(msgs_content))}")
    mime_msgs = []
    for m in msgs_content:
        msg_str = base64.urlsafe_b64decode(m['raw'].encode('ASCII'))
        mime_msg = email.message_from_bytes(msg_str)

        mime_msgs.append(mime_msg)
    return mime_msgs


def get_key(sender_path):
    with open(os.path.join(sender_path, key_file)) as f:
        sender_sub_key = str(f.readline())
        sender_unsub_key = str(f.readline())
    return sender_sub_key, sender_unsub_key


def get_subscribers(sender_path):
    with open(os.path.join(sender_path, subscribers_file)) as f:
        subscribers = set(u for u in f.readlines())
    return subscribers


def set_subscribers(sender_path, subscribers):
    with open(os.path.join(sender_path, subscribers_file)) as f:
        for s in subscribers:
            f.write(s + "\n")


def add_subscribers(sender_path, subscribers):
    with open(os.path.join(sender_path, subscribers_file), 'a') as f:
        if isinstance(subscribers, str):
            f.write(subscribers + "\n")
        else:
            for s in subscribers:
                f.write(s + "\n")


def update_subscribers(sender_path):
    timestamp = get_ref_timestamp(sender_path)
    sender_sub_key, sender_unsub_key = get_key(sender_path)
    subscribers = get_subscribers(sender_path)

    query = '{} OR {}'.format(sender_sub_key, sender_unsub_key)
    if timestamp is not None:
        query += " after:{}".format(str(timestamp))
    msgs = ListMessagesMatchingQuery(service=service,
                                     user_id=user_id,
                                     q=query)
    if len(msgs) == 0:
        return

    msgs_content = GetMessage(service=service, user_id=user_id,
                              msg_ids=[m['id'] for m in msgs],
                              format="metadata",
                              metadataHeaders=['From']
                              )

    for m in msgs_content:
        snip = m['snippet']
        one_sender = m['payload']['headers'][0]['value']
        if sub_key in snip:
            subscribers.add(one_sender)
        if unsub_key in snip:
            subscribers.remove(one_sender)
    set_subscribers(sender_path, subscribers)


def listen_and_deliver(sender, sender_path):
    msgs = get_stamped_mime_messages(sender, sender_path)
    if not msgs:
        return
    subscribers = get_subscribers(sender_path)
    if not subscribers:
        return
    for m in msgs:
        m['To'] = ', '.join(subscribers)
        message = {'raw': base64.urlsafe_b64encode(m.as_bytes()).decode()}
        message_ = service.users().messages().send(userId=user_id, body=message).execute()
        logging.info(str(message_))
    logging.info("Done")
