"""
Interface to push messages to mbf-lambda-notify system.

Error codes:
    * 1001 - myonotify queue name is not registered within ENV variables.
             It's expected to have queue name registered under
             `MYONOTIFY-QUEUE-NAME` key.
    * 1002 - not able to connect to SQS queue
    * 1003 - can't *push* message to SQS queue
"""

import json
import os
from datetime import datetime
import boto3


SQS_QUEUE_NAME = os.environ.get('MYONOTIFY_QUEUE_NAME')


class NotifyException(Exception):
    pass


def _get_sqs_queue():
    if not SQS_QUEUE_NAME:
        raise NotifyException(
            '[err #1001] myonotify SQS queue name is not registered within env'
        )

    sqs = boto3.resource('sqs')

    try:
        return sqs.get_queue_by_name(QueueName=SQS_QUEUE_NAME)
    except Exception:
        return None


def notify(message, channel='default'):
    """
    Args:
        message (str): notification text
        channel (str): notification channel to which message will be pushed
    """
    sqs_queue_handler = _get_sqs_queue()
    if not sqs_queue_handler:
        raise NotifyException('[err #1002] Cant reach SQS')

    msg = {
        'channel': channel,
        'message': message,
        'timestamp': datetime.now().isoformat()
    }

    try:
        sqs_queue_handler.send_message(MessageBody=json.dumps(msg))
    except Exception:
        raise NotifyException('[err #1003] Cant push msg to SQS')
