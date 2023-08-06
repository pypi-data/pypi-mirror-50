import boto3
import logging
from datetime import datetime


class CloudwatchLogHandler(logging.Handler):
    def __init__(self, stream_name, level):
        logging.Handler.__init__(self, level)
        self.group_name = 'CloudLogger'
        self.stream_name = stream_name
        self.client = boto3.client('logs')

    def emit(self, record):
        args = {'logGroupName': self.group_name,
                'logStreamName': self.stream_name,
                'logEvents': [{'timestamp': int(datetime.now().timestamp() * 1000), 'message': self.format(record)}],
                }
        token = self.get_token()
        if token is not None:
            args['sequenceToken'] = token
        resp = self.client.put_log_events(**args)
        if 'rejectedLogEventsInfo' in resp:
            print(resp)

    def get_token(self):
        try:
            resp = self.client.describe_log_streams(logGroupName=self.group_name, logStreamNamePrefix=self.stream_name)
            return resp['logStreams'][0]['uploadSequenceToken'] if 'uploadSequenceToken' in resp['logStreams'][0] else None
        except IndexError:
            # Stream doesn't exist
            self.client.create_log_stream(logGroupName=self.group_name, logStreamName=self.stream_name)
            return None


class CloudwatchLogger:
    def __init__(self, stream_name):
        self.group_name = 'CloudLogger'
        self.stream_name = stream_name
        self.client = boto3.client('logs')
        self.logger = logging.getLogger("Cloudwatch")
        handler = CloudwatchLogHandler(self.stream_name, logging.INFO)
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S'))
        self.logger.setLevel(10)
        # lambda loggers can persist through separate executions so clear out the handlers to prevent duplicates
        self.logger.handlers = []
        self.logger.addHandler(handler)
