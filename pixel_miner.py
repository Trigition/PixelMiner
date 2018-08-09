#!/usr/bin/env python
# -*- coding: utf-8 -*-
from queue import Queue
from threading import Thread
import os
import logging
from downloaders import download_image

class Worker(Thread):

    """A worker"""

    def __init__(self, tasks):
        """Initializes an asynchronous worker

        :tasks: TODO

        """
        Thread.__init__(self)

        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kwargs = self.tasks.get()
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(e)
            finally:
                self.tasks.task_done()

class PixelMiner():

    """A class which asynchronously downloads images from a queue of URLS"""

    def __init__(self, n_concurrent, subreddits):
        """Initializes a PixelMiner instance

        :n_concurrent: The number of concurrent downloads

        """
        self.tasks = Queue(n_concurrent)
        for _ in range(n_concurrent):
            Worker(self.tasks)

        if not isinstance(subreddits, list):
            subreddits = [subreddits]

        for subreddit in subreddits:
            thread_path = 'images/' + subreddit
            if not os.path.exists(thread_path):
                os.makedirs(thread_path)

    def add_url(self, url, subreddit):
        filepath = 'images/' + subreddit
        logging.info('Queuing: ' + url + ' from ' + subreddit)
        self.add_task(download_image, url, filepath)

    def add_task(self, func, *args, **kwargs):
        self.tasks.put((func, args, kwargs))

    def wait_completion(self):
        self.tasks.join()
