"""
REDIS_URL = 'redis://{}:{}/{}'.format('host', 'port', db)
BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = SQLALCHEMY_URI

you should run celery like that in command shell:
../venv/bin/python -m pip install celery pymongo jsonschema
../venv/bin/python -m celery -A async_task --loglevel=info worker -b $REDIS_URL ---result-backend xxx
--result-backend $SQLALCHEMY_URL -Q notification,celery
"""

from __future__ import absolute_import

from functools import wraps

from celery import Celery
from celery.bin.celery import CeleryCommand


def hook_commandline(func):
    @wraps(func)
    def wrap(self, *args, **kwargs):
        argv = args[1]
        exclude_own_defined = lambda x: not x.startswith('--mongo_pwd') \
                                        and not x.startswith('--ding_robot')
        args = (args[0], list(filter(exclude_own_defined, argv)))
        return func(self, *args, **kwargs)

    return wrap


CeleryCommand.execute = hook_commandline(CeleryCommand.execute)

app = Celery('blueCup')
app.config_from_object('blueCup.conf')


def generate_celery(broker: str,
                    result_backend: str = '',
                    main: str = 'blueCup',
                    conf: str = 'blueCup.conf') -> Celery:
    result_backend = result_backend or broker
    celery = Celery(main=main)
    celery.config_from_object(conf)
    celery.add_defaults({
        'BROKER_URL': broker,
        'CELERY_RESULT_BACKEND': result_backend,
    })
    return celery
