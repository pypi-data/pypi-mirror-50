from __future__ import absolute_import
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
app = Celery('contact')


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
