"""
  Copyright (c) 2017-2018 Atrio, Inc.

  All rights reserved.
"""

ruote = {
    'users': {
        'me': {},
        ':id': {}
    },
    'sso': {
        'token_by_email': {},
        'providers': {},
    },
    'clusters': {
        ':id': {}
    },
    'AWSclusters': {
        ':id': {}
    },
    'queues': {
        ':id': {}
    },
    'files': {
        '__attrs_files': ['file'],
        ':id': {
            'upload': {},
            'download': {},
        },
    },
    'jobs': {
        ':id': {
            'stdout': {},
            'stderr': {},
            'log': {},
            'perf': {},
            'telemetry': {},
            'advisor': {},
        }
    },
    'jobs-by-uuid': {
        ':uuid': {
            'query': {},
        }
    },
    'apps': {
        ':id': {
            'ranking': {},
        }
    },
    'payment-sources': {
        ':amount': {},
    },
}
virgo = {
    'build': {
        '__attrs_files': ['file'],
        ':id': {
            'log': {},
        },
    },
}
