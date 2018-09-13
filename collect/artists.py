from bs4 import BeautifulSoup
import json
import sys
import requests
from api.model.artist import Artist

ARTISTS_URL = 'http://m.malawi-music.com/artists-list.php'
ARTIST_URL_TEMPLATE = 'http://m.malawi-music.com/artist.php?artist=%s'

class ArtistInfoCollector(object):
    '''Collects album information on a particular artist from
    Malawi Music website'''

    def __init__(self, artist_id):
        self.artist_id = artist_id

    
    def parse(self):
        '''Get the artist information from the artist page'''
        response = requests.get(ARTIST_URL_TEMPLATE.format(self.artist_id))
        soup = BeautifulSoup(response.text, 'html.parser')
        
        select = soup.find(id='myartist')
        

class ArtistsCollector(object):
    '''Collects artist names and urls to their profiles from Malawi Music website'''
    name = 'artists'

    def parse(self):
        response = requests.get(ARTISTS_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        select = soup.find(id='myartist')
        
        if select is None:
            exit()

        artists = []
        for opt in select.find_all('option'):
            artists.append({
                'artist': opt.string,
                'artist_url': opt.attrs['value'],
            })
        
        return artists

if __name__ == '__main__':
    ac = ArtistsCollector()

    artists = []
    for artist in ac.parse():
        info_collector = ArtistInfoCollector(artist.artist_id)
        d = info_collector.parse()
        artists.append(Artist(
            id = artist.artist,
            name = artist.artist,
            real_name = artist.artist,
            biography = d['biography'] or None,
            city = d['city'] or None,
            country = None,
            profile_pic = d['profile_pic_url'] or None,
            registered_on = datetime.now(),
            website = d['website_url'] or None,
            artist_url = artist.artist_url,
            genres = d['genres'] or None,
            albums = None
        ))
    
    for a in artists: 
        Artist.insert_or_update(a)
    
    # json.dump(ac.parse(), sys.stdout)