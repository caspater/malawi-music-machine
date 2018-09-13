
class Artist:
    
    def __init__(self, name, url):
        self.id = None
        self.name = name
        self.real_name = None
        self.biography = None
        self.city = None
        self.country = None
        self.profile_pic = None
        self.registered_on = None
        self.website = None
        self.artist_url = url
        self.genres = None
        self.albums = None

    def as_compact(self):
        return dict(
            id=self.id,
            name=self.name,
            artist_url=self.artist_url,
            profile_pic=self.profile_pic
        )