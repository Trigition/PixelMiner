#!/usr/bin/env python
# -*- coding: utf-8 -*-
import praw
import argparse
import re
import logging
from pixel_miner import PixelMiner

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--cred', type=str, help='A credential file holding PixelMiner\'s tokens')
parser.add_argument('-r', '--rthread', type=str, nargs='+', help='The subreddit(s) you wish to parse')

args = parser.parse_args()
logging.basicConfig(level=logging.INFO)

# Load configuration
cred = dict(
        [re.match(r'^(.+)=(.+)$', l.strip()).groups() for l in open(args.cred, 'rt')]
)

reddit = praw.Reddit(**cred)

miner = PixelMiner(3, args.rthread)
threads = '+'.join(args.rthread)

logging.info('Initializing')
for submission in reddit.subreddit(threads).stream.submissions():
    url = str(submission.url)
    miner.add_url(url, str(submission.subreddit).lower())

miner.wait_completion()
logging.info('Finished.')
