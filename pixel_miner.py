#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

is_py2 = sys.version_info < (3, 0)

if is_py2:
    from Queue import Queue
else:
    from queue import Queue
from threading import Thread
import os
import colorlog
from downloaders import download_image

class Worker(Thread):

    """A worker"""

    def __init__(self, tasks, worker_name='Worker'):
        """Initializes an asynchronous worker

        :tasks: TODO

        """
        Thread.__init__(self)

        self.logger = colorlog.getLogger(worker_name)

        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kwargs = self.tasks.get()
            try:
                self.logger.info('Downloading: ' + args[0])
                func(*args, **kwargs)
            except Exception as e:
                self.logger.warning('Encountered error: ' + str(e))
            finally:
                self.tasks.task_done()

class PixelMiner():

    """A class which asynchronously downloads images from a queue of URLS"""

    def __init__(self, n_concurrent, subreddits):
        """Initializes a PixelMiner instance

        :n_concurrent: The number of concurrent downloads

        """
        colorlog.basicConfig(level='INFO')

        handler = colorlog.StreamHandler()
        handler.setFormatter(colorlog.ColoredFormatter('%(log_color)s%(levelname)s:%(name)s:%(message)s'))
        self.logger = colorlog.getLogger('PixelMiner')
        #self.logger.addHandler(handler)

        self.tasks = Queue(n_concurrent)
        for n in range(n_concurrent):
            Worker(self.tasks, worker_name='Worker %d' % n)

        if not isinstance(subreddits, list):
            subreddits = [subreddits]

        for subreddit in subreddits:
            thread_path = 'images/' + subreddit
            if not os.path.exists(thread_path):
                os.makedirs(thread_path)

    def add_url(self, url, subreddit):
        filepath = 'images/' + subreddit
        self.logger.info('Queuing: ' + url + ' from ' + subreddit)
        self.add_task(download_image, url, filepath)

    def add_task(self, func, *args, **kwargs):
        self.tasks.put((func, args, kwargs))

    def wait_completion(self):
        self.tasks.join()
