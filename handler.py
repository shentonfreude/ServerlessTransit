import json
import logging

import boto3
from boto3.dynamodb.types import TypeDeserializer


LOG = logging.getLogger(__name__)


def _ddb_deserialize(ddb_data):
    return {k: TypeDeserializer().deserialize(v) for k, v in ddb_data.items()}


def dynamodb_event(event, context):
    print(f'### event={event}')
    for rec in event['Records']:
        # TODO ensure INSERT as that's all we expect now
        data = _ddb_deserialize(rec['dynamodb']['NewImage'])
        print(f'### DATA={data}')
        pk = data['pk']
        if pk.startswith('report:'):
            _report(data)
        elif pk.startwith('incident:'):
            _incident(data)
        elif pk.startswith('subscriber:'):
            _subscriber(data)
        else:
            LOG.error(f'unrecognized pk={pk} data={data}')

def _report(data):
    """search DB for same line within last 30 minutes if found, create incident record."""
    print(f'### Got a report! data={data}')
    # TODO: search DB for same line within last 30 minutes
    # if found, create incident.

def _incident(data):
    """Call a functino to query the DB to find interested subscribers and send SNS."""
    print(f'### Not yet processing incident data.')

def _subscriber(data):
    # do we ever want to process subscribers?
    print(f'### Not yet processing subscriber data.')




if __name__ == '__main__':
    """Silly way to test."""
    event = json.loads(open('event-report.json').read())
    dynamodb_event(event, None)
