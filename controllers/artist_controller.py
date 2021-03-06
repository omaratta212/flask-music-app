from models import db, Artist
from flask import render_template, request, flash, redirect, url_for
from forms import *
from helpers import safe_commit


#  Get Create Artist From
#  ----------------------------------------------------------------
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


#  Create Artist
#  ----------------------------------------------------------------
def create_artist_submission():
    new_artist = Artist(
        name=request.form.get('name'),
        city=request.form.get('city'),
        state=request.form.get('state'),
        phone=request.form.get('phone'),
        genres=request.form.getlist('genres'),
        image_link=request.form.get('image_link'),
        facebook_link=request.form.get('facebook_link'),
        website=request.form.get('facebook_link'),
        seeking_venue=request.form.get('seeking_venue') == 'y',
        seeking_description=request.form.get('seeking_description'),
    )

    db.session.add(new_artist)
    if safe_commit():
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
    else:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')

    return render_template('pages/home.html')


#  List Artists
#  ----------------------------------------------------------------
def artists():
    # Query only the needed fields
    data = Artist.query.with_entities(Artist.id, Artist.name).all()
    return render_template('pages/artists.html', artists=data)


#  Show Artists
#  ----------------------------------------------------------------
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    data = Artist.query.get_or_404(artist_id)
    return render_template('pages/show_artist.html', artist=data)


#  Get Update Artists form
#  ----------------------------------------------------------------
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get_or_404(artist_id)

    # Loop over the form fields & populate the data if available
    for attr in form:
        if hasattr(artist, attr.name):
            attr.data = getattr(artist, attr.name)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


#  Update Artists
#  ----------------------------------------------------------------
def edit_artist_submission(artist_id):
    artist = Artist.query.get(artist_id)

    # Update the artist object
    artist.name = request.form.get('name')
    artist.city = request.form.get('city')
    artist.state = request.form.get('state')
    artist.phone = request.form.get('phone')
    artist.genres = request.form.getlist('genres')
    artist.image_link = request.form.get('image_link')
    artist.facebook_link = request.form.get('facebook_link')
    artist.website = request.form.get('facebook_link')
    artist.seeking_venue = request.form.get('seeking_venue') == 'y'
    artist.seeking_description = request.form.get('seeking_description')

    # Safely commit the changes to the db
    if safe_commit():
        flash('Artist ' + request.form['name'] + ' was successfully updated!')
    else:
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')

    return redirect(url_for('show_artist', artist_id=artist_id))


#  Delete Artist
#  ----------------------------------------------------------------
def delete_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    name  = artist.name
    db.session.delete(artist)

    # Safely commit the changes to the db
    if safe_commit():
        flash('Artist ' + name + ' was successfully deleted!')
    else:
        flash('The Artist has a show or more.'  + name + ' could not be deleted.')

    return redirect(url_for('artists'))

#  Search Artists
#  ----------------------------------------------------------------
def search_artists():
    search_term = request.form.get('search_term', '')
    results = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()

    response = {
        "count": len(results),
        "data": results
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))
