from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

#  Venue Relationships abstract
#  2. Venue has many shows
#  ----------------------------------------------------------------
class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))

    genres = db.Column(db.ARRAY(db.String))
    shows = db.relationship('Show', backref='venue', lazy=True)

    def __repr__(self):
        return f' <Venue ID: {self.id}, Name: {self.name}, City: {self.city}, State: {self.state} \n'

    # Fat models
    @property
    def past_shows(self):
        return list(filter(lambda show: show.start_time < datetime.now(), self.shows))

    @property
    def upcoming_shows(self):
        return list(filter(lambda show: show.start_time >= datetime.now(), self.shows))

    @property
    def past_shows_count(self):
        return len(self.past_shows)

    @property
    def upcoming_shows_count(self):
        return len(self.upcoming_shows)


#  Artist Relationships abstract
#  2. Artist has many shows.
#  ----------------------------------------------------------------
class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(120))

    genres = db.Column(db.ARRAY(db.String))
    shows = db.relationship('Show', backref='artist', lazy=True)

    def __repr__(self):
        return f' <Artist ID: {self.id}, Name: {self.name}, City: {self.city}, State: {self.state} \n'

    # Fat models
    @property
    def past_shows(self):
        return list(filter(lambda show: show.start_time < datetime.now(), self.shows))

    @property
    def upcoming_shows(self):
        return list(filter(lambda show: show.start_time >= datetime.now(), self.shows))

    @property
    def past_shows_count(self):
        return len(self.past_shows)

    @property
    def upcoming_shows_count(self):
        return len(self.upcoming_shows)


#  Show Relationships abstract
#  1. Show has one Artist.
#  2. Show has one Venue.
#  ----------------------------------------------------------------
class Show(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)

    def __repr__(self):
        return f' <Show ID: {self.id}, Time: {self.start_time_string} \n'

    # Fat models
    @property
    def venue_name(self):
        return self.venue.name

    @property
    def artist_name(self):
        return self.artist.name

    @property
    def artist_image_link(self):
        return self.artist.image_link
