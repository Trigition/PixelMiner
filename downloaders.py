import re
import requests
import logging
import wget
from hashlib import sha256

def download_image(url, filepath):
    """Downloads an image, the output filepath is a hash of the url

    :url: The url to download
    :returns: The filename. If an error occured or the url passed does not
    point to an image, None is returned

    """
    check = r'[^/\\&\?]+\.\w{3,4}(?=([\?&].*$|$))'
    match = re.search(check, url)
    if match:
        filename = wget.filename_from_url(url)
        if filepath[-1] != '/':
            filepath += '/'

        logging.info('Downloading: ' + url + ' -> ' + filepath)
        wget.download(url, filepath + filename, bar=lambda current, total, width: None)
        logging.info('Finished: ' + url)
        return filename

    return None
