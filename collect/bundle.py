"""Bundle allows you to create a download bundle from a list of song ids.
Use this class to download multiple songs easily from the Malawi Music Website
"""
import os
import os.path
import zipfile
import tarfile
import time
import requests
import argparse

from io import BytesIO
from bs4 import BeautifulSoup

SONG_URL_TEMPLATE = "https://m.malawi-music.com/song.php?id={0}"
DOWNLOAD_URL_TEMPLATE = "http://m.malawi-music.com/download/index.php?song={0}"
# Headers to send to the site for it to give use binary response for
# the song download
HEADERS = {
    'Host' : 'm.malawi-music.com',
    'User-Agent' : 'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Referer': 'http://m.malawi-music.com/song.php',
    'Cookie': '__cfduid=d5e5bccadd5345e5034a6f98d552231e61497988016; __utmmobile=0x10c6f96c3ffacef6; device_id=110416851634147269; __utma=139809583.586711656.1500067253.1503340706.1503349769.5; __utmz=139809583.1500067253.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=139809583; __utmb=139809583.1.10.1503349769; __utmt=1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': "1'",
}

class Bundle(object):
    """Download Bundle from Malawi music, the bundles are
    saved to a directory specified by the `MMM_DOWNLOAD_DIR`
    environment variable or the `CWD` if that's not defined"""

    def __init__(self, name, song_ids, archive_as):
        base_dir = os.environ['MMM_DOWNLOAD_DIR'] if 'MMM_DOWNLOAD_DIR' in os.environ else '.'
        self.name = name + "-" + str(int(time.time()))
        self.dir_name = base_dir
        self.archive_name = None
        self.full_path = os.path.join(base_dir, self.name)
        self.song_ids = song_ids
        self.archive_as = archive_as
    
    def full_path(self):
        return self.full_path

    def create_bundle(self):
        # TODO(zikani): Probably wanna do this in multiple threads?
        self.create_bundle_directory()
        for song_id in self.song_ids:
            # TODO(zikani): logger.info("Downloading song with id: %s" % song_id)
            self.download_song_by_id(song_id) 
        self.create_archive()

    def create_bundle_directory(self):
        os.makedirs(self.full_path, 0o755, True)

    def download_song_by_id(self, song_id):
        # Get the song title from the song page
        r = requests.get(SONG_URL_TEMPLATE.format(song_id))
        soup = BeautifulSoup(r.text, 'html.parser')
        DOWNLOAD_PREFIX_LEN = len('Download ')
        download_name = soup.title.string[DOWNLOAD_PREFIX_LEN:]
        download_url=DOWNLOAD_URL_TEMPLATE.format(song_id)
        # logger.info("Downloading song from: ", download_url)
        song_response = requests.get(download_url, headers=HEADERS)
        filename = os.path.join(self.full_path, download_name + '.mp3')
        # Create the file
        fd = open(filename, 'w+b', 512)
        fd.write(song_response.content)
        fd.flush()
        fd.close()
        
    def create_archive(self):
        self.archive_name = "{0}.tar.gz".format(self.name)
        self.archive_path = os.path.join(self.dir_name, self.archive_name)
        with tarfile.open(self.archive_path, 'w:gz') as ar:
            for file in os.listdir(self.full_path):
                ar.add(os.path.join(self.full_path, file))

if __name__ == '__main__':
    default_dir = os.path.join('.', 'bundles')
    if 'MMM_DOWNLOAD_DIR' not in os.environ:
        os.environ['MMM_DOWNLOAD_DIR'] = default_dir
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', type=str, default=default_dir, 
                        help='Directory to place the created bundle')
    parser.add_argument('--bundle', type=str, help='Name of the created bundle')
    parser.add_argument('ids', metavar='SONG_ID', type=int, nargs='+',
                        help='Song IDs')
    
    bundle_request = None

    args = parser.parse_args()
    if args.dir:
        os.environ['MMM_DOWNLOAD_DIR'] = args.dir
    
    if args.bundle and args.ids:
        bundle_request = Bundle(args.bundle, args.ids, 'tar')
    else:
        parser.print_usage()
    
    if bundle_request is not None:
        bundle_request.create_bundle()
    