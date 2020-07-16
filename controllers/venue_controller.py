from app import app
from models import db, Venue
from flask import render_template, request, flash, redirect, url_for
from forms import *
from helpers import safe_commit


#  Get Create Venue Form
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

#  Create Venue
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    new_venue = Venue(
        name=request.form.get('name'),
        city=request.form.get('city'),
        state=request.form.get('state'),
        address=request.form.get('address'),
        phone=request.form.get('phone'),
        genres=request.form.getlist('genres'),
        image_link=request.form.get('image_link'),
        facebook_link=request.form.get('facebook_link'),
        website=request.form.get('facebook_link'),
        seeking_talent=request.form.get('seeking_talent') == 'y',
        seeking_description=request.form.get('seeking_description'),
    )

    db.session.add(new_venue)
    if safe_commit():
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
    else:
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')

    return render_template('pages/home.html')


#  List Venues
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():
    # Get all venues once to avoid multiple db queries, ordered to optimize for the next step
    venues = Venue.query.order_by('city', 'state').all()

    # Using a set to create non-duplicated location tuples of city and state
    locations = set()
    for venue in venues:
        locations.add(
            (venue.city, venue.state)
        )

    data = []
    for location in locations:
        # Filter venues list where a venue has the current location (city & state)
        location_venues = list(
            filter(lambda venue_item: (venue_item.city == location[0]) and (venue_item.state == location[1]), venues))

        # Append the new location & it's venues to the data list
        data.append({
            "city": location[0],
            "state": location[1],
            "venues": location_venues
        })

    return render_template('pages/venues.html', areas=data)


#  Show Venue
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    return render_template('pages/show_venue.html', venue=venue)


#  Get Update Venue form
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = Venue.query.get_or_404(venue_id)

    # Loop over the form fields & populate the data if available
    for attr in form:
        if hasattr(venue, attr.name):
            attr.data = getattr(venue, attr.name)
    return render_template('forms/edit_venue.html', form=form, venue=venue)

#  Update Venue
#  ----------------------------------------------------------------
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    venue = Venue.query.get(venue_id)

    # Update the venue object
    venue.name = request.form.get('name')
    venue.city = request.form.get('city')
    venue.state = request.form.get('state')
    venue.address = request.form.get('address')
    venue.phone = request.form.get('phone')
    venue.genres = request.form.getlist('genres')
    venue.image_link = request.form.get('image_link')
    venue.facebook_link = request.form.get('facebook_link')
    venue.website = request.form.get('facebook_link')
    venue.seeking_talent = request.form.get('seeking_talent') == 'y'
    venue.seeking_description = request.form.get('seeking_description')

    # Safely commit the changes to the db
    if safe_commit():
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
    else:
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')

    return redirect(url_for('show_venue', venue_id=venue_id))


#  Delete Venue
#  ----------------------------------------------------------------
@app.route('/venues/<venue_id>/delete', methods=['POST']) # Changed request type to handle the redirection on backend
def delete_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    name  = venue.name
    db.session.delete(venue)

    # Safely commit the changes to the db
    if safe_commit():
        flash('Venue ' + name + ' was successfully deleted!')
    else:
        flash('The Venue has a show or more.'  + name + ' could not be deleted.')

    return redirect(url_for('venues'))


#  Search Venue
#  ----------------------------------------------------------------
@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', '')
    results = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()

    response = {
        "count": len(results),
        "data": results
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))
