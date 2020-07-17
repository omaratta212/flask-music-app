# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#


from flask import Flask, render_template
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from models import db
from helpers import format_datetime

# Import models controllers
from controllers.venue_controller import create_venue_form, create_venue_submission, venues, show_venue, edit_venue, \
    edit_venue_submission, delete_venue, search_venues
from controllers.artist_controller import create_artist_form, create_artist_submission, artists, show_artist, \
    edit_artist, edit_artist_submission, delete_artist, search_artists
from controllers.shows_controller import create_shows, create_show_submission, shows, search_shows

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)
toolbar = DebugToolbarExtension(app)
app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# App Routes & Controllers.
# Didn't use decorators to be able to separate controllers in other files without blueprints or circular imports.
# ----------------------------------------------------------------------------#
@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues Routes
#  ----------------------------------------------------------------
app.add_url_rule('/venues/create', 'create_venue_form', create_venue_form, methods=['GET'])
app.add_url_rule('/venues/create', 'create_venue_submission', create_venue_submission, methods=['POST'])
app.add_url_rule('/venues', 'venues', venues)
app.add_url_rule('/venues/<int:venue_id>', 'show_venue', show_venue)
app.add_url_rule('/venues/<int:venue_id>/edit', 'edit_venue', edit_venue, methods=['GET'])
app.add_url_rule('/venues/<int:venue_id>/edit', 'edit_venue_submission', edit_venue_submission, methods=['POST'])
app.add_url_rule('/venues/<venue_id>/delete', 'delete_venue', delete_venue, methods=['POST'])
app.add_url_rule('/venues/search', 'search_venues', search_venues, methods=['POST'])

#  Artists Routes
#  ----------------------------------------------------------------
app.add_url_rule('/artists/create', 'create_artist_form', create_artist_form, methods=['GET'])
app.add_url_rule('/artists/create', 'create_artist_submission', create_artist_submission, methods=['POST'])
app.add_url_rule('/artists', 'artists', artists)
app.add_url_rule('/artists/<int:artist_id>', 'show_artist', show_artist)
app.add_url_rule('/artists/<int:artist_id>/edit', 'edit_artist', edit_artist, methods=['GET'])
app.add_url_rule('/artists/<int:artist_id>/edit', 'edit_artist_submission', edit_artist_submission, methods=['POST'])
app.add_url_rule('/artists/<artist_id>/delete', 'delete_artist', delete_artist, methods=['POST'])
app.add_url_rule('/artists/search', 'search_artists', search_artists, methods=['POST'])

#  Shows Routes
#  ----------------------------------------------------------------
app.add_url_rule('/shows/create', 'create_shows', create_shows, methods=['GET'])
app.add_url_rule('/shows/create', 'create_show_submission', create_show_submission, methods=['POST'])
app.add_url_rule('/shows', 'shows', shows)
app.add_url_rule('/shows/search', 'search_shows', search_shows, methods=['POST'])


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
