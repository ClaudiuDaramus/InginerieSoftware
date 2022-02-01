class MediaEntry:
    def __init__(self, media_details):
        self.rated = media_details["Rated"]
        self.runtime = int(media_details["Runtime"].split(' min')[0])
        self.genres = [elem.lower() for elem in media_details['Genre'].split(',')]
        self.director = media_details['Director']
        self.writers = [elem.lower() for elem in media_details['Writer'].split(',')]
        self.actors = [elem.lower() for elem in media_details['Actors'].split(',')]
        self.languages = [elem.lower() for elem in media_details['Language'].split(',')]
        self.countries = [elem.lower() for elem in media_details['Country'].split(',')]
        self.typeOfMedia = media_details['Type']
        self.production = [elem.lower() for elem in media_details['Production'].split(',')] if media_details.get('Production') else []
        self.imdbRating = float(media_details['imdbRating'])

    def format_as_dictionary(self):
        if self is None:
            raise Exception('Method needs one parameter')
        return {
            'rated': self.rated,
            'runtime': self.runtime,
            'genres': self.genres,
            'director': self.director,
            'writers': self.writers,
            'actors': self.actors,
            'languages': self.languages,
            'countries': self.countries,
            'typeOfMedia': self.typeOfMedia,
            'production': self.production,
            'imdbRating': self.imdbRating
        }