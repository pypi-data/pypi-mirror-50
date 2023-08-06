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

from celery import Celery

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
