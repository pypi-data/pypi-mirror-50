import boto3
import logging
import os
import json
import sys
import fcntl
from datetime import datetime


class SQSLogHandler(logging.Handler):
    def __init__(self, queue, level):
        logging.Handler.__init__(self, level)
        self.queue = queue

    def emit(self, record):
        group = 'default'
        if hasattr(record, 'name'):
            group = record.name.replace(" ", "_")
        self.queue.send_message(MessageBody=json.dumps(record.__dict__), MessageGroupId=group)


class SQSLogger:
    def __init__(self, queue_name="Logs.fifo"):
        self.queue = boto3.resource("sqs").get_queue_by_name(QueueName=queue_name)
        handler = SQSLogHandler(self.queue, logging.INFO)
        self.logger = logging.getLogger("SQS")
        self.logger.setLevel(10)
        self.logger.addHandler(handler)
        self.formatter = logging.Formatter('[%(name)s] %(asctime)s - %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')

    def consume(self, name=None):
        print("Press Enter to stop consuming.")
        fl = fcntl.fcntl(sys.stdin.fileno(), fcntl.F_GETFL)  # Some magic that lets us continue reading until
        fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, fl | os.O_NONBLOCK)  # the user presses enter
        while True:
            resp = self.queue.receive_messages(MaxNumberOfMessages=1, AttributeNames=['MessageGroupId'])
            if len(resp) > 0:
                message = resp[0]
                record = json.loads(resp[0].body)
                groupId = message.attributes['MessageGroupId']
                # TODO: use logging formatter (self.formatter) rather than % formatting)
                if name is not None:
                    if groupId == name.replace(" ", "_"):
                        print("[%s] %s - %s: %s" % (groupId,
                                                    datetime.utcfromtimestamp(record['created']).strftime(
                                                        '%Y-%m-%d %H:%M:%S'),
                                                    record['levelname'], record['msg']))
                        message.delete()
                else:
                    print("[%s] %s - %s: %s" % (groupId,
                                                datetime.utcfromtimestamp(record['created']).strftime(
                                                    '%Y-%m-%d %H:%M:%S'),
                                                record['levelname'], record['msg']))
                    message.delete()
            try:
                if sys.stdin.read():
                    sys.stdout.write("\r")
                    break
            except IOError:
                pass
            except TypeError:
                pass

    def purge(self):
        self.queue.purge()
